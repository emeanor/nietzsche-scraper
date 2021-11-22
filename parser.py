from bs4 import BeautifulSoup
import re


class NietzscheParser:

    @classmethod
    def nietzsche_number(self, block):
        '''
        This is not perfect, as the odd text (e.g., 9[1]) contains more than one
        Nietzsche number. It saves a great deal of manual work though.
        '''
        # Find the first instances in the text where 1-3 digits are set in parentheses.
        parenthetical_digits = re.search(r'\(\d{1,3}?\)', block.text)
        
        if parenthetical_digits:
            nietzsche_number = parenthetical_digits.group().strip('()')
        else:
            nietzsche_number = None

        return nietzsche_number

    @classmethod
    def kgw_numbers(self, block):
        text = block.text
        notebook_number = int(text[0 : text.index('[')])
        text_number = int(text[text.index('[') + 1 : text.index(']')])
        return (notebook_number, text_number)

    @classmethod
    def text(self, block):
        html = block.get_attribute('innerHTML')

        # Remove newlines and leading/trailing whitespace.
        html = html.replace('\n', '').strip()
        # Replace multiple whitespace characters with a single one.
        html = re.sub(' +', ' ', html)
        
        soup = BeautifulSoup(html, 'html.parser')

        whitelist = ['p', 'span']

        for tag in soup.find_all(True):
            if tag.name not in whitelist:
            # There shouldn't be any cases where we want to keep link text, so remove <a> tags along with their contents.
                tag.decompose() if tag.name == 'a' else tag.unwrap()
            else:
                if tag.name == 'p':
                    tag.insert_after('\n')
                    tag.unwrap()
                elif tag.name == 'span':
                    # The 'bold' class on NietzscheSource corresponds to italics.
                    if tag.has_attr('class') and 'bold' in tag['class']:
                        tag.string = tag.string.strip()
                        tag.insert_before('*')
                        tag.insert_after('*')
                        tag.unwrap()
                    # The 'bolditalic' class on NietzscheSource corresponds to boldface.
                    elif tag.has_attr('class') and 'bolditalic' in tag['class']:
                        tag.string = tag.string.strip()
                        tag.insert_before('**')
                        tag.insert_after('**')
                        tag.unwrap()
                    else:
                        tag.unwrap()
            
        return soup

