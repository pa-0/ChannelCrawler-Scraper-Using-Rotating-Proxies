# -*- coding: utf-8 -*-
import scrapy

class ChannelSpider(scrapy.Spider):
    name = 'channel'
    allowed_domains = ['channelcrawler.com']
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://channelcrawler.com/eng/results/136614",
            callback=self.parse
        )
    ################################################
    #                                              #
    #       NEED TO START FROM 1046                #
    #                                              #
    ################################################
    def parse(self, response):
        row = response.xpath("//div[contains(@class,'channel')]")
        for each_row in row:
            yield {
                'Channel Name':each_row.xpath('.//h4/a/text()').get(),
                'Category':each_row.xpath('.//h4/following-sibling::small/b/text()').get(),
                'Subscriber':(each_row.xpath('normalize-space(.//p[1]/small/text()[1])').get().split(' '))[0],
                'Total videos':(each_row.xpath('normalize-space(.//p[1]/small/text()[2])').get().split(' '))[0],
                'Total Views':(each_row.xpath('normalize-space(.//p[1]/small/text()[3])').get().split(' '))[0],
                'Join Date':(each_row.xpath('normalize-space(.//p[1]/small/text()[4])').get().split(':'))[1],
                'Country':each_row.xpath('.//h4/img/@title').get()
            }
        next_page = response.xpath('//ul[@class="pagination"]/li[@class="next"]/a/@href').get()
        if next_page:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(next_page_link,
                   callback=self.parse
                )