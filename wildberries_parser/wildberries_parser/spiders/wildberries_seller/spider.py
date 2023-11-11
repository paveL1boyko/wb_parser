import scrapy
from scrapy.http import Response

from .parser import WildberriesSellerParser


class WildberriesBrandParser(scrapy.Spider):
    name = "wildberries_seller"
    allowed_domains = ["wildberries.ru", "static-basket-01.wb.ru"]

    start_link = "https://www.wildberries.ru/webapi/seller/data/short/{}"
    seller_logo_link = "https://static-basket-01.wb.ru/vol1/crm-bnrs/shops/{}_logo.webp"

    def start_requests(self):
        start_seller_id = 1
        yield scrapy.Request(
            self.start_link.format(1),
            callback=self.parse,
            meta={"seller_id": start_seller_id},
        )

    def parse(self, response: Response, **kwargs):
        response_meta = response.meta
        seller_id = response_meta["seller_id"]
        while True:
            seller_id += 1
            response_meta["seller_id"] = seller_id
            yield scrapy.Request(
                self.start_link.format(seller_id),
                callback=self.parse_seller,
                errback=self.errback_seller,
                meta=response_meta,
            )

    def parse_seller(self, response):
        """
        @url https://www.wildberries.ru/webapi/seller/data/short/1
        @returns requests 1 1
        @item_meta {"seller_id": 2}
        """
        seller_id = response.meta["seller_id"]
        data = response.json()
        if data.get("isUnknown") is False:
            data["seller_link"] = response.url
            yield scrapy.Request(
                self.seller_logo_link.format(seller_id),
                callback=self.parse_seller_with_logo,
                errback=self.errback_logo,
                meta={"seller_data": data},
            )

    def parse_seller_with_logo(self, response):
        """
        @url https://www.wildberries.ru/webapi/seller/data/short/56538
        @returns items 1 1
        @item_data wildberries_seller/tests/result_2.json
        @item_meta {"seller_data":{"id":56538,"name":"ООО ТК АЗУР","fineName":"ТК АЗУР","ogrn":"1116674010310","trademark":"ТК Азур","legalAddress":"620146, Свердловская обл., г. Екатеринбург, ул. Волгоградская, д.178, офис 14","isUnknown":false}}
        """
        seller_data = response.meta["seller_data"]
        seller_data["seller_logo_link"] = response.url
        yield WildberriesSellerParser.parse_seller(seller_data)

    def errback_seller(self, failure):
        if failure.value.response.status == 404:
            self.crawler.engine.close_spider(self, "Seller not found, stopping spider.")

    def errback_logo(self, failure):
        self.logger.error(f'Logo not found for seller {failure.request.meta["seller_data"]["id"]}')
        yield WildberriesSellerParser.parse_seller(failure.value.response.meta["seller_data"])
