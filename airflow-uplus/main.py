import os
import time

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


def xpath_click(browser, element):
    element = browser.find_element("xpath", element)
    element.click()


def id_send(browser, element, key):
    element = browser.find_element("id", element)
    element.send_keys(key)


def name_send(browser, element, key):
    element = browser.find_element("name", element)
    element.send_keys(key)


def id_select(browser, element, key):
    element = browser.find_element("id", element)
    select = Select(element)
    select.select_by_value(key)


def get_info(browser):
    element = browser.find_element(
        "xpath",
        "/html/body/div[5]/div[1]/div/div/div/div/div/div/div/div[1]/div/p",  # (이번달 납부하실 금액은 **,***원입니다.) | (납부할 요금이 없습니다.)
    )
    return element.text


def get_price(browser):
    element = browser.find_element(
        "xpath",
        "/html/body/div[5]/div[1]/div/div/div/div/div[1]/div/div/div[1]/div/p/strong",  # 이번달 납부하실 금액은 (**,***)원입니다.
    )
    return int(element.text[:-1].replace(",", ""))


def price_send(browser, PRICE):
    element = browser.find_element("id", "displayPayAmt")
    browser.execute_script("arguments[0].value = '';", element)
    element = browser.find_element("xpath", '//*[@id="displayPayAmt"]')
    element.send_keys(PRICE)


def login(browser):
    id_send(browser, "username-1-6", USER_ID)
    id_send(browser, "password-1", USER_PASSWORD)
    xpath_click(
        browser,
        "/html/body/div[1]/div/div/div[4]/div[1]/div/div[2]/div/div/div/div/section/div/button",
    )
    xpath_click(
        browser,
        "/html/body/div[1]/div/div/div[4]/div[1]/div/div[2]/div/div/div/div/section/div/button",
    )
    time.sleep(5)


def move(browser):
    browser.get("https://www.lguplus.com/mypage/payinfo?p=1")
    time.sleep(3)
    xpath_click(
        browser,
        "/html/body/div[1]/div/div/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div[3]/button[1]",
    )
    time.sleep(8)


def info(browser, PRICE):
    id_send(browser, "cardNo", CARD_NO)
    name_send(browser, "cardCustName", NAME)
    name_send(browser, "cardCustbirth", BIRTH)
    id_select(browser, "selCardDate1", CARD_YEAR)
    id_select(browser, "selCardDate2", CARD_MONTH)
    price_send(browser, PRICE)
    price_send(browser, PRICE)


if __name__ == "__main__":
    slack = zz.api.SlackBot(SLACK, "zerohertz", name="U+", icon_emoji="iphone")
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        )
        browser = webdriver.Chrome(options)

        # U+ 접속
        browser.get("https://www.lguplus.com/login/onid-login")

        # U+ 로그인
        login(browser)

        # 결제 화면 이동
        move(browser)

        # 결제 잔액 확인
        tmp = get_info(browser)
        if "납부할 요금이 없습니다." in tmp:
            slack.message(f":bell: [결제 :x:] {tmp}")
            exit()
        tmp = get_price(browser)

        # 결제 가격
        if tmp == 0 or tmp == 5999:
            slack.message(f":no_bell: [결제 :x:] 자동결제 금액:\t{tmp}원")
            exit()
        elif tmp > 5999 + 5999:
            PRICE = "5999"
        else:
            PRICE = str(tmp - 5999)

        # 결제 정보 입력
        slack.message(f":bell: [결제 :o:] 결제 예정 금액:\t{PRICE}원")
        info(browser, PRICE)

        # 결제
        xpath_click(browser, "/html/body/div[5]/div[1]/div/div/footer/button[2]")
        slack.message(f":bell: [결제 :o:] 결제 완료!:\t{PRICE}원")
        slack.message(f":bell: [결제 :o:] 결제 후 결제 예정 금액:\t{tmp - int(PRICE)}원")
    except Exception as e:
        slack.message(
            ":warning:" * 10
            + "ERROR!!!"
            + ":warning:" * 10
            + "\n"
            + "```\n"
            + str(e)
            + "\n```",
        )
