import time
from pyquery import PyQuery as pq

# 1. 打开某个网站：
def baidu_resource():
    doc = pq('https://www.baidu.com') # doc = pq(url = 'https://www.baidu.com')
    print(doc)
    print(doc('head'))

html = '''<div>
    <ul id = 'haha'>
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul></div>'''

# 2. 基于CSS选择器查找：
'''
===============所有方法===================
    element是查找一个标签
    elements是查找所有标签

    (1) .class              .color              选择class="color"的所有元素
    (2) #id                 #info               选择id="info"的所有元素
    (3) *                   *                   选择所有元素
    (4) element             p                   选择所有的p元素
    (5) element,element     div,p               选择所有div元素和所有p元素
    (6) element element     div p               选择div标签内部的所有p元素
    (7) [attribute]         [target]            选择带有target属性的所有元素
    (8) [attribute=value]   [target=_blank]     选择target="_blank"的所有元素
'''
def search_from_css():
    doc = pq(html)
    print(doc('#haha .item-0 a span')) # id等于haha下面的class等于item-0下的a标签下的span标签（注意层级关系以空格隔开）
    item = doc('div ul')
    print(item) 
    print(item.parent()) # 父标签
    print(item.children()) # 子标签
    print(item.children('[class]')) # 子标签的class属性

def get_attribute():
    doc = pq(html)
    item = doc('.item-0 .active a')
    print(item.attr.href) # No.1
    print(item.attr('href')) # No.2

def tag_content():
    doc = pq(html)
    a = doc('a').text() # 找到所有a标签，连在一起打出
    print(a)


