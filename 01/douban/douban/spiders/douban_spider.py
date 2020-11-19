import scrapy


class DoubanSpider(scrapy.Spider):
    # name = "douban"
    #
    # def start_requests(self):
    #     for i in range(10):
    #         url = F'https://movie.douban.com/subject/27592484/comments?start={20 * i}&limit=20&sort=new_score&status=P&percent_type='
    #         yield scrapy.Request(url=url, callback=self.parse)
    #
    # def parse(self, response):
    #     for comment in response.css('div.comment-item'):
    #         yield {
    #             'votes': comment.xpath('div[2]/h3/span[1]/span/text()').get(),
    #             'name': comment.xpath('div[2]/h3/span[2]/a/text()').get(),
    #             'seen': comment.xpath('div[2]/h3/span[2]/span[1]/text()').get(),
    #             'star': comment.xpath('div[2]/h3/span[2]/span[2]/@title').get(),
    #             'date': comment.xpath('div[2]/h3/span[2]/span[3]/@title').get(),
    #             'text': comment.xpath('div[2]/p/span/text()').get()
    #         }
    #     # next_page = response.css('a.next::attr("href")').get()
    #     # if next_page is not None:
    #     #     yield response.follow(next_page, self.parse)

    name = 'douban'
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'author': quote.xpath('span/small/text()').get(),
                'text': quote.css('span.text::text').get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
