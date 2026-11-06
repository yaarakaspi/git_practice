import base64
import smtplib

SMPT_PORT = 25

# creating session
s = smtplib.SMTP('smtp.gmail.com', SMPT_PORT)
# starting tls
s.starttls()
# authentication
s.login("yaara.kaspi@gmail.com", "snin sypk gyln bhtc")
# message to send
msg1 = "Subject: Mail from Yaara\n\nThere's no place like 127.0.0.1"
# sending the mail
s.sendmail("yaara.kaspi@gmail.com", "merrygeva312@gmail.com", msg1)


# getting img
img_name = "C:\\Users\\admin\\Pictures\\Screenshots\\mailJoke.png"
with open(img_name, "rb") as f:
    encoded_img = base64.b64encode(f.read()).decode()
# building message
boundary = "=============="
msg2 = f"""Content-Type: multipart/mixed; boundary="{boundary}"
--{boundary}
Content-Type: text/plain

Mail from Yaara

--{boundary}
Content-Type: image/png; name = "C:\\Users\\admin\\Pictures\\Screenshots\\mailJoke.png"
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename={img_name}

{encoded_img}
--{boundary}--"""

s.sendmail("yaara.kaspi@gmail.com", "merrygeva312@gmail.com", msg2)
# quitting
s.quit()
