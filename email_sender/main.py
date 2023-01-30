import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path

html = Template(Path("index.html").read_text())
email =EmailMessage()
email["from"]="MQ"
email["to"]="deciver5@gmail.com"
email["subject"]="Python test"

email.set_content(html.substitute(name="Tim"),"html")

with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login("marcinqunik@gmail.com","tGtP3ULmX2N5YDq")
    smtp.send_message(email)
    print("Done!")



#tGtP3ULmX2N5YDq marcinqunik@gmail.com