# Scrapy settings for scrapy_google_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'googlesearch'

SPIDER_MODULES = ['googlesearch.spiders']
NEWSPIDER_MODULE = 'googlesearch.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'googlesearch (+http://www.yourdomain.com)'

ITEM_PIPELINES = ['googlesearch.pipelines.ScrapyGoogleSpiderPipeline']
