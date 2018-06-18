import scrapy
import json

class GovLkSpider(scrapy.Spider):
    name = 'govlk_services'

    def start_requests(self):
        # count contains number of pages for each letter topic pages
        count = {}

        count['A'] = 5; count['B'] = 2; count['C'] = 5; count['D'] = 3; count['E'] = 3; count['F'] = 5
        count['G'] = 1; count['H'] = 1; count['I'] = 5; count['J'] = 1; count['L'] = 2; count['M'] = 2
        count['N'] = 2; count['O'] = 10; count['P'] = 5; count['R'] = 11; count['S'] = 7; count['T'] = 3
        count['U'] = 1; count['V'] = 3; count['W'] = 2

        urls = []

        url_format = 'https://www.gov.lk/iclass/icm-atozindex.php?category=https%3A%2F%2Fwww.gov.lk%2Fservices%2Feservices&text={0}&lang=en&page={1}'

        for letter in count:
            for page in xrange(count[letter]):
                urls.append(url_format.format(letter, str(page)))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        data = json.loads(response.body)
        services = data['results']['bindings']

        for service in services:
            if 'howto_endpoint' in service:
                service_name = service['servicename']['value']
                description = service['description']['value']
                url = service['howto_endpoint']['value'] + service['howto_idxpage']['value']

                yield scrapy.Request(url=url, callback=self.parse_service, meta={'service_name' : service_name, 'description' : description})

        
    def parse_service(self, response):
        service_name = response.meta['service_name']
        description = response.meta['description']

        # scrape the webpage and extract the content
        # write (yield) the content as a dictionay (which will eventually be converted into a json)

    



