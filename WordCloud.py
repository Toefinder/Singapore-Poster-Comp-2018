from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
from os import path, getcwd

name = "B2205000.xlsx"
df = pd.read_excel(name, sheet_name='Sheet1')
text=""
d = getcwd()
trump_mask = np.array(Image.open(path.join(d, "Trump.png")))

for index, row in df.iterrows():
    number = row['Numbers']
    for x in range(number):
        text += (" "+str(row['Words']))

wordcloud = WordCloud(background_color="rgba(255, 255, 255, 0)", mode="RGBA",
                         max_words= 1000, mask=trump_mask
                         ).generate(text)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.figure()
plt.imshow(trump_mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")
plt.show()
fig = plt.gcf()
fig.set_size_inches(11.69, 16.53)
name2 = "WordCloud.png"
plt.savefig(name2)