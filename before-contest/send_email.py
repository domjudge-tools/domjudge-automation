import json
import os
import smtplib

from dotenv import load_dotenv

# Load environment variables for SMTP
load_dotenv()
SENDER_EMAIL = os.environ.get("SENDER_EMAIL_ADDRESS")
SENDER_PASSWORD = os.environ.get("SENDER_EMAIL_PASSWORD")
if SENDER_EMAIL is None or SENDER_PASSWORD is None:
    print("Both Email and Password are required.")
    exit()

SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))

# Email body template
BODY_TEMPLATE = """سلام بچه ها،

اطلاعات ورود شما به شرح زیر است:

یوزرنیم: {username}
پسورد: {password}

برای شرکت در مسابقه، به آدرس زیر مراجعه کنید:
https://bircpc.ir/

اگر مشکلی در ورود به سایت داشتید یا سوالی برایتان پیش آمد، از طریق ایمیل یا گروه تلگرام ما را مطلع کنید.

همچنین می‌تونید اخبار و اطلاعات بیشتر در مورد مسابقمون رو توی وبلاگ دنبال کنید:
https://blog.bircpc.ir/

با آرزوی موفقیت،
انجمن علمی کامپیوتر دانشگاه بیرجند
"""

# Function to send a single email

def send_email(sender_email: str, sender_password: str, recipient: str, subject: str, body: str):
    headers = [
        f"From: {sender_email}",
        f"To: {recipient}",
        f"Subject: {subject}",
        "Content-Type: text/plain; charset=utf-8"
    ]
    message = "\r\n".join(headers) + "\r\n\r\n" + body

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, message.encode('utf-8'))
        print(f"✅ Email sent to {recipient}")

# Load created users info
def load_created_users(path: str = 'created_users.json'):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

if __name__ == '__main__':
    users = load_created_users()
    subject = "دسترسی به لیگ BCPC"

    for user in users:
        recipient = user['email']
        username = user['username']
        password = user['password']
        try:
            send_email(
                sender_email=SENDER_EMAIL,
                sender_password=SENDER_PASSWORD,
                recipient=recipient,
                subject=subject,
                body=BODY_TEMPLATE.format(username=username, password=password)
            )
        except Exception as e:
            print(f"❌ Failed to send to {recipient}: {e}")
