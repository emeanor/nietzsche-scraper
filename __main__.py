from scraper import NietzscheScraper
from parse import nietzsche_number, kgw_numbers, text

scraper = NietzscheScraper()
block = scraper.scrape_text(1887, 9, 35)

#print(block.text)
print(text(block))