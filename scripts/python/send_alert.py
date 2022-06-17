from helpers.mail import temp_dir, send_mail
import platform


def main():
    err_file = temp_dir / "error.txt"
    if not err_file.is_file():
        return
    err_msgs = []
    body = ""
    with open(err_file) as err_file:
        err_msgs = err_file.readlines()
    if len(err_msgs) == 0:
        return
    body += "<ul>"
    for err_msg in err_msgs:
        body += f"<li>{err_msg}</li>"
    body += "</ul>"

    node_name = platform.node()
    subject = f"[Alert] {node_name}"
    send_mail(msg=body, subject=subject)


if __name__ == "__main__":
    main()
