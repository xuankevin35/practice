import pyodbc
import requests
from bs4 import BeautifulSoup
import re
import pyodbc

base_url = 'http://58921.com/alltime'
login_url = 'http://58921.com/user/login'

server = '39.106.71.104'
database = 'Orinsight_Db'
username = 'orinsight'
password = 'ddsz#123'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'

}
cookies = {
    'Cookie': 'Hm_lvt_e71d0b417f75981e161a94970becbb1b=1584709306,1584734931,1584997434; DIDA642a4585eb3d6e32fdaa37b44468fb6c=d1n9upspj4c7nqlksnrk9er785; remember=0; time=MTEzNTI2LjIxNjM0Mi4xMDI4MTYuMTA3MTAwLjExMTM4NC4yMDc3NzQuMTE5OTUyLjExMTM4NC4xMDQ5NTguMTEzNTI2LjExOTk1Mi4xMTEzODQuMTIyMDk0LjEyMjA5NC4xMTc4MTAuMTExMzg0LjEyMjA5NC4xMDI4MTYuMA%3D%3D; Hm_lpvt_e71d0b417f75981e161a94970becbb1b=1584997493'

}

def get_info(url, headers, cookies):
    r = requests.get(url, headers = headers, cookies = cookies)
    r.raise_for_status()
    r.encoding = 'utf-8'
    html_doc = r.text

    soup = BeautifulSoup(html_doc, 'lxml')

    tr_list = soup.find('tbody').findAll('tr')
    info_sum = []
    for tr in tr_list:
        info = {}
        
        pattern1 = re.compile(r'<td>(.*?)</td>')
        pattern2 = re.compile(r'title=".*?">(.*?)</a>')
        info1 = pattern1.findall(str(tr))
        info2 = pattern2.findall(str(tr))

        info['yearRank'] = info1[0]
        info['histRank'] = info1[1]
        info['Name'] = info2[0]
        info['peopleCount'] = info1[4]
        info['totalCount'] = info1[5]
        info['year'] = info1[6]

        info_sum.append(info)
    return info_sum

def Out2File(number, dict):
    with open('page{}.txt'.format(str(number)), 'w+', encoding= 'utf-8') as f:
        for info in dict:
            f.write(info['yearRank'] + '\t' + info['histRank'] + '\t' +
                info['Name'] + '\t' + info['peopleCount'] + '\t' +
                info['totalCount'] + '\t' + info['year'] + '\n')

def Out2SQL(dict):
    conn = pyodbc.connect('Driver={SQL Server};Server='+ server +';Database='+ database +';UID='+ username +';PWD='+ password +';')
    cursor = conn.cursor()
    
    for info in dict:
        #print(info['Name'])
        cursor.execute("INSERT INTO [Orinsight_Db].[dbo].[MovieInfo] VALUES('" + info['yearRank'] + "','" + info['histRank'] + "',\
            '" + info['Name'] + "','" + info['peopleCount'] + "','" + info['totalCount'] + "','" + info['year'] + "')")

    conn.commit()

def main():
    page_number = 206
    #conn = pyodbc.connect('Driver={SQL Server};Server='+ server +';Database='+ database +';UID='+ username +';PWD='+ password +';')
    #cursor = conn.cursor()
    for i in range(page_number):
        print(i)
        url = base_url + '?page=' + str(i)
        #Out2File(i + 1, get_info(url, headers, cookies))
        Out2SQL(get_info(url, headers, cookies))

if __name__ == '__main__':
    main()
