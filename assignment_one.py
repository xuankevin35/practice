from selenium import webdriver # 用来驱动浏览器的
from selenium.webdriver import ActionChains # 破解滑动验证码的时候用的 可以拖动图片
from selenium.webdriver.common.by import By # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC # 和下面WebDriverWait一起用的
from selenium.webdriver.support.wait import WebDriverWait # 等待页面加载某些元素
import time
from pyquery import PyQuery as pq

url = 'http://125.35.6.80:8181/ftban/fw.jsp'
brand_list = ['珀莱雅', '彩棠', '优资莱', '悦芙媞', '丸美', '春纪', '恋火', '润百颜', '夸迪', \
    'Bio-MESO肌活', '米蓓尔', '佰草集', '玉泽', '美加净', '六神', '高夫', '启初', '双妹', '家安', \
    '汤美星', '一花一木', '百雀羚', '三生花', '伊丽莎白雅顿', '欧珀莱', '沙宣', 'P&G', 'OLAY', \
    '雅芳', '毛戈平', 'AUSSIE', '佳洁士', '黑人', '芙莉美娜', '吉列', '伊丽莎白雅顿', \
    '赫妍', '兰芝', '吕', '艾诺碧', '雪花秀', '梦妆', '泡泡玛特']

driver = webdriver.Firefox()

def search(brand):
    try:
        driver.implicitly_wait(2)
        searchtext = driver.find_elements_by_id('searchtext')[0]
        #print(searchtext)
        searchtext.send_keys(brand)
        print('Keyword entered!')
        #time.sleep(5)
        searchtext.send_keys(Keys.ENTER)
        #time.sleep(5)
        print('Keyword searched!')
    except Exception as e:
        print('Exception occurred: ' + e)

def get_pageNumber():
    try:
        page_number = driver.find_element_by_xpath('//div[@id="page"]/ul/li[7]').text
        return int(page_number) #/html/body/div[3]/div[2]/ul/li[7]
    except:
        print('Error occurred!')    

def next_page(i):
    try:
        txt_box = driver.find_elements_by_xpath('//*[@id="xlJumpNum"]')[0]
        txt_box.send_keys(i)
        button = driver.find_element_by_xpath('/html/body/div[3]/div[2]/ul/li[10]')
        button.click()
        print('Turned to page No.{}!'.format(i))
    except: # Exception as e:
        print('The last page!')
    
def get_info(brand):
    #driver.get(url)
    html = driver.page_source
    doc = pq(html)
    li_list = doc('.dzpzmain #FileItems #gzlist li').items()
    #print(li_list)
    for li in li_list:
        #print(li)
        Name = li.find('dl a').text()
        Number = li.find('ol a').text()
        Company = li.find('p').text()
        Time = li.find('i').text()
        with open('{}_info.txt'.format(brand), 'a', encoding='utf-8') as f:
            f.write(Name + '\t')
            f.write(Number + '\t')
            f.write(Company + '\t')
            f.write(Time + '\n')

def main():
    driver.get(url)
    driver.maximize_window()
    search('')
    for brand in brand_list:
        driver.get(url)
        search(brand)
        get_info(brand)
        page_number = get_pageNumber()
        for i in range(2, page_number + 1):
            next_page(i)
            get_info(brand)
    driver.close()

if __name__ == '__main__':
    main()

