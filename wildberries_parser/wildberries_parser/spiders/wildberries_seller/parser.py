# parser.py
from wildberries_parser.items import WildberriesSellerItem


class WildberriesSellerParser:
    @staticmethod
    def parse_seller(seller: dict):
        item = WildberriesSellerItem()
        item["name"] = seller.get("name")
        item["seller_link"] = f'https://www.wildberries.ru/seller/{seller["id"]}'
        item["seller_logo_link"] = seller.get("seller_logo_link")
        item["ogrn"] = seller.get("ogrn") or seller.get("ogrnip")
        return item
