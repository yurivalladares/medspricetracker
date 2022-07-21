import json

import scrapy
from ..items import MedpricesItem


class DrogaRaiaSpider(scrapy.Spider):
    name = 'drogaraiaspider'
    store = 'droga_raia'

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

class DrogasilSpider(scrapy.Spider):
    name = 'drogasilspider'
    store = 'drogasil'

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
    }

    def start_requests(self):
        urls = [
            'https://www.drogasil.com.br/medicamentos.html?p=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items_list = response.css('div.products')


        for i in items_list:
            item = MedpricesItem()
            item['product_name'] = i.css("div.ProductCardNamestyles__ProductNameStyles-sc-1l5s4fj-0.cuGHOR.product-card-name a.LinkNextstyles__LinkNextStyles-t73o01-0.cpRdBZ.LinkNext::text").get()
            item['manufacturer'] = i.css("div.product-brand::text").get()
            item['product_url'] = i.css("div.ProductCardNamestyles__ProductNameStyles-sc-1l5s4fj-0.cuGHOR.product-card-name a.LinkNextstyles__LinkNextStyles-t73o01-0.cpRdBZ.LinkNext::attr(href)").get()
            item['price'] = i.css(".price-final .price::text").get()
            yield item

        next_page = response.css('li.itensPage.next a.ancor-class::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)

class DrogariaSaoPauloSpider(scrapy.Spider):
    name = 'saopaulospider'
    store = 'drogariasaopaulo'
    page = 1
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
    }
    url = "https://www.drogariasaopaulo.com.br/buscapagina?PS=48&sl=727d3c85-e93a-42fd-bd7e-42dfd3978c22&cc=48&sm=0&fq=C%3a%2f800%2f&PageNumber={}".format(page)
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):

        items_list = response.css('div.descricao-prateleira')
        if items_list is not None:
            for i in items_list:
                item = MedpricesItem()
                item['product_name'] = i.css("a.collection-link::text").get()
                item['manufacturer'] = ''
                item['product_url'] = i.css("a.collection-link::attr(href)").get()
                item['price'] = i.css("p.price a.valor-por span::text").get()
                yield item
            self.page += 1
            next_url = "https://www.drogariasaopaulo.com.br/buscapagina?PS=48&sl=727d3c85-e93a-42fd-bd7e-42dfd3978c22&cc=48&sm=0&fq=C%3a%2f800%2f&PageNumber={}".format(
                self.page)
            yield scrapy.Request(url=next_url, callback=self.parse)

class PagueMenosSpider(scrapy.Spider):
    name = 'paguemenosspider'
    store = 'paguemenos'
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
    }
    url = "https://www.paguemenos.com.br/_v/segment/graphql/v1?workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=pt-BR&__bindingId=23424e23-86bb-4397-98b0-238d88d7f528&operationName=productSearchV3&variables=%7B%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2267d0a6ef4d455f259737e4edb1ed58f6db9ff823570356ebc88ae7c5532c0866%22%2C%22sender%22%3A%22vtex.store-resources%400.x%22%2C%22provider%22%3A%22vtex.search-graphql%400.x%22%7D%2C%22variables%22%3A%22eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6ZmFsc2UsInNrdXNGaWx0ZXIiOiJBTExfQVZBSUxBQkxFIiwic2ltdWxhdGlvbkJlaGF2aW9yIjoiZGVmYXVsdCIsImluc3RhbGxtZW50Q3JpdGVyaWEiOiJNQVhfV0lUSE9VVF9JTlRFUkVTVCIsInByb2R1Y3RPcmlnaW5WdGV4IjpmYWxzZSwibWFwIjoiYyIsInF1ZXJ5IjoibWVkaWNhbWVudG9zLWUtc2F1ZGUiLCJvcmRlckJ5IjoiT3JkZXJCeVNjb3JlREVTQyIsImZyb20iOjQ4LCJ0byI6OTUsInNlbGVjdGVkRmFjZXRzIjpbeyJrZXkiOiJjIiwidmFsdWUiOiJtZWRpY2FtZW50b3MtZS1zYXVkZSJ9XSwib3BlcmF0b3IiOiJhbmQiLCJmdXp6eSI6IjAiLCJzZWFyY2hTdGF0ZSI6bnVsbCwiZmFjZXRzQmVoYXZpb3IiOiJTdGF0aWMiLCJjYXRlZ29yeVRyZWVCZWhhdmlvciI6ImRlZmF1bHQiLCJ3aXRoRmFjZXRzIjpmYWxzZX0%3D%22%7D"
    headers = {
        'Referer': 'https://www.paguemenos.com.br/medicamentos-e-saude'
    }
    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        data = response.json()
        items_list = data['data']['productSearch']['products']

        for i in items_list:
            item = MedpricesItem()
            item['product_name'] = i['productName']
            item['manufacturer'] = i['brand']
            item['product_url'] = 'https://www.paguemenos.com.br' + i['link']
            item['price'] = i['priceRange']['sellingPrice']['lowPrice']
            yield item

