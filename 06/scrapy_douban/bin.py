from scrapy import cmdline

cmdline.execute(
    'scrapy crawl movie_comment -o movie_comments.csv -a id=27073752 -a start=1 -a end=-1 -a sort=new_score'.split(
        ' '))
