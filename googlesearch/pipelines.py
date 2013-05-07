# Define your item pipelines here
#
import MySQLdb
from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb.cursors

class ScrapyGoogleSpiderPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='corpus',
                                            user='root',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8',
                                            use_unicode=True)

    def process_item(self, item, spider):
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
            tx.execute("insert into page(url, name, html, region, query, crawled)"
                    "values (%s, %s, %s, %s, %s, %s)", (item.get('url'), item.get('name'),
                                                    item.get('html'), item.get('region'),
                                                    item.get('query'), item.get('crawled')))
            log.msg("page %s store in db" % item.get('url'), logLevel=log.INFO)

    def handle_error(self, e):
        log.err(e)