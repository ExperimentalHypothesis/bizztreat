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


def main():
    logger.info("Scraping the BizzTreat web started. ")
    rows = []
    for i in range(1, 51):
        url = f"https://www.bizztreat.com/bizztro?p1400={i}"
        parser = Parser(url)
        rows.extend(parser.parse())
    write_to_csv("outfile-sync.csv", rows)
    logger.info("Scraping the BizzTreat web finished. ")


if __name__ == "__main__":
    main()
