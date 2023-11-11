import json
from pathlib import Path

from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail


class ItemDataContract(Contract):
    name = "item_data"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expected_data = None
        self.file_path = args[1]

    def adjust_request_args(self, args):
        with open(Path(__file__).resolve().parent / "spiders" / self.file_path) as f:
            self.expected_data = json.load(f)
        return args

    def post_process(self, output):
        if output != self.expected_data:
            raise ContractFail(f"Item does not match expected data: {self.expected_data}")


class ItemMetaDataPreprocessContract(Contract):
    name = "item_meta"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta_data = json.loads("".join(args[1:]))

    def pre_process(self, response):
        response.meta.update(self.meta_data)
        return response
