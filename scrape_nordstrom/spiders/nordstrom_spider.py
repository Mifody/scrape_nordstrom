# -*- coding: utf-8 -*-
'''
SPIDER
'''
import scrapy
import urlparse

from scrape_nordstrom.items import Product

from scrape_nordstrom.utils import xcontains, xtract
from scrape_nordstrom.transforms import add_field, to_float, transform_initial_data


class NordstromSpider(scrapy.Spider):
    '''
    SPIDER
    '''
    name = 'nordstrom'
    allowed_domains = ['nordstrom.com', 'shop.nordstrom.com/', 'http://shop.nordstrom.com/']
    start_urls = ['http://shop.nordstrom.com/c/sitemap', 'http://shop.nordstrom.com/c/brands-list']

    def parse(self, response):
        links = response.xpath("//a[contains(@href, '/c/')]/@href")
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

            yield scrapy.Request(product_url, callback=self.parse_product)

    # pagination_pattern = "//div[@class='fashion-results-pager']/ul/li/a[@class='standard']/@href"
    # page_urls = response.xpath(pagination_pattern).extract()
    # for page_url in page_urls:
    #   yield scrapy.Request(url = page_url, callback = self.parse_products_page)

    def parse_product(self, response):
        product = Product()

        product['url'] = response.url

        # NAME
        name = xtract(response, "//h1/text()")
        add_field(product, 'name', name)

        # ITEM NUM
        item_num = xtract(response, xcontains('span', 'style-number'))
        add_field(product, 'item_num', item_num, lambda x: x.split('#')[-1].strip())

        # PRICE
        price = xtract(response, xcontains('span', 'price-current'))
        if len(price) == 0:
            price = xtract(response, xcontains('span', 'regular-price'))

        add_field(product, 'price', price, to_float)

        data_script = response.xpath("//script[contains(., 'initialData')]/text()").extract()
        if len(data_script) > 0:
            product['data_script'] = transform_initial_data(data_script[0])

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
        if len(old_product_id) > 0:
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
