# Define your item pipelines here
#
import MySQLdb
from lxml.html import document_fromstring
from lxml.html.clean import Cleaner
from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb.cursors

class ScrapyGoogleSpiderPipeline(object):
    def __init__(self):
        self.cleaner = Cleaner(style=True, page_structure=False)
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='postal_address_corpus',
                                            user='root',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8',
                                            use_unicode=True)

    def process_item(self, item, spider):
        html = self.cleaner.clean_html(item.get('html', ''))
        doc = document_fromstring(html)
        item['text'] = self._normalize_text(doc.text_content())
        if spider.savedb:
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        tx.execute('SELECT * from page where url = "%s"' %item['url'])
        result = tx.fetchone()
        if result:
            log.msg("page %s already scraped.s" % item['url'], logLevel=log.INFO)
        else:
            tx.execute("insert into page(url, name, html, text, country, kw)"
                    "values (%s, %s, %s, %s, %s, %s)", (item.get('url'), item.get('name'),
                                                    item.get('html'), item.get('text'),
                                                    item.get('country'), item.get('kw')))
            log.msg("page %s store in db" % item.get('url'), logLevel=log.INFO)


    def _normalize_text(self, text):
        return " ".join(text.split())

    def handle_error(self, e):
        log.err(e)