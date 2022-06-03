import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    base_url = 'http://books.toscrape.com/'

    def parse(self, response):
        books_list = response.xpath('//article')

        for book in books_list:
            book_url = self.start_urls[0] + book.xpath('.//div[@class="image_container"]/a/@href').extract_first()
            yield scrapy.Request(book_url, callback=self.parse_book)

    def parse_book(self, response):
        title = response.xpath('//div/h1/text()').extract_first()
        relative_image = response.xpath('//div[@class="item active"]/img/@src').extract_first()
        final_image = self.base_url + relative_image.replace('../..' , '')
        price = response.xpath('//div[contains(@class, "product_main")]/p[@class="price_color"]/text()').extract_first()
        stock = response.xpath('//div[contains(@class, "product_main")]/p[contains(@class, "instock")]/text()').extract()[1].strip()
        rating = response.xpath('//div/p[contains(@class, "star-rating")]/@class').extract_first().replace('star-rating', '')
        upc = response.xpath('//table[@class="table table-striped"]/tr[1]/td/text()').extract_first()
        price_exc_tax = response.xpath('//table[@class="table table-striped"]/tr[3]/td/text()').extract_first()
        price_inc_tax = response.xpath('//table[@class="table table-striped"]/tr[4]/td/text()').extract_first()
        print(upc)
        yield {
            'title': title,
            'image':relative_image,
            'price':price,
            'stock':stock,
            'rating':rating,
            'upc':upc,
            'price_exc_tax':price_exc_tax,
            'price_inc_tax':price_inc_tax,
            }
# OLD            
#            title = book.xpath('.//h3/a/@title').extract_first()
#            price = book.xpath('.//div[@class="product_price"]/p[@class="price_color"]/text()').extract_first()  
#            image_url = self.start_urls[0] + book.xpath('.//a/img/@src').extract_first()
#            yield {
#                'title': title,
#                'price': price,
#                'image_url': image_url,
#                'book_url': book_url,
#                }
#To save output into a file, in the console type scrapy crawl spider -o books.csv