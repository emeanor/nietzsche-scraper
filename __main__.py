from scraper import NietzscheScraper
import parse

def export(notebook_numbers):
    scraper = NietzscheScraper()

    notebooks = []
    for number in notebook_numbers:
        notebook = scraper.scrape_notebook(1887, number)

        blocks = []
        for block in notebook:
            blocks.append(block)

        notebooks.append({
            'notebook_number': number,
            'blocks': blocks 
        })

    texts = []
    for notebook in notebooks:
        notebook_texts = []
        for block in notebook['blocks']:
            nietzsche_num = parse.nietzsche_number(block)

            if nietzsche_num is not None:
                kgw_nums = parse.kgw_numbers(block)
                full_text = parse.text(block)

                notebook_texts.append({
                    'nietzsche_number': nietzsche_num,
                    'kgw_notebook_number': kgw_nums[0],
                    'kgw_text_number': kgw_nums[1],
                    'text': full_text
                })
        
        texts.append(notebook_texts)

    print(texts)

export_374([9])
