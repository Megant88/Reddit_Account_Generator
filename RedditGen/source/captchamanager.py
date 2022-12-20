import requests
import time
from colorama import Fore

def twocaptcha(key):
    s = requests.get(f"http://2captcha.com/in.php?key={key}&method=userrecaptcha&googlekey=6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC&pageurl=https://reddit.com/register&userAgent=Mozilla/5.0%20(Windows%20NT%2010.0;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/105.0.0.0%20Safari/537.36")
    if "ERROR" in s.text:
        return s.text, False
    else:
        taskid = s.text[3:]
        while True:
            s = requests.get(f"http://api.2captcha.com/res.php?key={key}&action=get&id={taskid}")
            if "ERROR" in s.text:
                return s.text, False
            time.sleep(2.5)
            if "OK" in s.text:
                captchatoken = s.text[3:]
                return captchatoken, True

def captchaguru(key):
    s = requests.get(f"http://api.captcha.guru/in.php?key={key}&method=userrecaptcha&googlekey=6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC&pageurl=https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC&co=aHR0cHM6Ly93d3cucmVkZGl0LmNvbTo0NDM.&hl=de&v=vP4jQKq0YJFzU6e21-BGy3GP&size=normal&cb=mjdz35h2g49")
    if "ERROR" in s.text:
        return s.text, False
    else:
        taskid = s.text[3:]
        waiting = True
        while waiting:
            s = requests.get(f"http://api.captcha.guru/res.php?key={key}&action=get&id={taskid}")
            if "ERROR" in s.text:
                 return s.text, False
            time.sleep(5)
            if "OK" in s.text:
                captchatoken = s.text[3:]
                waiting = False
                return captchatoken, True

def anticaptcha(key, service): ## compitable with captchaio
    s = requests.post(f"https://api.{service}/createTask", json={"clientKey": {key}, "task": {"type": "RecaptchaV2TaskProxyless", "websiteURL": "https://reddit.com/register", "websiteKey": "6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC", "userAgent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}})
    errrorID = s.json()["errorId"]
    if errrorID != "0":
        return s.text, False
    else:
        taskId = s.json()["taskId"]
        time.sleep(3.5)
        waiting = True
        while waiting:
             time.sleep(1.5)
             s = requests.post("https://api.{service}/getTaskResult", data={f"clientKey":{key},"taskId":{taskId}})
             errrorID = s.json()["errorId"]
             if errrorID != "0":
                return s.text, False
             else:
                status = s.json()["status"]
                if status == "ready":
                    captchatoken = s.json["solution"]["gRecaptchaResponse"]
                    return captchatoken, True