class PanvelSpider(scrapy.Spider):
    name = 'panvelspider'
    store = 'panvel'
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
    }

    url = 'https://www.panvel.com/api/v2/search/'

    payload = str({
        "term":"",
        "itemsPerPage":16,
        "currentPage":1,
        "assortment":"",
        "categoryId":35206,
        "filters":[{"name":"descricao_da_categoria_1","values":["medicamentos"]}],
        "searchType":"category"
    })
    body = {"term":"","itemsPerPage":16,"currentPage":5,"assortment":"","categoryId":35206,"filters":[{"name":"descricao_da_categoria_1","values":["medicamentos"]}],"searchType":"category"}
    headers = {
        'Host': 'www.panvel.com',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.panvel.com/panvel/medicamentos/c-35206',
        'Content-Length': '178',
        'Origin': 'https://www.panvel.com',
        'Connection': 'keep-alive',
        'Cookie': '__uzma=1e87b069-bd1e-48e5-9a1d-fe644c2aba1c; __uzmb=1657810293; __uzme=1581; __uzmc=179555816966; __uzmd=1658349545; RKT=false; _gcl_au=1.1.1462098345.1657810295; _pm_id=820001657810295052; _tt_enable_cookie=1; _ttp=5fd427c7-420d-471b-85a3-07579d3dc477; __ssds=2; __ssuzjsr2=a9be0cd8e; __uzmaj2=ed8e309e-aae9-4f7d-9501-489f241acd2e; __uzmbj2=1657810296; __uzmcj2=581136155472; __uzmdj2=1658349545; _ga=GA1.2.1079548759.1657810297; _fbp=fb.1.1657810296754.177085868; _clck=r25tkn|1|f3b|0; _hjSessionUser_261182=eyJpZCI6ImY1MzA3Njk1LTBiMGYtNWE3MC1hMmM3LThjZmQ0MzVhM2U2ZCIsImNyZWF0ZWQiOjE2NTc4MTAyOTczMzIsImV4aXN0aW5nIjp0cnVlfQ==; cto_bundle=uoRxwl9uODA5c0FtdDBxeUdUTiUyQmpJZkhPWmdkcTdxSFFteGEwRVUyQU1ZTG92U1VDeWVSY2o3V3JQWmJLYzlFU1BIMkpVbHpxWDBWbG42Sk9ldFFxT0huUkVwS3M0T0NLUjNkblZiMXZJdTQxTEtlWW5BTTE1SldqNHBpdkJrZFAybjdoUm9LbXl6YnRuJTJGZ0N5SGM4ZlJUc05RJTNEJTNE; chaordic_browserId=0-ulNJ_Lhi0srIO1WyTylGhqxkMYftrixaYJ5K16583485852361821; chaordic_anonymousUserId=anon-0-ulNJ_Lhi0srIO1WyTylGhqxkMYftrixaYJ5K16583485852361821; chaordic_session=1658348586265-0.9783635778878473; LojaVirtualPanvelCepExpired=true; chaordic_testGroup=%7B%22experiment%22%3Anull%2C%22group%22%3Anull%2C%22testCode%22%3Anull%2C%22code%22%3Anull%2C%22session%22%3Anull%7D; _pm_sid=981111658348587067; _gid=GA1.2.134784337.1658348587; _hjIncludedInSessionSample=0; _hjSession_261182=eyJpZCI6ImNkNDI4YmJlLTBkZTQtNDc4My05N2I5LWIyZWUxNTg1MDZlNSIsImNyZWF0ZWQiOjE2NTgzNDg1ODc4ODYsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; shoppingCartId=62d8642ce8b2637a00b9e01d; appName=search; _clsk=1v1rldj|1658349548633|11|0|f.clarity.ms/collect; voxusmediamanager_id=16578103008370.79983347031302425tnwk4ytvoo; ADRUM=s=1658349546253&r=https%3A%2F%2Fwww.panvel.com%2Fpanvel%2Fmedicamentos%2Fc-35206%3F-530585044; _uetsid=c671a640086911edac560fbe3ef8e4c6; _uetvid=74e78170038411ed9e4a4de8e8edd167; voxusmediamanager__ip=177.50.213.58',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
        'user-id': '8601417',
        'client-ip': '1',
        'app-token': 'ZYkPuDaVJEiD',
        'Content-Type': 'application/json',
        'ADRUM': 'isAjax:true',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    cookie = {
        __uzma=1e87b069-bd1e-48e5-9a1d-fe644c2aba1c; __uzmb=1657810293; __uzme=1581; __uzmc=179555816966; __uzmd=1658349545; RKT=false; _gcl_au=1.1.1462098345.1657810295; _pm_id=820001657810295052; _tt_enable_cookie=1; _ttp=5fd427c7-420d-471b-85a3-07579d3dc477; __ssds=2; __ssuzjsr2=a9be0cd8e; __uzmaj2=ed8e309e-aae9-4f7d-9501-489f241acd2e; __uzmbj2=1657810296; __uzmcj2=581136155472; __uzmdj2=1658349545; _ga=GA1.2.1079548759.1657810297; _fbp=fb.1.1657810296754.177085868; _clck=r25tkn|1|f3b|0; _hjSessionUser_261182=eyJpZCI6ImY1MzA3Njk1LTBiMGYtNWE3MC1hMmM3LThjZmQ0MzVhM2U2ZCIsImNyZWF0ZWQiOjE2NTc4MTAyOTczMzIsImV4aXN0aW5nIjp0cnVlfQ==; cto_bundle=uoRxwl9uODA5c0FtdDBxeUdUTiUyQmpJZkhPWmdkcTdxSFFteGEwRVUyQU1ZTG92U1VDeWVSY2o3V3JQWmJLYzlFU1BIMkpVbHpxWDBWbG42Sk9ldFFxT0huUkVwS3M0T0NLUjNkblZiMXZJdTQxTEtlWW5BTTE1SldqNHBpdkJrZFAybjdoUm9LbXl6YnRuJTJGZ0N5SGM4ZlJUc05RJTNEJTNE; chaordic_browserId=0-ulNJ_Lhi0srIO1WyTylGhqxkMYftrixaYJ5K16583485852361821; chaordic_anonymousUserId=anon-0-ulNJ_Lhi0srIO1WyTylGhqxkMYftrixaYJ5K16583485852361821; chaordic_session=1658348586265-0.9783635778878473; LojaVirtualPanvelCepExpired=true; chaordic_testGroup=%7B%22experiment%22%3Anull%2C%22group%22%3Anull%2C%22testCode%22%3Anull%2C%22code%22%3Anull%2C%22session%22%3Anull%7D; _pm_sid=981111658348587067; _gid=GA1.2.134784337.1658348587; _hjIncludedInSessionSample=0; _hjSession_261182=eyJpZCI6ImNkNDI4YmJlLTBkZTQtNDc4My05N2I5LWIyZWUxNTg1MDZlNSIsImNyZWF0ZWQiOjE2NTgzNDg1ODc4ODYsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; shoppingCartId=62d8642ce8b2637a00b9e01d; appName=search; _clsk=1v1rldj|1658349548633|11|0|f.clarity.ms/collect; voxusmediamanager_id=16578103008370.79983347031302425tnwk4ytvoo; ADRUM=s=1658349546253&r=https%3A%2F%2Fwww.panvel.com%2Fpanvel%2Fmedicamentos%2Fc-35206%3F-530585044; _uetsid=c671a640086911edac560fbe3ef8e4c6; _uetvid=74e78170038411ed9e4a4de8e8edd167;

    }
    def start_requests(self):
        yield scrapy.Request(url=self.url, method='POST', headers=self.headers, body=self.payload, callback=self.parse)

    def parse(self, response):
        data = response.json()
        items_list = data['items']

        for i in items_list:
            item = MedpricesItem()
            item['product_name'] = i['name']
            item['manufacturer'] = i['brandName']
            item['product_url'] = 'https://www.panvel.com' + i['link']
            item['price'] = i['discount']['dealPrice']['lowPrice']
            yield item

