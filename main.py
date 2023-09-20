import aiohttp
import asyncio
import csv
import logging

from src.parser import Parser

logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%d-%m-%Y %H:%M:%S",
                    level=logging.INFO,
                    # filename="logs.txt"
                    )

logger = logging.getLogger("scape-bizz")


def write_to_csv(outfile: str, rows: list):
    logger.info(f"Writing rows to csv file {outfile}")
    with open(outfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(rows[0]._fields)
        for row in rows:
            writer.writerow(row)


async def fetch_page(session, url: str):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text(), url
        raise Exception(f"Error fetching page {url}, status code {response.status}")


async def get_multiple_pages(loop, urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            tasks.append(fetch_page(session, url))
        return await asyncio.gather(*tasks)


def main():
    logger.info("Scraping the BizzTreat web started. ")

    loop = asyncio.get_event_loop()
    urls = [f"https://www.bizztreat.com/bizztro?p1400={i}" for i in range(1, 10)]
    pages = loop.run_until_complete(get_multiple_pages(loop, urls))

    rows = []
    for page, url in pages:
        p = Parser(page, url)
        rows.extend(p.parse())
    write_to_csv("outfile-async.csv", rows)

    logger.info("Scraping the BizzTreat web finished. ")


if __name__ == "__main__":
    main()
