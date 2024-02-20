from re import T
from xmlrpc.client import Boolean
import requests
from typing import Any, Dict, List
from controllers.fetch_page import fetch_page
import controllers.scraping.listings_list.scraping as listings_list
from controllers.scraping.initiation.login import login
import time
from fetch_listing import add_listing
from config import listing_pages

from controllers.scraping.common.apply_actions_on_page import (
    apply_click_on_elements_with_innerHtml,
    apply_click_on_element_by_class,
    type_text_globally,
)


time_1 = time.time()
for page in listing_pages.values():
    for url in page["search_rules"]["search_urls"]:
        previous_listing_urls: List[str] = []
        current_listing_urls: List[str] = []
        sold_urls: List[str] = []
        for page_number in range(page["search_rules"]["max_page_numbers"]):
            print("page number: ", page_number + 1)
            check_url = url.replace("<PAGE_NUMBER>", str(page_number + 1))

            page_driver = fetch_page(check_url)
            login(page_driver)
            page_content = page_driver.page_source

            current_listing_urls = listings_list.get_listing_urls_from_search_page(
                page_content, page["search_rules"]
            )
            sold_urls = listings_list.get_listing_urls_from_search_page(
                page_content, page["search_rules"], "sold"
            )

            if previous_listing_urls and current_listing_urls == previous_listing_urls:
                break
            previous_listing_urls = current_listing_urls
            active_listing_urls = set(current_listing_urls) - set(sold_urls)
            # add_listing(
            #     current_listing_urls[1], page["database_url_field"], page["page_name"]
            # )
            [
                add_listing(
                    page_driver, url, page["database_url_field"], page["page_name"]
                )
                for url in active_listing_urls
            ]
    time_2 = time.time()

    print("time elapsed: ", time_2 - time_1)
