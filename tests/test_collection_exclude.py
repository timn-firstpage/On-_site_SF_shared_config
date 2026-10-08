"""Check intended exclusions and retention of primary URLs, offline."""
import re
import unittest
from pathlib import Path


class CollectionExcludeTests(unittest.TestCase):
    def test_combinations_excluded_and_primary_urls_retained(self):
        assets = Path(__file__).resolve().parents[1] / 'assets' / 'sf-configs'
        rule = (assets / 'collection-combination-exclude.txt').read_text().strip()
        self.assertIn(rule.encode('ascii'), (assets / 'onsite-main-js.seospiderconfig').read_bytes())
        excluded = [
            'https://hk.gpbatteries.com/collections/power-bank/device_laptop+device_smartphone+product-line_powerbank',
            'https://another.example/collections/shoes/red%2Blarge?page=2',
            'http://shop.example/collections/shoes/red%2blarge/',
        ]
        retained = [
            'https://hk.gpbatteries.com/collections/power-bank',
            'https://shop.example/collections/power-bank/',
            'https://shop.example/collections/power-bank?page=2',
            'https://shop.example/collections/power-bank/device_laptop',
            'https://shop.example/collections/power-bank/device_laptop?page=2',
            'https://shop.example/products/item+name',
            'https://shop.example/collections/power-bank?q=red+large',
        ]
        for url in excluded:
            with self.subTest(url=url): self.assertIsNotNone(re.fullmatch(rule, url))
        for url in retained:
            with self.subTest(url=url): self.assertIsNone(re.fullmatch(rule, url))


if __name__ == '__main__':
    unittest.main()
