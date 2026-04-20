import base64
from email.mime.text import MIMEText
from integrations.google_auth import get_gmail_service
from agent.tools import Tool


class GmailSendTool(Tool):
    def __init__(self):
        super().__init__(
            name='gmail_send',
            description='Send an email via Gmail. Provide recipient, subject, and body text.',
            parameters={
                'to': {'type': 'string', 'description': 'Recipient email address'},
                'subject': {'type': 'string', 'description': 'Email subject line'},
                'body': {'type': 'string', 'description': 'Email body text'},
            }
        )

    def execute(self, to='', subject='', body='', **kwargs) -> str:
        try:
            service = get_gmail_service()
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            sent = service.users().messages().send(
                userId='me', body={'raw': raw}
            ).execute()
            return f"Email sent to {to} | Message ID: {sent['id']}"
        except Exception as e:
            return f"Error sending email: {e}"


class GmailReadTool(Tool):
    def __init__(self):
        super().__init__(
            name='gmail_read',
            description='Read recent emails from your Gmail inbox.',
            parameters={
                'max_results': {'type': 'integer', 'default': 5},
                'unread_only': {'type': 'boolean', 'default': False},
            }
        )

    def execute(self, max_results=5, unread_only=False, **kwargs) -> str:
        try:
            service = get_gmail_service()
            query = 'is:unread' if unread_only else ''
            result = service.users().messages().list(
                userId='me', maxResults=max_results, q=query
            ).execute()
            messages = result.get('messages', [])
            if not messages:
                return 'No emails found.'
            lines = []
            for msg_ref in messages:
                msg = service.users().messages().get(
                    userId='me', id=msg_ref['id'], format='metadata',
                    metadataHeaders=['From', 'Subject', 'Date']
                ).execute()
                headers = {h['name']: h['value'] for h in msg['payload']['headers']}
                lines.append(
                    f"- From: {headers.get('From', '?')} | "
                    f"Subject: {headers.get('Subject', '(no subject)')} | "
                    f"Date: {headers.get('Date', '?')}"
                )
            return '\n'.join(lines)
        except Exception as e:
            return f"Error reading emails: {e}"


class GmailSearchTool(Tool):
    def __init__(self):
        super().__init__(
            name='gmail_search',
            description='Search Gmail inbox using Gmail query syntax (e.g. "from:boss subject:meeting").',
            parameters={
                'query': {'type': 'string', 'description': 'Gmail search query'},
                'max_results': {'type': 'integer', 'default': 5},
            }
        )

    def execute(self, query='', max_results=5, **kwargs) -> str:
        try:
            service = get_gmail_service()
            result = service.users().messages().list(
                userId='me', maxResults=max_results, q=query
            ).execute()
            messages = result.get('messages', [])
            if not messages:
                return f'No emails matching "{query}".'
            lines = []
            for msg_ref in messages:
                msg = service.users().messages().get(
                    userId='me', id=msg_ref['id'], format='metadata',
                    metadataHeaders=['From', 'Subject', 'Date']
                ).execute()
                headers = {h['name']: h['value'] for h in msg['payload']['headers']}
                lines.append(
                    f"- From: {headers.get('From', '?')} | "
                    f"Subject: {headers.get('Subject', '(no subject)')} | "
                    f"Date: {headers.get('Date', '?')}"
                )
            return '\n'.join(lines)
        except Exception as e:
            return f"Error searching emails: {e}"
