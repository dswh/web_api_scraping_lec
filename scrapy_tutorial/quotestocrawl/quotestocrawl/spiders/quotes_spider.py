import scrapy


class QuotesSpider(scrapy.Spider):
    """
    must return an iterable of requests which the spider
    will begin to crawl
    """

    name = "quotes"

    def start_requests(self):
        """
        must return an iterable of requests which the spider
        will begin to crawl
        """
        urls = [
            "http://quotes.toscrape.com/page/1/"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            text = quote.css("span.text::text").get()
            author = quote.css("small.author::text").get()
            tags = quote.css("div.tags a.tag::text").getall()
            yield dict(text=text, author=author, tags=tags)

          # checking for the next page availability.
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

