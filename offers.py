"""Script containing the class responsible for parsing the offers 
from the baseURL and a model of a Offer"""

import logging
from bs4 import BeautifulSoup, ResultSet
from pydantic import BaseModel
from pydantic_core import Url
import requests


class Offer(BaseModel):
    """Model of a Offer with the following fields:"""
    name: str
    image: Url
    description: str
    offer_detail: str
    tags: list[str]


class OffersParser():
    """Class responsible for parsing the offers from the url and returning a list of Offer objects."""
    def __init__(self, base_url: str = "https://education.github.com/pack"):
        self.base_url = base_url
        self.result_offers = []
        

    def list_offers(self)-> list[Offer]:
        logging.info(f"Parsing Github Education offers from {self.base_url}")
        for raw_offer in self._parse_offers():
            offer = self._parse_offer(raw_offer)
            self.result_offers.append(offer)
        return self.result_offers
    

    def _parse_offers(self)-> ResultSet:
        soup = BeautifulSoup(self._get_soup_markup() , 'html.parser')
        cards = soup.find_all('div', class_='pack-offer-card')
        return cards


    def _parse_offer(self, card)->Offer:
        name = card.find('h3').text
        image = self._parse_image(card)
        description = self._parse_description(card)
        offer_detail = self._parse_offer_detail(card)
        tags = self._parse_tags(card)

        return Offer(name=name,
                     image=image,
                     description=description,
                     offer_detail=offer_detail,
                     tags=tags)


    def _parse_image(self, card)-> Url:
        src = card.find('img')['src']
        if src.startswith('/assets'):
            return "https://education.github.com/" + src
        else:
            return card.find('img')['src']

            
    def _parse_description(self, card)-> str:
        description_section = card.find('h4').find_next_sibling()
        return description_section.text


    def _parse_offer_detail(self, card)-> str:
        offer_detail_section = card.find('h5').find_next_sibling()
        return offer_detail_section.text


    def _parse_tags(self, card)-> list[str]:
        tag_names = []
        tag_list_items = card.find('h6').find_next_sibling().find_all('li')
        for list_item in tag_list_items:
            tag_name = list_item.find('span').text
            tag_names.append(tag_name)
        return tag_names
    
    def _get_soup_markup(self) -> str:
        response = requests.get(self.base_url, timeout=10)
        try:
            response.raise_for_status()
            logging.info(f"Scraped the target url {self.base_url}")
        except:
            logging.error(f"Error calling the scrap-target url {self.base_url}")
        return response.text