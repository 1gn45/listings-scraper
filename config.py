from dotenv import load_dotenv
import os

load_dotenv()

listing_page_url = os.getenv("listing_page_url")

listing_pages = {
    listing_page_url: {
        "page_name": listing_page_url,
        "search_rules": {
            "search_urls": [
                "https://"
                + listing_page_url
                + "/skelbimai/naudoti-automobiliai?order_by=3&order_direction=DESC&page_nr=<PAGE_NUMBER>"
            ],
            "max_page_numbers": 5,
            "listing_url_filter": {
                "announcement_class": "announcement-item",
                "sold_class": "is-sold",
            },
        },
        "database_url_field": "url_1",
    }
}
