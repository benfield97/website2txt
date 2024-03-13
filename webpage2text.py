import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_urls(url):
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid_url(href):
            continue
        if domain_name not in href:
            continue
        urls.add(href)
    return urls

def get_text_from_url(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    text = soup.get_text(separator="\n")
    return text

def scrape_website(url, output_file):
    urls = get_all_urls(url)
    with open(output_file, "w", encoding="utf-8") as file:
        for url in urls:
            text = get_text_from_url(url)
            file.write(text)
            file.write("\n\n")

# Example usage
website_url = "https://react-pdf.org/"
output_file = "react-pdf.txt"
scrape_website(website_url, output_file)