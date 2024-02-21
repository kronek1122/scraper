import requests
from bs4 import BeautifulSoup

URL = 'https://en.wikipedia.org/wiki/Snakelocks_anemone'
search_text = 'Bob'

class WikiScraper:
    def __init__(self, start_url, search_word):
        self.start_url = start_url
        self.visited_urls = set()
        self.queue_url = [start_url]
        self.step = 0
        self.search_word = search_word
        self.page_visited = 0

    def __str__(self):
        return f'Scraper: {URL}'


    def get_links_from_url(self, url):
        links = []
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, features='html.parser')
            for a in soup.select('p a[href^="/wiki/"]'):
                link = "https://en.wikipedia.org" + a['href']
                if link not in self.visited_urls:
                    links.append(link)
        except Exception as error:
            print(f'Error: {error} from {url}')
        return links


    def has_searched_word_been_mentioned(self, url):
        try:
            response = requests.get(url)
            return self.search_word in response.text
        except Exception as error:
            print(f'Error while checking in {url}: {error}')
            return False
    

    def search_for_word(self):
        while self.queue_url:
            current_url = self.queue_url.pop(0)
            self.visited_urls.add(current_url)
            self.page_visited += 1
            print(f'Checking {current_url} (Steps: {self.step}, Page visited {self.page_visited})')
        
            if self.has_searched_word_been_mentioned(current_url):
                print(f'We have found a mention about {self.search_word} after: {self.step} steps')
                return 

            for link in self.get_links_from_url(current_url):
                if link not in self.visited_urls:
                    self.queue_url.append(link)
                
            self.step += 1



if __name__ == "__main__":
    scraper = WikiScraper(URL, search_text)
    scraper = scraper.search_for_word()
