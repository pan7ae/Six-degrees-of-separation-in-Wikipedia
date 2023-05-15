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
    url2 = "https://en.wikipedia.org/wiki/Dietrich_Mateschitz"
    url1 = "https://en.wikipedia.org/wiki/Lewis_Hamilton"
    rate_limit = 10

    shortest_path = find_shortest_path(url1, url2, rate_limit)
    if shortest_path:
        print(" => ".join(shortest_path))
    else:
        print("Цепочка переходов не найдена за 5 шагов.")
