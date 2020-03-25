import requests

# 1. requests的几种使用方法：
'''
import requests
r = requests.get('https://api.github.com/events')
r = requests.post('http://httpbin.org/post', data = {'key':'value'})
r = requests.put('http://httpbin.org/put', data = {'key':'value'})
r = requests.delete('http://httpbin.org/delete')
r = requests.head('http://httpbin.org/get')
r = requests.options('http://httpbin.org/get')
'''

# 2. 简单例子：爬取百度首页

def get_baidu():
    response = requests.get(url = 'https://www.baidu.com')
    response.encoding = 'utf-8'
    print(response) # <Response [200]>
    print(response.status_code) # 返回所有相应状态码: 200
    print(response.text) # 返回相应文本
    with open('baidu.txt', 'w', encoding='utf-8') as f:
        f.write(response.text)


# 3. GET请求头讲解
# (1) 请求头header使用
# 直接爬取会出错：
def requests_400():
    response = requests.get('https://www.zhihu.com/explore')
    print(response.status_code) # 400
    print(response.text) # 返回错误页面

def requests_add_header():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    response = requests.get(url = 'https://www.zhihu.com/explore', headers = headers) # 在get请求内添加user-agent的header
    with open('zhihu.txt', 'w', encoding='utf-8') as f:
        f.write(response.text)

# (2) params请求参数
# 某些网站URL过长，并且会有看不懂的字符串，需要用params进行参数替换
from urllib.parse import urlencode
# 以百度搜索“蔡徐坤”为例
# url = 'https://www.baidu.com/s?wd=%E8%94%A1%E5%BE%90%E5%9D%A4'

def parmas_method_one():
    url = 'https://www.baidu.com/s?' + urlencode({'wd': '蔡徐坤'})
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    response = requests.get(url, headers = headers)
    print(response.text)

def parmas_method_two():
    url = 'https://www.baidu.com/s?'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    response = requests.get(url, headers = headers, params={'wd': '蔡徐坤'}) # 在get方法中添加params参数
    print(url)
    print(response.text)
    with open('caixukun.txt', 'w', encoding='utf-8') as f:
        f.write(response.text)

# (3) cookies参数使用：
# 破解GitHub登录认证

def cookies_method_one():
    url = 'https://github.com/settings/emails'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        # 在headers中拼接cookies：
        'cookies': '_gh_sess=egG6mzIvbERRqovMTI7T45XuXZ3pej8CIKuik55E3NhqRscJfmS5HH4jFPpamfcuWvCgZmaj%2BS15UOMRcp60o34LJNA6JiXm%2BOeMsW4W3S9twp%2BN%2Bj%2BTfDDyGWSiy4IXdemIK5Wr1tWb%2FIPp%2F%2BY%2BVAb8YOPDxI0BW6PZ9RWdHR3bHwP8IVX8atgU9rXNBB%2Fo%2BB3RPiX%2FQMLh%2F4FwAzN5VFMsMmsHEeDOk9ntnVtpUX7vITrjhm%2B%2FwT1P70Gf4uEZ6lda%2FqvMELMe7AeHoC26sg%3D%3D--oE%2F4%2Fa1nSRH%2B2Vjx--AUwkUiCLxt%2F8pY5p9qp1rg%3D%3D; _octo=GH1.1.222392104.1583784566; logged_in=no; _ga=GA1.2.1910357256.1583784567; _gat=1; tz=America%2FChicago'
    }
    github_res = requests.get(url, headers = headers)
    print(github_res.text)

def cookies_method_two():
    url = 'https://github.com/settings/emails'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    }
    cookies = {
        'Cookie': '_gh_sess=egG6mzIvbERRqovMTI7T45XuXZ3pej8CIKuik55E3NhqRscJfmS5HH4jFPpamfcuWvCgZmaj%2BS15UOMRcp60o34LJNA6JiXm%2BOeMsW4W3S9twp%2BN%2Bj%2BTfDDyGWSiy4IXdemIK5Wr1tWb%2FIPp%2F%2BY%2BVAb8YOPDxI0BW6PZ9RWdHR3bHwP8IVX8atgU9rXNBB%2Fo%2BB3RPiX%2FQMLh%2F4FwAzN5VFMsMmsHEeDOk9ntnVtpUX7vITrjhm%2B%2FwT1P70Gf4uEZ6lda%2FqvMELMe7AeHoC26sg%3D%3D--oE%2F4%2Fa1nSRH%2B2Vjx--AUwkUiCLxt%2F8pY5p9qp1rg%3D%3D; _octo=GH1.1.222392104.1583784566; logged_in=no; _ga=GA1.2.1910357256.1583784567; _gat=1; tz=America%2FChicago'
    }
    github_res = requests.get(url, headers = headers, cookies = cookies)
    github_res1 = requests.get(url, headers = headers)
    print(github_res.text)
    print('--------------')
    print(github_res1.text)

cookies_method_two()

# 4. response属性
'''
print(response.status_code)  # 获取响应状态码
print(response.url)  # 获取url地址
print(response.text)  # 获取文本
print(response.content)  # 获取二进制流
print(response.headers)  # 获取页面请求头信息
print(response.history)  # 上一次跳转的地址
print(response.cookies)  # 获取cookies信息
print(response.cookies.get_dict())  # 获取cookies信息转换成字典
print(response.cookies.items())  # 获取cookies信息转换成字典
print(response.encoding)  # 字符编码
print(response.elapsed)  # 访问时间
'''

# 5. post请求(和get类似)
'''
(1)GET请求常用的操作：
    a. 在浏览器的地址栏中直接给出URL，那么就一定是GET请求
    b. 点击页面上的超链接也一定是GET请求
    c. 提交表单时，表单默认使用GET请求，但可以设置为POST
(2)POST请求
    a. 数据不会出现在地址栏中
    b. 数据的大小没有上限
    c. 有请求体
    d. 请求体中如果存在中文，会使用URL编码！
'''
# 步骤一：访问login获取authenticity_token
import re

login_url = 'https://github.com/login'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'Referer': 'https://github.com'
}
login_res = requests.get(login_url, headers = headers)
authenticity_token = re.findall('name = "authenticity_token" value = "(.*?)"', login_res.text, re.S)[0]
login_cookies = login_res.cookies.get_dict()

# 步骤二：携带token在请求体内往session发送post请求
session_url = 'https://github.com/session'
session_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'Referer': 'https://github.com/login'
}
form_data = {
    "commit": "Sign in",
    "utf8": "✓",
    "authenticity_token": authenticity_token,
    "login": "username",
    "password": "githubpassword",
    'webauthn-support': "supported" 
}

# 步骤三：测试是否登录
session_res = requests.post(
    session_url,
    data=form_data,
    cookies=login_cookies,
    headers=session_headers,
    # allow_redirects=False
)

session_cookies = session_res.cookies.get_dict()

url3 = 'https://github.com/settings/emails'
email_res = requests.get(url3, cookies=session_cookies)

print('账号' in email_res.text)

