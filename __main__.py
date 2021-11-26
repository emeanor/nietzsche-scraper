from scraper import NietzscheScraper
import parse

def export_374():
    scraper = NietzscheScraper()

    # blocks = []
    # for n in range (9, 12):
    #     for block in scraper.scrape_notebook(1887, n):
    #         blocks.append(block)

    texts = []
    for block in scraper.scrape_notebook(1887, 9):
        nietzsche_num = parse.nietzsche_number(block)

        if nietzsche_num is not None:
            kgw_nums = parse.kgw_numbers(block)
            full_text = parse.text(block)

            texts.append({
                'nietzsche_number': nietzsche_num,
                'kgw_notebook_number': kgw_nums[0],
                'kgw_text_number': kgw_nums[1],
                'text': full_text
            })

    print(texts)

export_374()
