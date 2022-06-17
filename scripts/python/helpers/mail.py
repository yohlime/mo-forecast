import os
import warnings
import yagmail
import json
from pathlib import Path
from typing import List

main_dir = os.getenv("MAINDIR")
if main_dir is None:
    raise NotADirectoryError("MAINDIR")
main_dir = Path(main_dir)

temp_dir = os.getenv("TEMP_DIR")
if temp_dir is None:
    raise NotADirectoryError("TEMP_DIR")
temp_dir = Path(temp_dir)

script_dir = os.getenv("SCRIPT_DIR")
if script_dir is None:
    script_dir = main_dir / "scripts"
    warnings.warn(f"SCRIPT_DIR not set, script_dir set to '{script_dir}'")
script_dir = Path(script_dir)

username = os.getenv("MAIL_USERNAME")
if username is None:
    raise ValueError("MAIL_USERNAME")

password = os.getenv("MAIL_PASSWORD")
if password is None:
    raise ValueError("MAIL_PASSWORD")

mail = yagmail.SMTP(username, password)

conf_file = open(script_dir / "python/config/mail.json")
mail_conf = json.load(conf_file)
conf_file.close()


def send_mail(msg: str, to: List[str] = None, subject: str = None):
    if to is None:
        to = mail_conf.get("to", [])
    if subject is None:
        subject = mail_conf.get("subject", "[Alert]")
    if (len(to) == 0) or (len(msg) == 0):
        return
    if len(to) > 1:
        mail.send(to=to[0], bcc=to[1:], subject=subject, contents=msg)
    else:
        mail.send(to=to, subject=subject, contents=msg)
