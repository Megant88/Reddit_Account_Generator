from time import sleep
import requests
import re

def kopeechka(key):
    s = requests.get(f"http://api.kopeechka.store/mailbox-get-email?site=reddit.com&mail_type=Outlook&token={key}&soft=68&api=2.0")
    status = s.json()["status"]
    if status != "OK":
        return s.text, False
    else:
        taskid = s.json()["id"]
        mail = s.json()["mail"]
        return mail, taskid

def emailverification(key, taskid):
    sleep(5)
    while True:
        resp = requests.get(f"http://api.kopeechka.store/mailbox-get-message?full=1&id={taskid}&token={key}&api=2.0")
        if resp.json()["value"] == "WAIT_LINK":
            pass
        else:
            str_html = resp.json()['fullmessage']
            search_element = re.findall(
                '<a href="[^"]*" target="_blank" class="link c-white" style="display: block; padding: 8px; text-decoration:none; color:#ffffff;"><span class="link c-white" style="text-decoration:none; color:#ffffff;">',
                str_html)
            search_url = re.search('"[^"]*"', search_element[0])
            verification_url = search_url[0].strip('"')
            return verification_url