import pandas as pd
from typing import TypeVar
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import scrapy

T = TypeVar("T")
Base = declarative_base()


class LanguagesSpider(scrapy.Spider):
    name = "spider"

    def start_requests(self) -> T:
        """
        Must return an iterable of Requests
        :return:
        """
        urls: list[str] = [
            "https://pt.wikipedia.org/wiki/Lista_de_linguagens_de_programa%C3%A7%C3%A3o"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs) -> dict:
        """
         A method that will be called to handle the response # 4 a 9
         downloaded for each of the requests made.
        :param response:
        :param kwargs:
        :return:
        """
        for data in response.css("tr"):
            yield {
                "logo": data.css("td img::attr(src)").get(),
                "content":  data.css("td a::text").getall()
            }

    @staticmethod
    def __save_in_local_database(logo: str, name: str, year: int,
                                 paradigm: str, developer: str) -> None:
        orm_ = ORM()
        orm_.insert(logo, name, year, paradigm, developer)


class ProgrammingLanguages(Base):
    """Table of database"""
    __tablename__ = 'ProgrammingLanguages'

    id = Column(Integer, primary_key=True)
    logo = Column(String)
    name = Column(String)
    year = Column(Integer)
    paradigm = Column(String)
    developer = Column(String)

    def __repr__(self) -> str:
        return f"ProgrammingLanguages {self.name}"


class ORM:
    def __init__(self) -> None:
        self.__engine = create_engine("sqlite:///database_spider", echo=True)
        self.__conn = self.__engine.connect()
        self.__session = sessionmaker(bind=self.__engine)
        self.__session_ = self.__session()

    def create_table(self) -> None:
        Base.metadata.create_all(self.__engine)

    def insert(self, logo: str, name: str, year: int,
               paradigm: str, developer: str) -> None:
        """
        Insert data into table
        :return:
        """
        pl = ProgrammingLanguages(logo=logo,
                                  name=name,
                                  year=year,
                                  paradigm=paradigm,
                                  developer=developer)
        self.__session_.add(pl)
        self.__session_.commit()

    def count_lines_from_table(self) -> int:
        """
        Returns rows count
        :return: int
        """
        count: int = 0
        response = self.__engine.execute(text("SELECT * FROM ProgrammingLanguages;"))
        for row in response:
            count += 1
        return count

    def read_and_insert(self) -> None:
        """
        read items from json and insert into local sqlite
        :return: None
        """
        try:
            json_data = pd.read_json("../../spider.json")
            images = []
            data = []
            for key, value in json_data.items():
                for index, item in enumerate(value):
                    if index > 3 and (not isinstance(item, list)):
                        images.append(item)
                    if isinstance(item, list) and index > 3:
                        data.append(item)
            for i in range(len(data)):
                try:
                    self.insert(images[i], data[i][0], data[i][1], data[i][2], data[i][3])
                except IndexError:
                    pass
        except IndexError:
            print("[-] Index ERROR")


if __name__ == '__main__':
    # save into local database
    orm = ORM()
    orm.create_table()
    orm.read_and_insert()
    orm.count_lines_from_table()
