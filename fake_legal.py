import sys
import json
import urllib.request
import urllib.error
import argparse

BASE_URL = "https://fake.legal/api"

class FakeLegal:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.headers = {}
        if api_key:
            self.headers["x-api-key"] = api_key

    def _request(self, path, method="GET", data=None):
        url = f"{BASE_URL}{path}"
        req = urllib.request.Request(url, method=method, headers=self.headers)
        if data:
            req.add_header("Content-Type", "application/json")
            req.data = json.dumps(data).encode("utf-8")
        try:
            with urllib.request.urlopen(req) as res:
                return json.loads(res.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            try:
                err_data = json.loads(e.read().decode("utf-8"))
                return err_data
            except Exception:
                return {"success": False, "error": f"HTTP Error {e.code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_inbox(self, domain=None):
        path = "/inbox/new"
        if domain:
            path += f"?domain={domain}"
        return self._request(path)

    def create_custom_inbox(self, username, domain):
        return self._request("/inbox/custom", method="POST", data={"username": username, "domain": domain})

    def get_emails(self, address):
        return self._request(f"/inbox/{address}")

    def get_email(self, email_id):
        return self._request(f"/email/{email_id}")

    def get_stats(self):
        return self._request("/stats")

def main():
    parser = argparse.ArgumentParser(description="CLI for fake.legal Temporary Email Service")
    parser.add_argument("--api-key", help="Premium API key")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen_parser = subparsers.add_parser("generate", help="Generate a random inbox")
    gen_parser.add_argument("--domain", help="Select email domain")

    custom_parser = subparsers.add_parser("custom", help="Create a custom inbox")
    custom_parser.add_argument("username", help="Custom username")
    custom_parser.add_argument("domain", help="Email domain")

    inbox_parser = subparsers.add_parser("inbox", help="View inbox emails")
    inbox_parser.add_argument("address", help="Email address to check")

    email_parser = subparsers.add_parser("email", help="View a single email")
    email_parser.add_argument("id", help="Email ID")

    subparsers.add_parser("stats", help="Get service stats")

    args = parser.parse_args()
    client = FakeLegal(api_key=args.api_key)

    if args.command == "generate":
        res = client.create_inbox(domain=args.domain)
        if res.get("success"):
            print(res["address"])
        else:
            print(f"Error: {res.get('error', 'Failed to generate')}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "custom":
        res = client.create_custom_inbox(args.username, args.domain)
        if res.get("success"):
            print(res["address"])
        else:
            print(f"Error: {res.get('error', 'Failed to generate')}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "inbox":
        res = client.get_emails(args.address)
        if res.get("success") and res.get("exists"):
            emails = res.get("emails", [])
            if not emails:
                print("No emails found.")
            else:
                for email in emails:
                    print(f"[{email['id']}] From: {email['from']} - Subject: {email['subject']}")
        else:
            print(f"Error: {res.get('error', 'Failed to fetch inbox')}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "email":
        res = client.get_email(args.id)
        if res.get("success"):
            email = res["email"]
            print(f"From: {email['from']}")
            print(f"Subject: {email['subject']}")
            print("-" * 40)
            print(email.get("text", ""))
        else:
            print(f"Error: {res.get('error', 'Failed to fetch email')}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "stats":
        res = client.get_stats()
        print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
