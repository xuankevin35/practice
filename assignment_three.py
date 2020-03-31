import time
import pyodbc
import requests
from bs4 import BeautifulSoup
import re
import random
import json

info_sum = []
GetData_url = 'http://www.endata.com.cn/API/GetData.ashx'
base_url = 'http://www.endata.com.cn/BoxOffice/BO/Month/oneMonth.html'

server = '39.106.71.104'
database = 'Orinsight_Db'
username = 'orinsight'
password = 'ddsz#123'

startYear = ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
startMonth = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
startTime = []
for i in range(len(startYear)):
    for j in range(len(startMonth)):
        startTime.append(startYear[i] + '-' + startMonth[j] + '-01')
startTime.extend(['2020-01-01', '2020-02-01', '2020-03-01'])
IP_AGENTS = ["http://58.240.53.196:8080", "http://219.135.99.185:8088", "http://117.127.0.198:8080", "http://58.240.53.194:8080"]
proxies = {'http': random.choice(IP_AGENTS)}
Cookies = ''

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '53',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.endata.com.cn',
    'Origin': 'http://www.endata.com.cn',
    'Pragma': 'no-cache',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_info(url, number):
    data = {'startTime': startTime[number], 'MethodName': 'BoxOffice_GetMonthBox'}
    response = requests.post(url, data = data, headers = headers)#, proxies = proxies)

    json_info = json.loads(response.text)
    json_data = json_info['Data']
    json_table = json_data['Table']
    for i in range(len(json_table) - 1):
        for a, b in json_table[i].items():
            if not b:
                json_table[i][a] = 'NULL'
        info_sum.append(json_table[i])
    #return info

def Out2File(list):
    '''
    with open('info_sum.txt', 'w+', encoding= 'utf-8') as f:
        for info in list:
            f.write(info['MovieName'] + '\t' + str(info['Irank']) + '\t' +
                str(info['boxoffice']) + '\t' + str(info['box_pro']) + '\t' +
                str(info['avgboxoffice']) + '\t' + str(info['avgshowcount']) + '\t' +
                info['releaseTime'] + '\t' + str(info['days']) + '\n')'''
    
    for info in list:
        print("INSERT INTO [Orinsight_Db].[dbo].[MovieInfoNew] (Name, MonthRank, MonthBoxOffice,\
            MonthProportion, AvePrice, AvePeople, ReleaseDate, DaysInMonth) \
            VALUES('" + info['MovieName'] + "','" + str(info['Irank']) + "','" + str(info['boxoffice']) + "',\
            '" + str(info['box_pro']) + "','" + str(info['avgboxoffice']) + "','" + str(info['avgshowcount']) + "',\
            '" + info['releaseTime'] + "','" + str(info['days']) + "')")

def Out2SQL(list):   
    conn = pyodbc.connect('Driver={SQL Server};Server='+ server +';Database='+ database +';UID='+ username +';PWD='+ password +';')
    cursor = conn.cursor()

    num = 1
    for info in list:
        print('Population {} starts.'.format(num))
        query1 = "INSERT INTO [Orinsight_Db].[dbo].[MovieInfoNew] (Name"
        query2 = ")VALUES('" + info['MovieName']
        if info['Irank'] != 'NULL':
            query1 = query1 + ',MonthRank'
            query2 = query2 + "','" + str(info['Irank'])
        if info['boxoffice'] != 'NULL':
            query1 = query1 + ',MonthBoxOffice'
            query2 = query2 + "','" + str(info['boxoffice'])
        if info['box_pro'] != 'NULL':
            query1 = query1 + ',MonthProportion'
            query2 = query2 + "','" + str(info['box_pro'])
        if info['avgboxoffice'] != 'NULL':
            query1 = query1 + ',AvePrice'
            query2 = query2 + "','" + str(info['avgboxoffice'])
        if info['avgshowcount'] != 'NULL':
            query1 = query1 + ',AvePeople'
            query2 = query2 + "','" + str(info['avgshowcount'])
        if info['releaseTime'] != 'NULL':
            query1 = query1 + ',ReleaseDate'
            query2 = query2 + "','" + str(info['releaseTime'])
        if info['days'] != 'NULL':
            query1 = query1 + ',DaysInMonth'
            query2 = query2 + "','" + str(info['days'])

        #print(query1 + query2 + "')")
        cursor.execute(query1 + query2 + "')")
        num = num + 1
    conn.commit()
    
    print('ok')

def main():
    total_number = len(startTime)
    for i in range(total_number):
        print(i)
        get_info(GetData_url, i)
    #Out2File(info_sum)
    Out2SQL(info_sum)

if __name__ == '__main__':
    main()
