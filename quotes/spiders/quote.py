from scrapy.selector import Selector
import scrapy


class QuoteSpider(scrapy.Spider):
    name = 'login'

    def start_requests(self):
        yield scrapy.Request(
            "https://www.stealmylogin.com/demo.html",
            meta = {
                "playwright": True,
                "playwright_include_page": True
            }
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]

        await page.fill("input[name=username]", "random")
        await page.fill("input[name=password]", "random")

        await page.click("input[type=submit]")

        html_content = await page.inner_html("body")

        await page.close()

        body = Selector(text=html_content)

        yield {
            "heading": body.css("h1::text").get(),
            "paragraph": body.css("p::text").get()
        }

