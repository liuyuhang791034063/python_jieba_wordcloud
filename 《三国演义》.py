#encoding=utf-8

import requests
from os import path
import re
from bs4 import BeautifulSoup
from collections import Counter
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from scipy.misc import imread

#这里是爬虫 其中失败了两个章节
'''url = 'https://www.ybdu.com/xiaoshuo/2/2746/'
head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
file = open('test.txt','w')

html = requests.get(url,params=head)
html.encoding='gbk'
wenzhang_select = re.compile(r'<ul class="mulu_list">(.*?)</ul>',re.S)
wenzhang = wenzhang_select.search(html.text)
"""soup = BeautifulSoup(html,"html.parser")
list_old = soup.find(class_= "mulu_list")
list_new = list_old.find_all('li')"""
select = re.compile(r'<li>(.+?)</li>')
list_new = select.findall(wenzhang[0])
for i in list_new:
    id_select = re.compile(r'<a href="(.*?)">(.*?)</a>')
    one_url = url + id_select.findall(i)[0][0]
    one_html = requests.get(one_url,params=head)
    one_html.encoding = 'gbk'
    soup = BeautifulSoup(one_html.text,"html.parser")
    try:
        file.write(soup.find(class_ = 'h1title').h1.text + '\n')
    except BaseException:
        print('Sorry1')
    try:
        file.write((soup.find(class_ = 'contentbox').text.split('\n')[1].replace('    ','\n')) + '\n')
    except BaseException:
        print('Sorry2')
file.close()'''

#top n的词
text_read = open('test.txt').read()
jieba.load_userdict('test_dic.txt')
c = jieba.cut(text_read, cut_all=False, HMM=True)
word_list = []
for i in c:
    word_list.append(i)
word_dic = {}
for i in word_list:
    if i not in word_dic:
        word_dic[i] = 1
    else :
        word_dic[i] += 1
over_list = sorted(word_dic.items(), key = lambda x : x[1], reverse=True)

font_path = "D:\Fonts\simkai.ttf"#字体路径
dizi_path = "D:\dizi.jpg"#底子图片路径

back_coloring = imread(dizi_path)

wc = WordCloud(background_color="white", #背景颜色
               font_path=font_path, #字体选择
               max_words=1000, #最大词数
               mask=back_coloring ,#背景图片
               max_font_size=100, #最大字体大小
               width=1000, height=860, margin=2)

wc.fit_words(dict(over_list[20:]))

plt.figure()
#显示图片
plt.imshow(wc)
plt.axis("off")
plt.show()
#保存图片
wc.to_file(path.join(path.dirname(__file__), 'wordcloud1.png'))
#改变颜色
image_color = ImageColorGenerator(back_coloring)
plt.imshow(wc.recolor(color_func=image_color))
plt.axis('off')
#绘制背景颜色的词云
plt.figure()
plt.imshow(back_coloring, cmap = plt.cm.gray)
plt.axis('off')
plt.show()
wc.to_file(path.join(path.dirname(__file__), 'wordcloud2.png'))

