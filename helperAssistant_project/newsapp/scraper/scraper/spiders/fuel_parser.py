import pickle
from pathlib import Path
import scrapy
from datetime import datetime

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
file = Path(BASE_DIR).joinpath(Path('fuel_data.txt'))


class FuelParserSpider(scrapy.Spider):
    name = 'fuel_parser'
    allowed_domains = ['index.minfin.com.ua']
    start_urls = ['https://index.minfin.com.ua/ua/markets/fuel/tm/']

    def parse(self, response):
        data = list()
        id_key = 1
        date_resp = response.xpath("/html//div[@class='idx-updatetime']/text()").get().split()
        date = date_resp[2]
        try:
            date = datetime.strptime(date, "%d.%m.%Y").isoformat()
        except ValueError:
            print(f'Error for {date}')
        for element in response.xpath('/html//td[@class="r1"]').extract():
            if 'left' in element:
                temp_title = element.replace('<', ' ').replace('>', ' ').split()
                if len(temp_title) == 8:
                    title = temp_title[-3]
                elif len(temp_title) == 9:
                    title = temp_title[-4] + temp_title[-3]
                i = dict()
                i['title'] = title
            elif 'right' in element and id_key % 5 == 1:
                temp_price = element.replace('<', ' ').replace('>', ' ').split()
                price = temp_price[-2]
                if price == 'br':
                    price = 0.0
                else:
                    price = float(price.replace(",", "."))
                i['nf_plus'] = price
                id_key += 1
            elif 'right' in element and id_key % 5 == 2:
                temp_price = element.replace('<', ' ').replace('>', ' ').split()
                price = temp_price[-2]
                if price == 'br':
                    price = 0.0
                else:
                    price = float(price.replace(",", "."))
                i['nf'] = price
                id_key += 1
            elif 'right' in element and id_key % 5 == 3:
                temp_price = element.replace('<', ' ').replace('>', ' ').split()
                price = temp_price[-2]
                if price == 'br':
                    price = 0.0
                else:
                    price = float(price.replace(",", "."))
                i['nt'] = price
                id_key += 1
            elif 'right' in element and id_key % 5 == 4:
                temp_price = element.replace('<', ' ').replace('>', ' ').split()
                price = temp_price[-2]
                if price == 'br':
                    price = 0.0
                else:
                    price = float(price.replace(",", "."))
                i['dp'] = price
                id_key += 1
            elif 'right' in element and id_key % 5 == 0:
                temp_price = element.replace('<', ' ').replace('>', ' ').split()
                price = temp_price[-2]
                if price == 'br':
                    price = 0.0
                else:
                    price = float(price.replace(",", "."))
                i['gas'] = price
                i['date'] = date
                id_key += 1
                data.append(i)
        for element in response.xpath('/html//td[@class="r0"]').extract():
            if 'left' in element:
                temp_title = element.replace('<', ' ').replace('>', ' ').split()
                if len(temp_title) == 8:
                    title = temp_title[-3]
                elif len(temp_title) == 9:
                    title = temp_title[-4] + " " + temp_title[-3]
                i = dict()
                i['title'] = title
            elif 'right' in element and id_key % 5 == 1:
                temp_price = element.replace('<', ' ').replace('>', ' ').split()
                price = temp_price[-2]
                if price == 'br':
                    price = 0.0
                else:
                    price = float(price.replace(",", "."))
                i['nf_plus'] = price
                id_key += 1
            elif 'right' in element and id_key % 5 == 2:
                temp_price = element.replace('<', ' ').replace('>', ' ').split()
                price = temp_price[-2]
                if price == 'br':
                    price = 0.0
                else:
                    price = float(price.replace(",", "."))
                i['nf'] = price
                id_key += 1
            elif 'right' in element and id_key % 5 == 3:
                temp_price = element.replace('<', ' ').replace('>', ' ').split()
                price = temp_price[-2]
                if price == 'br':
                    price = 0.0
                else:
                    price = float(price.replace(",", "."))
                i['nt'] = price
                id_key += 1
            elif 'right' in element and id_key % 5 == 4:
                temp_price = element.replace('<', ' ').replace('>', ' ').split()
                price = temp_price[-2]
                if price == 'br':
                    price = 0.0
                else:
                    price = float(price.replace(",", "."))
                i['dp'] = price
                id_key += 1
            elif 'right' in element and id_key % 5 == 0:
                temp_price = element.replace('<', ' ').replace('>', ' ').split()
                price = temp_price[-2]
                if price == 'br':
                    price = 0.0
                else:
                    price = float(price.replace(",", "."))
                i['gas'] = price
                i['date'] = date
                id_key += 1
                data.append(i)

        with open(file, 'wb') as fh:
            pickle.dump(data, fh)


def main():
    runner = CrawlerRunner()
    d = runner.crawl(FuelParserSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == '__main__':
    main()
