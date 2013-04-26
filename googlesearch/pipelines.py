# Define your item pipelines here
#
from lxml.html import document_fromstring
from lxml.html.clean import Cleaner


class ScrapyGoogleSpiderPipeline(object):
    def __init__(self):
        self.cleaner = Cleaner(style=True, page_structure=False)

    def process_item(self, item, spider):
        html = self.cleaner.clean_html(item.get('body', ''))
        doc = document_fromstring(html)
        item['text'] = self._normalize_text(doc.text_content())
        return item

    def _normalize_text(self, text):
        return " ".join(text.split())
