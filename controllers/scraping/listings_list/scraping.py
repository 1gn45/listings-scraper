from typing import Any, Dict
from bs4 import BeautifulSoup


def get_listing_urls_from_search_page(
    page_html: str, search_rules: Dict[str, Any], get_listings_by_status=False
):
    soup = BeautifulSoup(page_html, "html.parser")
    urls = []
    filtering_class = search_rules["listing_url_filter"]["announcement_class"]
    if not get_listings_by_status:
        filtering_class = search_rules["listing_url_filter"]["announcement_class"]
    elif get_listings_by_status == "sold":
        filtering_class = search_rules["listing_url_filter"]["sold_class"]

    for anchor in soup.find_all("a", href=True, class_=filtering_class):
        href = anchor["href"]
        urls.append(href)
    return urls


def get_page_data_from_page_html(page_html):
    return False
