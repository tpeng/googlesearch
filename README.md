## Googlesearch
Scrape the google advanced search result with scrapy bootstraped from given queries. This spider can be used to collect the
HTML pages to prepare for a corpus.

## Usage
`scrapy crawl googlesearch -a queries='xxx'` -a region='xxx' replace the 'xxx' to the keywords you want search with Google
and the region (e.g. ie for Ireland) you wish to limit to.