#import packages
import pandas as pd
import numpy as np
import jieba.posseg as pseg
import gc
project_file_path = os.path.dirname(os.path.abspath(__file__))

#import xml-parsed-to-json files
data1 = pd.read_json(os.path.join(project_file_path,'../data/news_json0.txt'))
data2 = pd.read_json(os.path.join(project_file_path,'../data/news_json1.txt'))
data3 = pd.read_json(os.path.join(project_file_path,'../data/news_json2.txt'))

#combine files
data = [data1, data2, data3]
data = pd.concat(data)
#delete separated files 
del data1, data2, data3
gc.collect()

#drop rows that contains na in any of the columns
data = data.dropna()
gc.collect()

#reset index
data.index = range(len(data.index))
#extract hostname from url
data['host'] = data['url'].str.split('/').str.get(2)
#extract category from hostname
data['category'] = data['host'].str.split('.').str.get(-3)

#select example with known categories
data = data[data['category'].isin(['auto','fund','bschool','business', 'it','health','sports','2008','2010','2012','travel','learning','yule'])]

#recategorization
data['cat'] = data['category'].map({
	'auto':'auto',
	'fund':'money',
	'bschool':'money',
	'business':'money',
	'it':'it',
	'health':'health',
	'sports':'sports',
	'2008':'sports',
	'2010':'sports',
	'2012':'sports',
	'travel':'travel',
	'learning':'learning',
	'yule':'entertaiment',
	})

data.dropna()
#save cleaned data
data.to_csv(os.path.join(project_file_path,'../data/news_cleaned.csv'), encoding = 'utf-8')

#create a new column which is the concatenation of content title and content
data['words'] = data[['contenttitle', 'content']].apply(lambda x: ''.join(x), axis=1)
#drop content title and content
data = data.drop(['contentitle, content'], axis = 1)
#stop word x
stop_flag = ['x']
#word segmentation
data['words'] = data['words'].apply(lambda x: [word.word for word in pseg.cut(x) if not(word.flag in stop_flag)])
#save dasta
data.to_csv(os.path.join(project_file_path,'../data/news_cleaned_text_new.csv'), encoding = 'utf-8')

'''
汽車 auto          auto
財經 money         fund bschool business
IT  it            it
健康 health        health 
體育 sports         sports 2008 2010 2012
旅遊 travel        travel
教育 learning      learning
娛樂 entertaiment  yule 



# of examples 1411996

missing value
missing_values_count = data.isnull().sum()
content        113840(8%)
contenttitle           1
docno                  0
url                    0
category               0
host                   0




data.loc[data['category'] == 'auto']

category  counts  chinese title
2008         842  olympic grame
2010         558  world cup
2012          31  olympic game
astro        360  星座
auto      138576  ?
baobao      2693  母嬰
book        6532  閱讀
bschool      230  商學院
business   27489  stock 很怪 money 財經
campus         2. 校園招聘
chihe        532  吃喝
club         349. ?
cul         1924. ?
dm            29. ?
expo2010       1. ?
fund        5015. 基金
games         42. ?
gd          1843. ??
goabroad    1106. 出國(留學)
gongyi       239  公益
green        521  綠色
health     23409. 健康
it        199871. 科技
korea        109. 韓娛
learning   13012. 教育
media        669. 傳媒
men         1094  男人
money      10616  ??
news       86052. fm0
roll      720957
s           8678  體育（播報）
sh          1298. 上海
sports     44536  體育
stock      52930. 股票
travel      2179  旅遊
tuan           1
tv          1643. 視頻(影片平台)
v              8
women       5882  女人
yule       50138. 娛樂



汽車 auto
財經 fund bschool business
IT.  IT
健康. health 
體育  sports 2008 2010 2012
旅遊. travel
教育. learning
娛樂. yule 


'''
