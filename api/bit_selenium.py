from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from api.bit_api import *

if __name__ == "__main__":
    res = openBrowser(
        "062f0c4ce7814a5c9bf7fe0fd13a5a3d"
    )  # 窗口ID从窗口配置界面中复制，或者api创建后返回

    print(res)

    driverPath = res["data"]["driver"]
    debuggerAddress = res["data"]["http"]

    # selenium 连接代码
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", debuggerAddress)

    chrome_service = Service(driverPath)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # 以下为PC模式下，打开baidu，输入 BitBrowser，点击搜索的案例
    driver.get("https://www.baidu.com/")
    driver.get

    input = driver.find_element(By.CLASS_NAME, "s_ipt")
    input.send_keys("BitBrowser")

    print("before click...")

    btn = driver.find_element(By.CLASS_NAME, "s_btn")
    btn.click()

    print("after click")
