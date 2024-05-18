"""Simple script that parses all offer listed on the pack page of GitHub Education and notifies the webhook with the new list."""
import logging
import logger
from dotenv import load_dotenv
import os
from offers import OffersParser
from webhook import call_webhook

load_dotenv()

def main():
    #define the variable on your dotenv file or use the os command to set the variable
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url is None:
        raise ValueError("environment variable WEBHOOK_URL not set")
    
    offers_parser = OffersParser()  
    offers = offers_parser.list_offers()
    serialized_offers = [offer.model_dump_json() for offer in offers]
    result_code = call_webhook(webhook_url, serialized_offers)

    logging.info(f"Webhook called with status code {result_code}")


if __name__ == "__main__":
    main()