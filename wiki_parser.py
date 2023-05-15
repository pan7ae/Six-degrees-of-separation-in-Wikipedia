import requests
from bs4 import BeautifulSoup
from typing import List
import time


def send_request(url: str, rate_limit: int) -> str:
    """
    Отправка GET-запроса на URL-адрес

    :param url: URL-адрес страницы с Wikipedia
    :param rate_limit: Ограничение на количество запросов
    :return: Возвращает текст ответа с сервера
    """
    time.sleep(60 / rate_limit)
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def get_wikipedia_links(html: requests.Response.text, base_url: str) -> List[str]:
    """
    Парсинг HTML-текста и возвращает список ссылок на другие статьи на сайте Wikipedia.

    :param html: Текст HTTP-запроса
    :param base_url: Базовая сслыка на Wikipedia
    :return: Список ссылок, ведущих на другие статьи Wikipedia
    """
    soup = BeautifulSoup(html, "html.parser")
    main_content = soup.find("div", {"id": "bodyContent"})
    all_links = main_content.find_all("a", href=True)

    wiki_links = []

    for link in all_links:
        href = link["href"]
        if href.startswith("/wiki/") and ":" not in href:
            full_url = base_url + href
            wiki_links.append(full_url)

    return wiki_links
