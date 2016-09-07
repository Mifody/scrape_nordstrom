# -*- coding: utf-8 -*-
'''
SPIDER
'''
import scrapy

from scrape_nordstrom.items import Product

#from pprint import pprint
import urlparse
import logging

from scrape_nordstrom.utils import xcontains, xtract, to_float

class NordstromSpider(scrapy.Spider):
    '''
    SPIDER
    '''
    name = 'nordstrom'
    allowed_domains = ['nordstrom.com', 'shop.nordstrom.com/', 'http://shop.nordstrom.com/']
    start_urls = ['http://shop.nordstrom.com/c/sitemap', 'http://shop.nordstrom.com/c/brands-list']

    def parse(self, response):
        #category_links = response.xpath("//div[@class='column']/ul/li/a/@href").extract()
        links = response.xpath("//a[contains(@href, '/c/')]/@href")
        # http://stackoverflow.com/questions/6499603/
        #   python-scrapy-convert-relative-paths-to-absolute-paths
        for href in links:
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_products_page)

    def parse_products_page(self, response):
        product_page_pattern = "//p[@class='product-title']/a/@href"
        product_urls = response.xpath(product_page_pattern)
        # self.log(pprint(product_urls))
        for href in product_urls:
            base_product = href.extract().split('?')[0]
            product_url = urlparse.urljoin(response.url, base_product)

            # self.log("------------" + product_url, level=log.DEBUG)
            yield scrapy.Request(url = product_url, callback = self.parse_product)

    # pagination_pattern = "//div[@class='fashion-results-pager']/ul/li/a[@class='standard']/@href"
    # page_urls = response.xpath(pagination_pattern).extract()
    # for page_url in page_urls:
    #   yield scrapy.Request(url = page_url, callback = self.parse_products_page)

    def parse_product(self, response):
        product = Product()

        product['url'] = response.url

        # NAME
        name = xtract(response, "//h1/text()")
        if len(name) > 0:
            product['name'] = name[0]
        else:
            product['name'] = None

        # ITEM NUM
        # item_num = response.xpath("//span[contains(@class, 'style-number')]/text()").extract()
        item_num = xtract(response, xcontains('span', 'style-number'))
        if len(item_num) > 0:
            product['item_num'] = item_num[0].split('#')[-1].strip()
        else:
            product['item_num'] = None

        # PRICE
        # price = response("//span[contains(@class, )]")
        # price = response.xpath(xcontains('span', 'price-current')).extract()
        price = xtract(response, xcontains('span', 'price-current'))
        if len(price) == 0:
            # price = response.xpath(xcontains('span', 'regular-price')).extract()
            price = xtract(response, xcontains('span', 'regular-price'))

        if len(price) > 0:
            product['price'] = price[0]
        else:
            product['price'] = None

        data_script = response.xpath("//script[contains(., 'initialData')]/text()").extract()

        if len(data_script) > 0:
            product['data_script'] = data_script[0]

        yield product


    def parse_item_old(self, response):
        item = Product()
        title = response.xpath("//section[@id='product-title']/h1/text()").extract()
        if len(title) == 0:
            title = response.xpath("//h1/text()").extract()

        item['product_title'] = title[0]
        new_product_id = response.xpath("//div[@class='item-number-wrapper']/text()").extract()
        if len(new_product_id) > 0:
            item['product_id'] = new_product_id[0].split("#")[1].strip()
        else:
            old_product_id = response.xpath("//td[@class='item-number']/text()").extract()
        if(len(old_product_id) > 0):
            old_product_id = old_product_id[0].split("#")[1].strip()
            item['product_id'] = old_product_id

        item['brand'] = response.xpath("//section[@id='brand-title']/h2/a/text()").extract()
        if len(item['brand']) > 0:
            item['brand'] = item['brand'][0]

        sale_price = response.xpath("//span[contains(@class,'sale-price')]/text()").extract()
        if len(sale_price) > 0:
            sale_price = sale_price[0].replace("$","")
            sale_price = sale_price.split(":")[1].strip()
            item['price_sale'] = float(sale_price)

        price = response.xpath("//td[contains(@class,'item-price')]/span/text()").extract()
        if len(price) == 0:
            price = 0.0
        else:
            price = price[0]

        price = price.strip().replace("$","")
        price = price.replace(",","").strip()
        if "-" in price:
            prices = price.split("-")
            item['price_low'] = float(prices[0].strip())
            item['price_high'] = float(prices[1].strip())
        else:
            if ":" in price:
                price = price.split(":")[1]
        price = price.strip()
        if not price:
            price = 0.0
        item['price'] = float(price)

        breadcrumbs = response.xpath("//nav[@id='breadcrumb-nav']/ul/li/a/text()").extract()
        category = response.xpath("//nav[@id='breadcrumb-nav']/ul/li/text()").extract()
        breadcrumbs = breadcrumbs + category
        item['category'] = category[0]
        item['breadcrumbs'] = "-".join(breadcrumbs)
        item['product_url'] = response.url.split("?")[0]

        return item
