import requests
from html.parser import HTMLParser
from urllib.parse import urljoin

class LinkParser(HTMLParser):
    """
    A parser to extract links from HTML content.
    """
    def __init__(self, baseUrl):
        super().__init__()
        self.baseUrl = baseUrl
        self.links = []

    def handle_starttag(self, tag, attrs):
        """
        Handle start tags in HTML.
        """
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    new_url = urljoin(self.baseUrl, value)
                    self.links.append(new_url)

    def get_links(self, url):
        """
        Get links from the specified URL.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad response status
            if 'text/html' in response.headers.get('Content-Type', ''):
                self.links.clear()  # Clear previous links
                self.baseUrl = url
                self.feed(response.text)
                return response.text, self.links
            else:
                return "", []
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return "", []

def spider(url, max_pages):
    """
    Crawl web pages starting from the given URL.
    """
    links = []
    pages_to_visit = [url]
    number_visited = 0
    
    while number_visited < max_pages and pages_to_visit and not links:
        number_visited += 1
        url = pages_to_visit.pop(0)
        try:
            parser = LinkParser(url)
            _, links = parser.get_links(url)
            pages_to_visit.extend(links)
        except Exception as e:
            print(f"Error parsing URL '{url}': {e}")
    
    return links[:max_pages]
    crawled_links = spider("http://vulnweb.com", 10)
    print(crawled_links)
