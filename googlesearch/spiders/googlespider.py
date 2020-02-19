#from urlparse import urljoin, urlparse, parse_qsl
import urllib.parse
import datetime
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.misc import arg_to_iter
from googlesearch.items import GoogleSearchItem

COUNTRIES = {
    'ie': 'countryIE',
    'nl': 'countryNL'
}

"""
A spider to parse the google search result bootstraped from given queries.
"""
class GoogleSearchSpider(Spider):
    name = 'googlesearch'
    queries = ('contact us', 'hotel')
    region = 'ie'
    download_delay = 5
    base_url_fmt = 'http://www.google.{region}/search?hl=en&as_q=&as_epq={query}&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr={country}&as_qdr=all&as_sitesearch=&as_occt=any&safe=images&tbs=&as_filetype=&as_rights='
    download_html = False
    limit_country = False

    def start_requests(self):
        for query in arg_to_iter(self.queries):
            url = self.make_google_search_request(COUNTRIES[self.region], query)
            yield Request(url=url, meta={'query': query})

    def make_google_search_request(self, country, query):
        if not self.limit_country:
            country = ''
        return self.base_url_fmt.format(country=country, region=self.region, query='+'.join(query.split()).strip('+'))

    def parse(self, response):
        hxs = Selector(response)
        for sel in hxs.select('//div[@id="ires"]//li[@class="g"]//h3[@class="r"]'):
            name = u''.join(sel.select(".//text()").extract())
            url = _parse_url(sel.select('.//a/@href').extract()[0])
            region = _get_region(url)
            if len(url):
                if self.download_html:
                    yield Request(url=url, callback=self.parse_item, meta={'name':name,
                                                                           'query': response.meta['query']})
                else:
                    yield GoogleSearchItem(url=url, name=name, query=response.meta['query'], crawled=datetime.datetime.utcnow().isoformat())

        next_page = hxs.select('//table[@id="nav"]//td[contains(@class, "b") and position() = last()]/a')
        if next_page:
            url = self._build_absolute_url(response, next_page.select('.//@href').extract()[0])
            yield Request(url=url, callback=self.parse, meta={'query': response.meta['query']})

    def parse_item(self, response):
        name = response.meta['name']
        query = response.meta['query']
        url = response.url
        html = response.body[:1024 * 256]
        timestamp = datetime.datetime.utcnow().isoformat()
        yield GoogleSearchItem({'name': name,
                                'url': url,
                                'html': html,
                                'region': self.region,
                                'query': query,
                                'crawled': timestamp})

    def _build_absolute_url(self, response, url):
        return urljoin(get_base_url(response), url)

def _parse_url(href):
    """
    parse the website from anchor href.

    for example:

    >>> _parse_url(u'/url?q=http://www.getmore.com.hk/page18.php&sa=U&ei=Xmd_UdqBEtGy4AO254GIDg&ved=0CDQQFjAGODw&usg=AFQjCNH08dgfL10dJVCyQjfu_1DEyhiMHQ')
    u'http://www.getmore.com.hk/page18.php'
    """
    queries = dict(parse_qsl(urlparse(href).query))
    return queries.get('q', '')

def _get_region(url):
    """
    get country code from the url.

    >>> _get_region('http://scrapinghub.ie')
    'ie'
    >>> _get_region('http://www.astoncarpets.ie/contact.htm')
    'ie'
    """
    netloc = urlparse(url)[1]
    return netloc.rpartition('.')[-1]
