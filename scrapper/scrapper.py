import datetime
import locale
import re

import pymorphy3
import requests
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")


class MonstercatNews:
    """Класс для создания новостных постов"""

    def __init__(self, url: str, date: str) -> None:
        """Инициализирует объект MonstercatNews.

        Args:
            url (str): URL-адрес новости Monstercat.
            date (str): Дата релиза в формате дд.мм.гггг.

        Raises:
            ValueError: Если URL-адрес не соответствует домену monster.cat.
        """
        self.url = self.add_https(url)
        self.date = date
        self.morph = pymorphy3.MorphAnalyzer()

        if not self.is_valid_link():
            raise ValueError("Ссылка не соответствует домену monster.cat")

        self.html = self.get_html()

    def add_https(self, url: str) -> str:
        """Добавляет https:// к URL-адресу, если он еще не содержит его.

        Args:
            url (str): URL-адрес релиза.

        Returns:
            str: URL-адрес релиза с https://.
        """
        if url.startswith("monster.cat/"):
            url = "https://" + url
        return url

    def is_valid_link(self) -> bool:
        """Проверяет, является ли URL-адрес ссылкой на monster.cat.

        Returns:
            bool: True, если URL-адрес является ссылкой на monster.cat, False - в противном случае.
        """
        return bool(re.match(r"https://monster\.cat/*", self.url))

    def get_html(self) -> str:
        """Загружает HTML-код страницы по URL-адресу self.url.

        Returns:
            str: HTML-код страницы.
        """
        response = requests.get(self.url, allow_redirects=True)
        return response.text

    def get_release_title(self) -> str | None:
        """Получает название релиза из HTML-кода страницы.

        Returns:
            str: Название релиза или None, если его не удалось найти.
        """
        soup = BeautifulSoup(self.html, "lxml")
        title = soup.find("h2", class_="song-info")

        if title is None:
            return None
        return title.text.replace(" - ", " -- ")

    def get_image_url(self) -> str | None:
        """Получает URL-адрес изображения из HTML-кода страницы.

        Returns:
            str: URL-адрес изображения или None, если его не удалось найти.
        """
        soup = BeautifulSoup(self.html, "lxml")
        image = soup.find("img", class_="responsive-image null")

        if image is None:
            return None
        return image["src"]  # type: ignore

    def get_date_string(self) -> str:
        """Формирует строку с датой релиза в формате "В (Во) *день недели*, *число* *месяц строкой*, на *название лейбла*".

        Returns:
            str: Строка с датой релиза и лейблом.
        """
        day, month, year = self.date.split(".")
        date = datetime.date(int(year), int(month), int(day))
        weekday = date.strftime("%A")
        day = int(day)
        month = date.strftime("%B")
        month = self.morph.parse(month)[0].inflect({"gent"}).word  # type: ignore

        preposition = "В"
        if weekday == "вторник":
            preposition = "Во"

        label = {
            "понедельник": "Uncaged",
            "вторник": "Silk",
            "среда": "Uncaged",
            "четверг": "Instinct",
            "пятница": "Uncaged",
        }.get(weekday, "Unknown")

        return f"{preposition} {weekday}, {day} {month}, на {label}."

    def get_post_text(self) -> str:
        """Формирует текст новостного поста.

        Returns:
            str: Текст поста в формате **Название релиза**\n\n*дата релиза и лейбл*\nСохранить заранее: *URL релиза*\n\n#News.
        """
        title = self.get_release_title()
        date = self.get_date_string()

        post = f"**{title}**\n\n{date}\nСохранить заранее: {self.url}\n\n#News"
        return post

    def __str__(self) -> str:
        """Возвращает текст поста."""
        return self.get_post_text()
