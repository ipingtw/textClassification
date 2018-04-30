import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns	

project_file_path = os.path.dirname(os.path.abspath(__file__))

data = pd.read_csv(os.path.join(project_file_path,'../data/news_cleaned.csv'))

plt.figure(figsize=(10, 6))
uniques, counts= np.unique(data['cat'], return_counts=True)
print(counts)
cols = ['ip', 'app', 'device', 'os', 'channel']
sns.set(font_scale=1.2)
ax = sns.barplot(uniques, counts, log=True)
ax.set(xlabel='topic', ylabel='count', title='number of articles for each category)')
for p, uniq in zip(ax.patches, uniques):
    height = p.get_height()
    ax.text(p.get_x()+p.get_width()/2.,
            height + 10,
            height,
            ha="center") 
plt.savefig(os.path.join(project_file_path,'../data/output.png'))

plt.gcf().clear()

sns.set_style("darkgrid")



data['content_len'] = data['content'].str.len()

uniques, counts= np.unique(data['content_len'], return_counts=True)
plt.plot(uniques, counts)

#ax = sns.distplot(data['content_len'], bins =10, kde=False)

plt.savefig(os.path.join(project_file_path,'../data/hist.png'))

