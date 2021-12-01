from scraper import NietzscheScraper
import parse
import json

NOTEBOOKS_TO_EXPORT = [9]
OUTPUT_FILENAME = 'notebooks'

def get_notebooks(notebook_numbers):
    scraper = NietzscheScraper()
    outline = parse.parse_outline(scraper.scrape_outline())

    texts = []
    for number in notebook_numbers:
        blocks = scraper.scrape_notebook(1887, number)

        print('Processing texts...')
        texts = []
        for block in blocks:
            text = parse.all(block, outline)
            if text is not None:
                texts.append(text)

    return(texts)


notebooks = get_notebooks(NOTEBOOKS_TO_EXPORT)

with open(f'{OUTPUT_FILENAME}.json', 'w') as fp:
    json.dump(notebooks, fp)

print(f'Notebooks {NOTEBOOKS_TO_EXPORT} have been exported to {OUTPUT_FILENAME}.json.')
