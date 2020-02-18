## Googlesearch
Scrape the google advanced search result with scrapy bootstraped from given queries. This spider can be used to collect the
HTML pages to prepare for a corpus.

## Usage
`scrapy crawl googlesearch -a queries='xxx'` -a region='xxx' replace the 'xxx' to the keywords you want search with Google
and the region (e.g. ie for Ireland) you wish to limit to.


## Note from 2020
This code hadn't been touched for 7 years. 
I tried it because I read https://www.reddit.com/r/Python/comments/8wtrdk/sometime_you_get_lucky_and_find_the_right_google/

TL;DR: *It does not work for me*
Also I'm told it uses many old ways of doing things (e.g. .select instead of .xpath)

Anyway, perhaps https://github.com/ivankliuk/duckduckpy is a better approach.

