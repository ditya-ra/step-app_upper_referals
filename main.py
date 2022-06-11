import os
import re
import time
from datetime import datetime
import requests

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from peewee import fn
from loguru import logger

from settings.driver_settings import Driver
from models.models import Proxy, Account, Statistic


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logger.add(f"{os.path.join(BASE_DIR, 'logger.log')}", format="{time} $$$ {level} $$$ {message}", level="INFO")


def ref_action(proxy: Proxy, account: Account):
    driver_class = Driver(proxy=proxy)
    driver = driver_class.driver_init()
    driver.get("https://2ip.ru/")
    time.sleep(600)
    return
    try:
        driver.get("https://temp-mail.org/en/")
        time.sleep(10)
        driver.find_element(By.ID, "click-to-copy").click()
        time.sleep(2)

        driver.execute_script('''window.open("https://app.step.app/","_blank");''')
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])
        input_email = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "email__input")), "Not Found Element"
        )
        input_email.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)
        done_button = driver.find_element(By.XPATH, "//div[text()='Done']")
        done_button.click()
        time.sleep(2)

        driver.switch_to.window(driver.window_handles[0])
        email_message = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'StepApp')]")), "Not Found Element"
        )
        email_message.click()
        time.sleep(5)

        code_p = driver.find_element(By.XPATH, "//p[contains(text(),'Your verification code')]").text
        code_value = re.search(r"\d{6}", code_p).group(0)

        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        email_code_div = driver.find_element(By.CLASS_NAME, "email-code-input")
        code_inputs = email_code_div.find_elements(By.TAG_NAME, "input")
        for code, input_ in zip(str(code_value), code_inputs):
            input_.send_keys(code)

        time.sleep(5)
        ref_code_div = driver.find_element(By.CLASS_NAME, "email-code-input")
        ref_code_inputs = ref_code_div.find_elements(By.TAG_NAME, "input")
        ref_code_value = account.ref_code
        for code, input_ in zip(ref_code_value, ref_code_inputs):
            input_.send_keys(code)

        time.sleep(2)
        Statistic(date=datetime.now(), account=account, proxy=proxy).save()
    except Exception as ex:
        logger.error(f"Not filing with proxy:{proxy.id} and account:{account.id} error:{ex}")
    finally:
        driver.close()
        driver.quit()


def main():
    accounts = Account.select()
    while True:
        for account in accounts:
            try:
                proxy = Proxy.select().where(~Proxy.id.in_(Statistic.select(Statistic.proxy))).order_by(fn.Random()).get()
            except:
                logger.info("proxy out of range")
                break
            ref_action(proxy=proxy, account=account)


if __name__ == '__main__':
    main()