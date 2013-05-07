from urllib import urlencode
from urlparse import urljoin, urlparse, parse_qsl
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.utils.response import get_base_url
from googlesearch.items import GoogleSearchItem

_COUNTRIES = {
    'ie': 'countryIE'
}

"""
A spider to parse the google search result.
"""
class GoogleSearchSpider(BaseSpider):
    name = 'googlesearch'
    kws = ('contact us',)
    region = 'ie'
    savedb = True
    download_delay = 5
    base_url_fmt = 'http://www.google.{region}/search?hl=en&as_q=&as_epq={query}&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr={country}&as_qdr=all&as_sitesearch={region}&as_occt=any&safe=images&tbs=&as_filetype=&as_rights='

    def start_requests(self):
        for kw in self.kws:
            url = self.make_google_search_request(_COUNTRIES[self.region], kw)
            yield Request(url=url, meta={'kw': kw})

    def make_google_search_request(self, country, query):
        return self.base_url_fmt.format(country=country, region=self.region, query='+'.join(query.split()).strip('+'))

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        for sel in hxs.select('//div[@id="ires"]//li[@class="g"]//h3[@class="r"]'):
            name = u''.join(sel.select(".//text()").extract())
            url = _parse_url(sel.select('.//a/@href').extract()[0])
            region = _get_region(url)
            if region == self.region and len(url):
                yield Request(url=url, callback=self.parse_item, meta={'name':name,
                                                                       'kw': response.meta['kw']})

        next_page = hxs.select('//table[@id="nav"]//td[@class="b" and position() = last()]/a')
        if next_page:
            url = self._build_absolute_url(response, next_page.select('.//@href').extract()[0])
            yield Request(url=url, callback=self.parse, meta={'kw': response.meta['kw']})

    def parse_item(self, response):
        name = response.meta['name']
        kw = response.meta['kw']
        url = response.url
        html = response.body[:1024 * 256]
        yield GoogleSearchItem({'name': name,
                                'url': url,
                                'html': html,
                                'country': self.region,
                                'kw': kw})

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
