from scrapy.spiders import SitemapSpider
from scrapy.utils.sitemap import Sitemap
import requests
import scrapy

class reweRecipes(SitemapSpider):
    name="rewe"
    sitemap_urls = ["https://www.rewe.de/sitemaps/sitemap-rezepte.xml"]

    def parse(self, response):
        print(response.url)
        recipe_schema = response.xpath('//*[@id="recipe-schema"]/text()').get()
        yield {
            "url": response.url,
            "recipe_schema": recipe_schema,
        }