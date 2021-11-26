from scraper import NietzscheScraper
import parse

def get_notebooks(notebook_numbers, outline_only=True):
    scraper = NietzscheScraper()

    notebooks = []
    for number in notebook_numbers:
        blocks = scraper.scrape_notebook(1887, number)

        print('Processing texts...')
        texts = []
        for block in blocks:
            texts.append(parse.all(block))

        notebooks.append({
            'notebook_number': number,
            'texts': texts
        })

    print(notebooks)

get_notebooks([10])
