# Теория 6 рукопожатий на Wikipedia

## Часть 1: Краткая устная реализация задачи, план, и технологии

Задача заключается в написании приложения на языке Python, которое будет анализировать ссылки на Википедии и находить цепочку переходов между двумя заданными страницами.

### План:
* Получить входные данные - два URL и ограничение на количество запросов в минуту;
* Написать функцию для получения страницы Википедии и извлечения всех ссылок на другие страницы; * Википедии из основного блока статьи и блока "References";
* Реализовать алгоритм поиска в ширину (BFS) для нахождения кратчайшего пути между двумя страницами Википедии, с учетом ограничения на количество запросов в минуту;
* Если кратчайший путь не найден за 5 шагов, сообщить об этом;
* Если путь найден, вывести его.

Технологии:
* Библиотека `requests` для выполнения HTTP-запросов к Википедии;
* Библиотека `BeautifulSoup` для парсинга HTML-страниц и извлечения ссылок;
* Библиотека `typing` для аннотации типов;
* Встроенные библиотеки Python, такие как `time` для управления скоростью запросов и `collections` для реализации алгоритма BFS.

Выбор именно этих технологий обосновывается их широкой распространенностью, хорошей документацией и простотой использования. В качестве альтернатив можно рассмотреть использование библиотек scrapy или aiohttp для асинхронных запросов, однако они более сложны в использовании и могут быть избыточны для данной задачи.


## Часть 2: Структура проекта

В данном случае, задача относительно простая и весь код может быть умещен в одном файле. Однако, я всё равно предлагаю разделить код на две части:
* [`wiki_parser.py`](wiki_parser.py): Этот модуль будет содержать функции для работы с Wikipedia: функции для извлечения ссылок из статьи и функции для ограничения скорости запросов;
* [`main.py`](main.py): Этот модуль будет использовать функции из [`wiki_parser.py`](wiki_parser.py) для реализации алгоритма BFS и нахождения кратчайшего пути между двумя страницами Wikipedia.

Такая структура позволит нам отделить логику работы с Википедией от логики поиска кратчайшего пути, что упростит поддержку и масштабирование проекта. Если в будущем потребуется добавить другие источники информации или изменить алгоритм поиска, мы сможем это сделать без значительных изменений в существующем коде.


## Часть 3: Реализация кода

Для начала, создадим файл [`wiki_parser.py`](wiki_parser.py) и определим в нем функции для работы с Wikipedia.

[`wiki_parser.py`](wiki_parser.py):
```python
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

```

Теперь создадим файл [`main.py`](main.py) и определим функцию `find_shortest_path`, которая будет реализовывать алгоритм BFS для нахождения кратчайшего пути между двумя страницами Википедии.

[`main.py`](main.py):
```python
from collections import deque
from wiki_parser import get_wikipedia_links, send_request
from typing import List


def find_shortest_path(url_1: str, url_2: str, rate_limit: int) -> List[str] | None:
    """
    Используем очередь и поиск в ширину для обхода графа связей между страницами.

    :param url_1: URL-адрес страницы с Wikipedia
    :param url_2: URL-адрес страницы с Wikipedia
    :param rate_limit: Ограничение на количество запросов
    :return: Кратчайший путь в виде списка URL-адресов или None
    """
    base_url = "https://en.wikipedia.org"

    # Очередь путей, которые нужно исследовать
    queue = deque()

    # Множество посещенных адресов для избежания дублирования
    visited = set()

    queue.append(([url_1], 0))
    visited.add(url_1)

    while queue:
        path, depth = queue.popleft()

        if depth > 5:
            return None

        last_url = path[-1]
        html = send_request(last_url, rate_limit)
        wiki_links = get_wikipedia_links(html, base_url)

        for link in wiki_links:
            if link == url_2:
                path.append(link)
                return path

            if link not in visited:
                visited.add(link)
                new_path = path.copy()
                new_path.append(link)
                queue.append((new_path, depth + 1))

    return None


if __name__ == "__main__":
    url_1 = "https://en.wikipedia.org/wiki/Dietrich_Mateschitz"
    url_2 = "https://en.wikipedia.org/wiki/Lewis_Hamilton"
    rate_limit = 10

    shortest_path = find_shortest_path(url_1, url_2, rate_limit)
    if shortest_path:
        print(" => ".join(shortest_path))
    else:
        print("Цепочка переходов не найдена за 5 шагов.")

```

В предпоследней части приведен пример использования функции `find_shortest_path`. Если цепочка переходов найдена, она будет выведена на экран, иначе будет выведено сообщение о том, что цепочка не найдена за 5 шагов.


## Часть 4: Пример использования

Чтобы запустить приложение, нужно выполнить файл [`main.py`](main.py). В качестве входных параметров в коде уже заданы две ссылки на статьи и ограничение на количество запросов в минуту. Если требуется изменить входные параметры, можно просто изменить значения переменных `url_1`, `url_2` и `rate_limit` в коде.

Пример:
```
python main.py
```

После запуска приложение начнет анализировать ссылки на Wikipedia и искать цепочку переходов между двумя заданными страницами. Если цепочка будет найдена, она будет выведена на экран. Если цепочка не будет найдена за 5 шагов, будет выведено сообщение об этом:

```
https://en.wikipedia.org/wiki/Dietrich_Mateschitz => https://en.wikipedia.org/wiki/List_of_Formula_One_World_Constructors%27_Champions => https://en.wikipedia.org/wiki/Lewis_Hamilton
```

## Часть 5: Вывод

Мы успешно реализовали приложение на Python, которое анализирует ссылки на Википедии и находит цепочку переходов между двумя заданными страницами. Приложение использует алгоритм поиска в ширину (BFS) и учитывает ограничение на количество запросов в минуту. Проект организован таким образом, что легко масштабируется и поддерживается.

Также для удобства имеется [`laba_2_wiki.ipynb`](laba_2_wiki.ipynb) для запуска приложения в Google Colab или Jupyter Notebook
