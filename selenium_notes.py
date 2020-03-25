from selenium import webdriver # 用来驱动浏览器的
from selenium.webdriver import ActionChains # 破解滑动验证码的时候用的 可以拖动图片
from selenium.webdriver.common.by import By # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC # 和下面WebDriverWait一起用的
from selenium.webdriver.support.wait import WebDriverWait # 等待页面加载某些元素
import time


# 1. 基本使用：
def try_baidu():
    driver = webdriver.Firefox()
    try:
        #driver.implicitly_wait(10) # 隐式等待:在查找所有元素时，如果尚未被加载，则等10秒
        wait = WebDriverWait(driver, 10) # 显式等待：显式地等待某个元素被加载

        driver.get('https://www.baidu.com')
        input_tag = wait.until(EC.presence_of_element_located((By.ID, "kw")))
        input_tag.send_keys('NBA') # 在搜索框在输入要搜索的内容
        input_tag.send_keys(Keys.ENTER) # 按键盘回车键

        #contents = driver.find_element_by_id('content_left')
        #print(contents)

        time.sleep(3)
    finally:
        driver.close()

# 2. 使用xpath：
def try_xpath():
    driver = webdriver.Firefox()
    try:
        driver.implicitly_wait(5)

        driver.get('https://doc.scrapy.org/en/latest/_static/selectors-sample1.html')

        html = driver.find_element_by_xpath('/html')
        print(html.tag_name)

        div1 = driver.find_element_by_xpath('//div')
        print(div1.tag_name)

        div2 = driver.find_element_by_xpath('//div[@id = "images"]')
        print(div2.tag_name)

        a = driver.find_element_by_xpath('//a')
        print(a.tag_name)

        a_s = driver.find_elements_by_xpath('//a')
        print(a_s)

        a_href = driver.find_element_by_xpath('//a').get_attribute('href')
        print(a_href)
    
    finally:
        driver.close()

# 3. 所有选择器：

'''
===============所有方法===================
    element是查找一个标签
    elements是查找所有标签

    1、find_element_by_link_text  通过链接文本去找
    2、find_element_by_id 通过id去找
    3、find_element_by_class_name
    4、find_element_by_partial_link_text
    5、find_element_by_name
    6、find_element_by_css_selector
    7、find_element_by_tag_name
'''
