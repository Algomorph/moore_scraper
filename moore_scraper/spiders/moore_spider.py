"""
Created on Mar 30, 2016
@author: Gregory Kramida

Copyrint 2016 Gregory Kramida

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from scrapy.spiders import Spider
from scrapy.http import Request
import re
import sys
from moore_scraper.items import Grant


class MooreSpider(Spider):
    """
    Spider used to crawl through the Fellowship Directory on the Packard Foundation website
    """
    name = "moore"
    allowed_domains = ["www.moore.org"]
    index = "https://www.moore.org"
    base_url = (index + "/grants")
    start_url = base_url

    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        super(MooreSpider, self).__init__(self, *args, **kwargs)

    def __del__(self):
        self.selenium.close()
        print(self.verificationErrors)
        Spider.__del__(self)

    # program entry point
    def start_requests(self):
        """
        @override
        called to construct requests from start url(s)
        """
        yield Request(url=MooreSpider.start_url,
                      callback=self.parse_directory_list,
                      method="GET")

    def parse_directory_list(self, response):
        has_next = \
            response.xpath("//div[@class='pagination margin-ten no-margin-bottom']" +
                           "/a/text()")[-1].extract() == 'Next'

        links = \
            response.xpath(
                "//ul[@class='grant-tiles filterSortGridView' or @class='grant-tiles filterSortGridView filterSortGridSwitchView']" +
                "//a[@class='button-white-teal btn btn-medium button " +
                "xs-margin-bottom-five']/@href").extract()
        links = [MooreSpider.index + link for link in links]
        if len(links) < 24:
            print("ALERT: !! Only {:d} links at {:s}".format(len(links), response.url))

        for link in links:
            if self.db.contains(link):
                match = re.match(r'.*=(.*)', link)
                grant_number = match.group(1)
                print("Grant {:s} is already in database".format(grant_number))
            else:
                yield Request(url=link, callback=self.parse_grant,
                              method="GET")

        if has_next:
            next_url = MooreSpider.base_url + \
                       response.xpath("//div[@class='pagination margin-ten " +
                                      "no-margin-bottom']/a/@href")[-1].extract()
            yield Request(url=next_url,
                          callback=self.parse_directory_list,
                          method="GET")

    def parse_grant(self, response):
        grant = Grant()
        grant["name"] = \
            response.xpath("//section[@class='grantee-list-banner grant-detail-" +
                           "banner fadeIn animated']//h3/text()")[0].extract()

        date_awarded = \
            response.xpath(
                "//div/span/text()[contains(.,'Date Awarded: ')]/../../../div[@class='right']/span/text()").extract()
        date_awarded = None if len(date_awarded) == 0 else date_awarded[0]

        amount = \
            response.xpath(
                "//div/span/text()[contains(.,'Amount: ')]/../../../div[@class='right']/span/text()").extract()
        amount = None if len(amount) == 0 else amount[0]

        term = \
            response.xpath("//div/span/text()[contains(.,'Term: ')]/../../../div[@class='right']/span/text()").extract()
        term = None if len(term) == 0 else term[0]

        grant_id = \
            response.xpath(
                "//div/span/text()[contains(.,'Grant ID: ')]/../../../div[@class='right']/span/text()").extract()
        grant_id = None if len(grant_id) == 0 else grant_id[0]

        funding_area = \
            response.xpath(
                "//div/span/text()[contains(.,'Funding Area: ')]/../../../div[@class='right']/span/text()").extract()
        funding_area = None if len(funding_area) == 0 else funding_area[0]

        organization = \
            response.xpath(
                "//section[@class='grantee-list-banner grant-detail-banner fadeIn animated']" +
                "//div[@class='bottom']/div[@class='left']/h4/a/text()").extract()
        organization = None if len(organization) == 0 else organization[0]

        grant["organization"] = organization
        grant["date_awarded"] = date_awarded
        grant["amount"] = amount
        grant["term"] = term
        grant["id"] = grant_id
        grant["funding_area"] = funding_area
        grant["url"] = response.url

        yield grant
