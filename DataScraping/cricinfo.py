import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import json
from scrapy.http import Request, FormRequest
from collections import namedtuple
import re

class CricInfoScrapeSpider(scrapy.Spider):
    name='cricinfo-spider'
    start_urls=['http://www.espncricinfo.com/ci/content/player/country.html?country=6;alpha=A']
    first_class_batting_stats=namedtuple("first_batting_stats", 'matches, inns, not_outs, runs, highest, average, balls_faced, strike_rate, hundreds, fifties, boundaries, sixes, catches_taken, stumpings_made')
    #self.numPages=10

    def parse(self, response):
        sel = Selector(text=response.body_as_unicode(), type="html")
        players_urlpath=sel.xpath(
            '//div[@id="ciPlayerbyCharAtoZ"]//ul//li//a/@href'
        )
        for url in players_urlpath.extract()[1:-1]:
            url = "http://www.espncricinfo.com" + url
            request = scrapy.Request(url, self.parse_player_names)
            yield request

    def parse_player_names(self,response):
        sel= Selector(text=response.body_as_unicode(), type="html")
        urlPath=sel.xpath(
            '//td[@class="ciPlayernames"]//a/@href'
        )

        for url in urlPath.extract()[1:20]:
            url = "http://www.espncricinfo.com" + url
            request = scrapy.Request(url, self.parse_player_details)
            request.meta['url']=url
            yield request

    def parse_player_details(self, response):
        sel = Selector(text=response.body_as_unicode(), type="html")
        name = sel.xpath(
            '//div[@class="ciPlayernametxt"]/div/h1/text()'
        )

        dob_place=sel.xpath(
            '//p[@class="ciPlayerinformationtxt"]/b[contains(text(), "Born")]/following-sibling::span/text()'
        )

        teams=sel.xpath(
            '//p[@class="ciPlayerinformationtxt"]/b[contains(text(), "Major teams")]/following-sibling::span/text()'
        )
        self.first_class_batting_stats.matches=sel.xpath(
            '//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[1]/td[2]/text()'
        )

        self.first_class_batting_stats.inns = sel.xpath(
            '//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[1]/td[3]/text()'
        )

        self.first_class_batting_stats.not_outs = sel.xpath(
            '//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[1]/td[4]/text()'
        )

        self.first_class_batting_stats.runs = sel.xpath(
            '//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[1]/td[5]/text()'
        )

        self.first_class_batting_stats.highest = sel.xpath(
            '//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[1]/td[6]/text()'
        )

        self.first_class_batting_stats.average = sel.xpath(
            '//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[1]/td[7]/text()'
        )

        self.first_class_batting_stats.balls_faced = sel.xpath(
            '//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[1]/td[8]/text()'
        )

        self.first_class_batting_stats.strike_rate = sel.xpath(
            '//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[1]/td[9]/text()'
        )

        self.first_class_batting_stats.hundreds = sel.xpath(
            '//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[1]/td[10]/text()'
        )

        self.first_class_batting_stats.fifties = sel.xpath(
            '//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[1]/td[11]/text()'
        )

        self.first_class_batting_stats.boundaries = sel.xpath(
            '//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[1]/td[12]/text()'
        )

        self.first_class_batting_stats.sixes = sel.xpath(
            '//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[1]/td[13]/text()'
        )

        self.first_class_batting_stats.catches_taken = sel.xpath(
            '//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[1]/td[14]/text()'
        )

        self.first_class_batting_stats.stumpings_made = sel.xpath(
            '//*[@id="ciHomeContentlhs"]/div[4]/table[1]/tbody/tr[1]/td[15]/text()'
        )

        json_stats={
            "matches": re.sub('\s+','',self.first_class_batting_stats.matches.extract()[0]),
            "inns":re.sub('\s+','',self.first_class_batting_stats.inns.extract()[0]),
            "not_outs":re.sub('\s+','',self.first_class_batting_stats.not_outs.extract()[0]),
            "runs":re.sub('\s+','',self.first_class_batting_stats.runs.extract()[0]),
            "highest":re.sub('\s+','',self.first_class_batting_stats.highest.extract()[0]),
            "average":re.sub('\s+','',self.first_class_batting_stats.average.extract()[0]),
            "balls_faced":re.sub('\s+','',self.first_class_batting_stats.balls_faced.extract()[0]),
            "strike_rate":re.sub('\s+','',self.first_class_batting_stats.strike_rate.extract()[0]),
            "hundreds":re.sub('\s+','',self.first_class_batting_stats.hundreds.extract()[0]),
            "fifties":re.sub('\s+','',self.first_class_batting_stats.fifties.extract()[0]),
            "boundaries":re.sub('\s+','',self.first_class_batting_stats.boundaries.extract()[0]),
            "sixes":re.sub('\s+','',self.first_class_batting_stats.sixes.extract()[0]),
            "catches_taken":re.sub('\s+','',self.first_class_batting_stats.catches_taken.extract()[0]),
            "stumps":re.sub('\s+','',self.first_class_batting_stats.stumpings_made.extract()[0])
        }

        yield {
            "name": name.extract()[0].replace('\n',''),
            "url": response.meta['url'].replace('\n',''),
            "born": dob_place.extract()[0].replace('\n',''),
            "teams": teams.extract()[0].replace('\n',''),
            "first_class": json_stats

        }

