"""
A simple Gmail API wrapper for reading emails.
We only Read emails, we don't send or modify anything.
"""

import base64
from typing import List, Dict
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from config import GMAIL_TOKEN_FILE, GMAIL_CREDENTIALS_FILE

SCOPES = ["https://mail.google.com/"]

class GmailClient:
    """
    a small client for Gmail.
    Uses token.json and credentials.json that were created by main.py.
    """

    def __init__(self, token_file: str = GMAIL_TOKEN_FILE):
        """
        initialize the Gmail service object with given token file.
        """
        # Load credentials from the token file
        self.creds = Credentials.from_authorized_user_file(token_file, SCOPES)

        #Build the Gmail service object
        self.service = build("gmail", "v1", credentials=self.creds)

    def _get_message(self, msg_id: str) -> Dict:
        """
        internal helper to fetch a full message by its ID
        """
        message = self.service.users().messages().get(
            userId="me",
            id=msg_id,
            format="full"
        ).execute()
        return message

    def _get_subject(self, msg: Dict) -> str:
        """
        Extract the subject from the email message headers.
        """
        headers = msg.get("payload", {}).get("headers", [])
        for header in headers:
            if header.get("name", "").lower() == "subject":
                return header.get("value", "")
        return ""
    
    def _get_body_text(self, msg: Dict) -> str:
        """
        Extract plain text body from a Gmail message
        """
        payload = msg.get("payload", {})
        body_data = None

        # For multipat messages, find the text/plain part
        parts = payload.get("parts", [])
        if parts:
            #looking for text/plain part
            for part in parts:
                if part.get("mimeType") == "text/plain":
                    body_data = part.get("body", {}).get("data")
                    break
        else:
            #Single part message
            body_data = payload.get("body", {}).get("data")
        if not body_data:
            return ""
        
        # Decode from base64url
        body_bytes = base64.urlsafe_b64decode(body_data.encode("UTF-8"))
        body_text = body_bytes.decode("UTF-8", errors="ignore")
        return body_text
    
    def get_inbox_emails(self, max_results: int = 50) -> List[Dict]:
        """
        get a list of emails from the inbox
        each mail has a dictionary with keys: 'subject' and 'body'
        """
        result = self.service.users().messages().list(
            userId="me",
            q="in:inbox",
            maxResults=max_results
        ).execute()

        messages = result.get("messages", [])
        emails: List[Dict] = []

        for msg_meta in messages:
            msg_id = msg_meta.get("id")
            full_msg = self._get_message(msg_id)
            subject = self._get_subject(full_msg)
            body = self._get_body_text(full_msg).strip()

            emails.append({
                "subject": subject,
                "body": body
            })

            return emails
        
    def get_urgent_emails(self, max_results: int = 50) -> List[Dict]:
        """
        Return emails which body contains the word "urgent"
        each item has: subject and body
        """

        all_emails = self.get_inbox_emails(max_results=max_results)
        urgent_emails: List[Dict] = []

        for email in all_emails:
            body_lower = email["body"].lower()
            if "urgent" in body_lower:
                urgent_emails.append(email)

        return urgent_emails
        
    def get_emails_grouped_by_subject(self, max_results: int = 50) -> Dict[str, List[str]]:
        """
        Groupin emails by subject
        will retrun: {subject: [body1, body2, ...],...}
        Will be used to merge messages 
        """
        all_emails = self.get_inbox_emails(max_results=max_results)
        grouped: Dict[str, List[str]] = {}
        for email in all_emails:
            subject = email["subject"].strip()
            body = email["body"].strip()

            if subject not in grouped:
                grouped[subject] = []
                
            # Avoiding duplicates of the exact same body text
            if body and body not in grouped[subject]:
                grouped[subject].append(body)
        return grouped

        