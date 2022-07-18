import scrapy
from ..items import MedpricesItem


class DrogaRaiaSpider(scrapy.Spider):
    name = 'drogaraiaspider'
    store = 'Droga Raia'

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
    }

    def start_requests(self):
        urls = [
            'https://www.drogaraia.com.br/medicamentos.html?p=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items_list = response.css('li.item.last')


        for i in items_list:
            item = MedpricesItem()
            item['product_name'] = i.css("div.product-name a.show-hover::text").get()
            item['manufacturer'] = i.css("li.marca.hide-hover::text").get()
            item['product_url'] = i.css("div.product-name a.show-hover::attr(href)").get()
            item['store'] = self.store


            if i.css("span.lmpm-price-text::text").get():
                item["price"] = i.css("span.lmpm-price-text::text")[-1].get()
            elif i.css('span.regular-price::text').get():
                item["price"] = i.css('span.regular-price span::text')[-1].get()
            else:
                item["price"] = i.css("p.special-price span.price span::text")[-1].get()
            yield item

        next_page = response.css('a.next.i-next.btn-more::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)