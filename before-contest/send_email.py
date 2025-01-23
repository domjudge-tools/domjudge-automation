import json
import os
import smtplib


def send_email(user, pwd, recipient, subject, body):

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (
        FROM,
        ", ".join(TO),
        SUBJECT,
        TEXT,
    )
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print("successfully sent the mail")
    except:
        print("failed to send mail")


# SMTP_SSL Example
body = """Subject: BCPC League\n\n
سلام بچه ها،

اطلاعات ورود شما به شرح زیر است:

یوزرنیم:
{username}
پسورد:
{password}

برای شرکت در مسابقه، به آدرس زیر مراجعه کنید:
https://bircpc.ir/

اگر مشکلی در ورود به سایت داشتید یا سوالی برایتان پیش آمد، از طریق ایمیل یا گروه تلگرام مارا مطلع کنید.

با آرزوی موفقیت،
انجمن علمی کامپیوتر دانشگاه بیرجند"""

sender_email_address = os.environ.get("SENDER_EMAIL_ADDRESS", "")
sender_email_password = os.environ.get("SENDER_EMAIL_PASSWORD", "")

server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server_ssl.ehlo()  # optional, called by login()
server_ssl.login(sender_email_address, sender_email_password)

passwords = {}
with open("accounts.tsv", encoding="utf8") as f:
    passwords = {
        line.split("\t")[-3]: line.split("\t")[-1] for line in f.readlines()[1:]
    }
    

with open("domjudge_users.json", encoding="utf8") as f:
    users = json.load(f)
a = {
    "TeamName": "Tid",
}


for _t, user in users.items():
    tname = user["team"]
    t = a[tname]
    password = passwords[tname.replace("'", "&#039;").strip()]

    print(t, user["email"], passwords[tname.replace("'", "&#039;").strip()])

    server_ssl.sendmail(
        sender_email_address,
        user["email"],
        body.format(username=t, password=password).encode("utf8"),
    )

    print("sent")

# server_ssl.quit()
server_ssl.close()
print("successfully sent the mail")
