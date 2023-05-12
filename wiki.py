import requests
from bs4 import BeautifulSoup
import time
import datetime
from typing import List, Dict, Any
import json
import re


class HttpResponse:
    def get_response(self, url, params=None, headers=None):
        """
        Выполняем запрос по ссылке
        """
        response = requests.request(
            method="GET",
            url=url,
            params=params,
            headers=headers
        )
        return self.check_response(response)

    def check_response(self, response: requests.Response):
        """
        Проверка статуса запроса
        """
        if response.status_code == 200:
            return response
        else:
            error_message = f"Your request returned {response.status_code} status code."
            if response.status_code == 404:
                error_message += " The requested resource wasn't found."
            elif response.status_code == 500:
                error_message += " The server encountered an internal error."
            raise Exception(error_message)