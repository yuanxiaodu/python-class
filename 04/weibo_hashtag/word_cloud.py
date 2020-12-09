import jieba
# jieba.enable_parallel(4)
import pandas
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import os
from imageio import imread
from os import path


# user_id_list代表我们要爬取的微博用户的user_id，可以是一个或多个，也可以是文件路径，微博用户Dear-迪丽热巴的user_id为1669879400，具体如何获取user_id见如何获取user_id；
# filter的值为1代表爬取全部原创微博，值为0代表爬取全部微博（原创+转发）；
# since_date代表我们要爬取since_date日期之后发布的微博，因为我要爬迪丽热巴的全部原创微博，所以since_date设置了一个非常早的值；
# write_mode代表结果文件的保存类型，我想要把结果写入csv文件和json文件，所以它的值为["csv", "json"]，如果你想写入数据库，具体设置见设置数据库；
# original_pic_download值为1代表下载原创微博中的图片，值为0代表不下载；
# retweet_pic_download值为1代表下载转发微博中的图片，值为0代表不下载；
# original_video_download值为1代表下载原创微博中的视频，值为0代表不下载；
# retweet_video_download值为1代表下载转发微博中的视频，值为0代表不下载；
# cookie是可选参数，可填可不填，具体区别见添加cookie与不添加cookie的区别。

# id,bid,正文,头条文章url,原始图片url,视频url,位置,日期,工具,点赞数,评论数,转发数,话题,@用户

def filter_tweets(filepath):
    tweets = pandas.read_csv(filepath)
    tweets = tweets[tweets['点赞数'] > 1]
    return tweets['正文'].tolist()


# The function for processing text with Jieba
def jieba_processing_txt(tweets):
    mywordlist = []
    with open(stopwords_path, encoding='utf-8') as f_stop:
        f_stop_text = f_stop.read()
        f_stop_seg_list = f_stop_text.splitlines()
    for tweet in tweets:
        seg_list = jieba.cut(tweet, cut_all=False)
        liststr = "/ ".join(seg_list)

        for myword in liststr.split('/'):
            if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
                mywordlist.append(myword)
    return ' '.join(mywordlist)


if __name__ == '__main__':
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    stopwords_path = d + '/wc_cn/stopwords_cn_en.txt'
    # Chinese fonts must be set
    # font_path = d + '/fonts/SourceHanSerif/SourceHanSerifK-Light.otf'
    font_path = d + '/fonts/SourceHanSerif/Hiragino Sans GB.ttc'

    # the path to save worldcloud
    imgname1 = d + '/wc_cn/LuXun.jpg'
    imgname2 = d + '/wc_cn/LuXun_colored.jpg'
    # read the mask / color image taken from
    back_coloring = imread(path.join(d, d + '/wc_cn/LuXun_color.jpg'))

    tweets = filter_tweets('weibo/#进击的巨人最终季#/#进击的巨人最终季#.csv')

    wc = WordCloud(font_path=font_path, background_color="white", max_words=2000, mask=back_coloring,
                   max_font_size=100, random_state=42, width=1000, height=860, margin=2, )

    wc.generate(jieba_processing_txt(tweets))

    # create coloring from image
    image_colors_default = ImageColorGenerator(back_coloring)

    plt.figure()
    # recolor wordcloud and show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    # save wordcloud
    wc.to_file(path.join(d, imgname1))

    # create coloring from image
    image_colors_byImg = ImageColorGenerator(back_coloring)

    # show
    # we could also give color_func=image_colors directly in the constructor
    plt.imshow(wc.recolor(color_func=image_colors_byImg), interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    plt.imshow(back_coloring, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    wc.to_file(path.join(d, imgname2))