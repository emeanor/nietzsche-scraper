from scraper import NietzscheScraper
import parse

def get_notebooks(notebook_numbers, outline_only=True):
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

            if outline_only == True and nietzsche_num is None:
                continue

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

get_notebooks([9])
