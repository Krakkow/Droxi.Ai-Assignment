from api.gmail_client import GmailClient

def main():
    client = GmailClient()

    print("Some emails from inbox:")
    emails = client.get_inbox_emails(max_results=50)
    for email in emails:
        print("------")
        print(f"Subject: {email['subject']}")
        print(f"Body: (first 100 chars): {email['body'][:100]}")
        print("")


    print("\nUrgent emails:")
    urgent_emails = client.get_urgent_emails(max_results=20)
    if not urgent_emails:
        print("No urgent emails found.")
    else:
        for email in urgent_emails:
            print("------")
            print(f"Subject: {email['subject']}")
            print(f"Body: {email['body']}")
            print("")

if __name__ == "__main__":
    main()