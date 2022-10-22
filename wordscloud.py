#coding:utf-8
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import jieba
import numpy as np

'''使用函数一键生成词云'''    
def wordcloud_show(text,color_mask_path, font_path= '方正粗黑宋简体.ttf'):
    # 设置停用词并储存在stopwords列表中
    with open('stopwords.txt','r',encoding='utf-8') as file:
        stopwords = file.read().split('\n')

    # 分词(使用lcut命令得到词语列表)
    words = jieba.lcut(text, cut_all=False)
    
    # 去除停用词
    newword = []
    for word in words:
        if word not in stopwords:
            newword.append(word)
    mytext = ' '.join(newword)
    # 设置底图格式
    color_mask = np.array(Image.open(color_mask_path))
    # 设置词云参数
    wordcloud = WordCloud(
        background_color='white',
        mask= color_mask,
        font_path = font_path,
        max_words= 3000,        
        random_state=42,
        scale=2,
        color_func= None,
        prefer_horizontal=0.9).generate(mytext)
    image_colors = image_colors = ImageColorGenerator(color_mask)
    
    # 展示词云图
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
