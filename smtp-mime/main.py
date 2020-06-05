import smtplib
import os
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email import encoders
import argparse

class MailSender:
    def __init__(self, from_, to, sub, server, verbose, dir, password):
        files = os.listdir(dir)

        addr_from = from_
        addr_to = to

        msg = MIMEMultipart()
        msg['From'] = addr_from
        msg['To'] = addr_to
        msg['Subject'] = sub

        for filepath in files:
            ctype, encoding = mimetypes.guess_type(filepath)
            filename = os.path.basename(filepath)
            try:
                maintype, subtype = ctype.split('/', 1)
            except Exception:
                continue
            if maintype == "image":
                with open(dir+ "/" + filepath, 'rb') as fp:
                    file = MIMEImage(fp.read(), _subtype=subtype)
                encoders.encode_base64(file)
                file.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(file)

        server = smtplib.SMTP(server)
        server.starttls()
        server.login(addr_from, password)
        server.send_message(msg)
        if bool(verbose):
            server.set_debuglevel(True)
        server.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="адрес (или доменное имя) SMTP-сервера")
    parser.add_argument("-t", help="почтовый адрес получателя письма")
    parser.add_argument("-f", help="почтовый адрес отправителя", default="<>")
    parser.add_argument("--subject", help="необязательный параметр, задающий тему письма", default="Happy Pictures")
    parser.add_argument("-v", help="отображение протокола работы")
    parser.add_argument("-d", help="каталог с изображениями", default=".")
    args = parser.parse_args()
    password = input()
    MailSender(args.f, args.t, args.subject, args.s, args.v, args.d, password)

