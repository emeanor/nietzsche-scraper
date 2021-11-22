from scraper import NietzscheScraper
from parser import NietzscheParser

scraper = NietzscheScraper()
block = scraper.scrape_text(1887, 9, 5)

#print(block.text)
print(NietzscheParser.text(block))