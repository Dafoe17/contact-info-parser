import argparse
import json

from parser.parser import SiteContactParser
from parser.utils.logger import logger
from parser.utils.export import Exporter

import time


def main():
    parser = argparse.ArgumentParser(
        description="Парсер сайта для извлечения email и телефонов."
    )
    parser.add_argument(
        "url",
        type=str,
        help="Стартовый URL сайта для парсинга (например, https://example.com)"
    )
    parser.add_argument(
        "--csv",
        type=str,
        help="Сохранять результат в CSV файл (указать имя файла)"
    )
    parser.add_argument(
        "--txt",
        type=str,
        help="Сохранять результат в текстовый файл (указать имя файла)"
    )

    args = parser.parse_args()
    start_url = args.url

    logger.info("Запуск парсера для сайта: %s", start_url)

    site_parser = SiteContactParser(start_url)
    start = time.time()
    result = site_parser.parse()

    logger.info("Парсинг завершен. Результат:")

    exporter = Exporter(result)

    if args.csv:
        Exporter.to_csv(exporter, args.csv)

    if args.txt:
        Exporter.to_txt(exporter, args.txt)

    print(json.dumps(result, indent=4, ensure_ascii=False))
    elapsed = time.time() - start
    minutes, seconds = divmod(elapsed, 60)
    logger.info("Время выполнения: %d минут %.2f сек", minutes, seconds)


if __name__ == "__main__":
    main()
