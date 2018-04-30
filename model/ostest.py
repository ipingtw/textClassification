import os
import pandas as pd
project_file_path = os.path.dirname(os.path.abspath(__file__))
print(os.path.abspath(os.path.join(project_file_path,'../data/news_json'+str(1))))
'''
print(os.path.abspath(a))
b = os.path.join(a, '../x')
print(os.path.abspath(b))
c = os.path.join(a, './x')
print(os.path.abspath(c))
'''