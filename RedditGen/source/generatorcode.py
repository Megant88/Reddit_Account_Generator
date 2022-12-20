import httpx
import json
from source.captchamanager import anticaptcha, captchaguru, twocaptcha
from source.emailmanager import kopeechka, emailverification
from source.utils import namorator, random_char
import re
import random
from colorama import Fore
from getuseragent import UserAgent

with open("config.json") as f:
    config = json.load(f)
captchaKey = config["captcha"]["captchakey"]
captchaApi = config["captcha"]["captchasolver"]
emailverify = config["EmailVerification"]["Verify"]
emailservice = config["EmailVerification"]["emailservice"]
emailkey = config["EmailVerification"]["emailkey"]
useproxy = config["Proxy"]["Proxy"]


def generator():
    while True:
        if useproxy:
            randomproxy = random.choice(open("proxies.txt").readlines())
            proxy = {"http://": "http://" + randomproxy, "https://": "http://" + randomproxy, }
        else:
            proxy = None
        username = namorator()
        password = random_char(10)
        if emailverify == True:
            email, taskid = kopeechka(emailkey)
        else:
            email = random_char(12) + "@outlook.com"
        email2 = email.replace("@", "%40")
        print(f"{Fore.WHITE}[{Fore.BLUE}+{Fore.WHITE}] {Fore.BLUE}Solving Captcha with {captchaApi}")
        if captchaApi == "anti-captcha.com" or captchaApi == "captchaai.io":
            captchatoken, if_error = anticaptcha(captchaKey, captchaApi)
        elif captchaApi == "captcha.guru":
            captchatoken, if_error = captchaguru(captchaKey)
        elif captchaApi == "2captcha.com":
            captchatoken, if_error = twocaptcha(captchaKey)
        else:
            exit(f"{Fore.WHITE}[{Fore.YELLOW}-{Fore.WHITE}]{Fore.RED} not supported captcha service")
        if if_error == False:
            print(f"{Fore.WHITE}[{Fore.YELLOW}-{Fore.WHITE}]{Fore.RED} Failed to get captcha: {captchatoken}")
        else:
            print(f"{Fore.WHITE}[{Fore.BLUE}+{Fore.WHITE}] {Fore.BLUE}Solved Captcha")
            random_browser = ["firefox","chrome"]
            useragent = UserAgent(random.choice(random_browser))
            random_useragent = useragent.Random()
            header = {'accept': '*/*', 'accept-encoding': 'gzip, deflate', 'accept-language': 'en-US,en;q=0.9',
                      'origin': 'https://www.reddit.com', 'referer': 'https://www.reddit.com/register/',
                      'sec-ch-ua': '"Chromium";v="105", "Not)A;Brand";v="8"', 'sec-ch-ua-mobile': '?0',
                      'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors',
                      'sec-fetch-site': 'same-origin',
                      'user-agent': f'{random_useragent}'}
            with httpx.Client(headers=header, proxies=proxy, verify=False) as client:
                try:
                    response = client.get("https://www.reddit.com/register/")
                    result = re.search('name="csrf_token" value="(.*)"', response.text)
                    csrftoken = result.group(1)
                except Exception as e:
                    print(f"{Fore.WHITE}[{Fore.YELLOW}-{Fore.WHITE}]{Fore.RED} Exception occured: {e}")
                else:
                    try:
                        registerresp = client.post("https://www.reddit.com/register", data=(
                            f"csrf_token={csrftoken}&g-recaptcha-response={captchatoken}&password={password}&dest=https%3A%2F%2Fwww.reddit.com&lang=en-GB&username={username}&email={email2}"))
                    except Exception as e:
                        print(f"{Fore.WHITE}[{Fore.YELLOW}-{Fore.WHITE}]{Fore.RED} Exception occured: {e}")
                    else:
                        if "https://www.reddit.com" not in registerresp.text:
                            n = registerresp.text.replace("\n", "")
                            print(f"{Fore.WHITE}[{Fore.YELLOW}-{Fore.WHITE}]{Fore.RED} Failed to register: {n}")
                        else:
                            open("accounts.txt", "a").write(f"{username}:{password} \n")
                            print(
                                f"{Fore.WHITE}[{Fore.BLUE}+{Fore.WHITE}] {Fore.GREEN}Generated unverified account successfully, {username}:{password}")
                            if emailverify == True:
                                link = emailverification(emailkey,taskid)  # doesnt work since for some reason I have issues parsing the verificationcode
                                verifyurl = client.get(link)
                                checkurl = dict(verifyurl.headers)
                                try:
                                    if "?verified=true" in checkurl.get('location'):
                                       print(
                                       f'{Fore.WHITE}[{Fore.BLUE}+{Fore.WHITE}] {Fore.GREEN}Account "{username}" has been successfully verified')
                                    else:
                                        print(Fore.RED + "Account created but failed to verify")
                                except Exception as e:
                                    print(f"{Fore.WHITE}[{Fore.YELLOW}-{Fore.WHITE}]{Fore.RED} Exception occured: {e}")
