from selenium import webdriver
from selenium.webdriver.common.by import By


class NietzscheScraper:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape_text(self, year, notebook_number, text_number):
        print(f'Collecting notebook {notebook_number}...')
        self.driver.get(f'http://nietzschesource.org/#eKGWB/NF-{year},{notebook_number}')

        block = self.driver.find_element(By.ID, f'eKGWB/NF-{year},{notebook_number}[{text_number}]')
        return block

    def scrape_notebook(self, year, notebook_number):
        print(f'Collecting notebook {notebook_number}...')
        self.driver.get(f'http://nietzschesource.org/#eKGWB/NF-{year},{notebook_number}')

        elements = self.driver.find_elements(By.CLASS_NAME, 'txt_block')
        blocks = list(filter(lambda element: element.text.startswith(str(notebook_number)), elements))

        return blocks

    def scrape_outline(self):
        return self.scrape_text(1888, 12, 1)
