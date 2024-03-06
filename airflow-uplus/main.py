import os
import time
import traceback

import zerohertzLib as zz
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# Slack Bot Token
SLACK = os.environ.get("SLACK")
# Login ID
USER_ID = os.environ.get("USER_ID")
# Login Password
USER_PASSWORD = os.environ.get("USER_PASSWORD")
# 결제에 사용할 카드 번호
CARD_NO = os.environ.get("CARD_NO")
# U+ 사용자 이름
NAME = os.environ.get("NAME")
# 생년월일
BIRTH = os.environ.get("BIRTH")
# 카드 만료 년도
CARD_YEAR = os.environ.get("CARD_YEAR")
# 카드 만료 월
CARD_MONTH = os.environ.get("CARD_MONTH")


class Browser:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        )
        self.browser = webdriver.Chrome(options)
        # U+ 접속
        self.browser.get("https://www.lguplus.com/login/onid-login")

    def click_xpath(self, element):
        element = self.browser.find_element("xpath", element)
        element.click()

    def send_id(self, element, key):
        element = self.browser.find_element("id", element)
        element.send_keys(key)

    def send_name(self, element, key):
        element = self.browser.find_element("name", element)
        element.send_keys(key)

    def select_id(self, element, key):
        element = self.browser.find_element("id", element)
        select = Select(element)
        select.select_by_value(key)

    def get_info(self):
        return self.browser.find_element(
            "xpath",
            "/html/body/div[6]/div[1]/div/div/div/div/div/div/div/div[1]/div/p",  # (이번달 납부하실 금액은 **,***원입니다.) | (납부할 요금이 없습니다.)
        ).text

    def get_status(self):
        try:
            return self.browser.find_element(
                "xpath", "/html/body/div[7]/div[1]/div/div/div/div"
            ).text
        except:
            return self.browser.find_element(
                "xpath",
                "/html/body/div[6]/div[1]/div/div/div/div/div/div/div/div[1]/div/p",
            ).text

    def get_price(self):
        element = self.browser.find_element(
            "xpath",
            "/html/body/div[6]/div[1]/div/div/div/div/div[1]/div/div/div[1]/div/p/strong",  # 이번달 납부하실 금액은 (**,***)원입니다.
        )
        return int(element.text[:-1].replace(",", ""))

    def send_price(self, PRICE):
        element = self.browser.find_element("id", "displayPayAmt")
        self.browser.execute_script("arguments[0].value = '';", element)
        element = self.browser.find_element("xpath", '//*[@id="displayPayAmt"]')
        element.send_keys(PRICE)

    def login(self):
        self.send_id("username-1-6", USER_ID)
        self.send_id("password-1", USER_PASSWORD)
        while len(self.browser.current_url.split("/")) == 5:
            self.click_xpath(
                "/html/body/div[1]/div/div/div[4]/div[1]/div/div[2]/div/div/div/div/section/div/button"
            )
            time.sleep(3)
        time.sleep(10)

    def move(self):
        self.browser.get("https://www.lguplus.com/mypage/payinfo?p=1")
        time.sleep(3)
        self.click_xpath(
            "/html/body/div[1]/div/div/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div[3]/button[1]"
        )
        time.sleep(8)

    def info(self, PRICE):
        self.send_id("cardNo", CARD_NO)
        self.send_name("cardCustName", NAME)
        self.send_name("cardCustbirth", BIRTH)
        self.select_id("selCardDate1", CARD_YEAR)
        self.select_id("selCardDate2", CARD_MONTH)
        self.send_price(PRICE)
        self.send_price(PRICE)


def main(slack):
    browser = Browser()
    # U+ 로그인
    browser.login()
    # 결제 화면 이동
    browser.move()
    # 결제 잔액 확인
    try:
        tmp = browser.get_info()
    except:
        tmp = browser.get_status()
    if "납부할 요금이 없습니다." in tmp:
        slack.message(":bell: [결제 :x:]: 납부할 요금이 없습니다.")
        return None
    if "5,999" in tmp:
        slack.message(":bell: [결제 :x:]: 이번달 납부하실 금액은 5,999원입니다.")
        return None
    tmp = browser.get_price()
    # 결제 가격
    if tmp == 0 or tmp == 5999:
        slack.message(f":no_bell: [결제 :x:] 자동결제 금액:\t{int(tmp):,.0f}원")
        return None
    elif tmp > 5999 + 5999:
        PRICE = "5999"
    else:
        PRICE = str(tmp - 5999)
    # 결제 정보 입력
    slack.message(f":bell: [결제 :o:] 결제 예정 금액:\t{int(PRICE):,.0f}원")
    browser.info(PRICE)
    # 결제
    browser.click_xpath("/html/body/div[6]/div[1]/div/div/footer/button[2]")
    slack.message(f":bell: [결제 :o:] 결제 완료!:\t{int(PRICE):,.0f}원")
    slack.message(
        f":bell: [결제 :o:] 결제 후 결제 예정 금액:\t{tmp - int(PRICE):,.0f}원"
    )
    return None


if __name__ == "__main__":
    slack = zz.api.SlackBot(SLACK, "uplus", name="U+", icon_emoji="iphone", timeout=30)
    try:
        main(slack)
    except Exception as e:
        response = slack.message(
            ":warning:" * 3
            + "\tERROR!!!\t"
            + ":warning:" * 3
            + "\n"
            + "```\n"
            + str(e)
            + "\n```",
        )
        slack.message(traceback.format_exc(), True, response.json()["ts"])
