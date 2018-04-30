#import packages
import pandas as pd
import numpy as np
import ast
import gc
project_file_path = os.path.dirname(os.path.abspath(__file__))

#import data
data = pd.read_csv(os.path.join(project_file_path,'../data/news_cleaned_text.csv'))
#select columns that we need: cat is the label, words is the content, ie. features
data = data[['cat','words']]
#drop na
data = data.dropna()
gc.collect()

#sampling from each category 2000 samples
data = data.groupby('cat').apply(lambda x: x.sample(2000))
gc.collect()

#concatenate words into string, delimited by blank spaces
data['words'] = data['words'].apply(lambda x: ' '.join(ast.literal_eval(x)[0:100]))
data = data[['cat','words']]
data = data.dropna()
gc.collect()

print(data.shape)

#map cat into integer categories
data['cat_int'] = data['cat'].map({
	'auto':1,
	'money':2,
	'it':3,
	'health':4,
	'sports':5,
	'travel':6,
	'learning':7,
	'entertaiment':8})

#save data
data.to_csv(os.path.join(project_file_path,'../data/news_final_sample.csv'), encoding = 'utf-8')


