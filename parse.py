from bs4 import BeautifulSoup
import re

def nietzsche_number(block):
    '''
    This is not perfect, as the odd text (e.g., 9[1]) contains more than one
    Nietzsche number. It saves a great deal of manual work though.
    '''
    # Find the first instances in the text where 1-3 digits are set in parentheses.
    parenthetical_digits = re.search(r'\(\d{1,3}?\)', block.text)
    nietzsche_number = parenthetical_digits.group().strip('()') if parenthetical_digits else None

    return nietzsche_number

def kgw_numbers(block):
    text = block.text
    notebook_number = int(text[0 : text.index('[')])
    text_number = int(text[text.index('[') + 1 : text.index(']')])
    return (notebook_number, text_number)

def text(block):
    html = block.get_attribute('innerHTML').strip().replace('\n', '')
    soup = BeautifulSoup(html, 'html.parser')

    # Remove errata tooltip divs first to avoid nesting problems in the main loop.
    errata = soup.find_all('div', { 'class': 'tooltip' })
    for erratum in errata:
        erratum.decompose()

    whitelist = ['p', 'span']
    for tag in soup.find_all(True):
        if tag.name not in whitelist:
            # There is never a need to retain link text.
            tag.decompose() if tag.name == 'a' else tag.unwrap()
        else:
            if tag.name == 'p':
                if tag.has_attr('class') and 'Zentriert' in tag['class']:
                    tag.insert_before('# ')

                tag.insert_after('\n')
                tag.unwrap()
            elif tag.name == 'span':
                if tag.has_attr('class') and 'bold' in tag['class']:
                    tag.string = tag.string.strip()
                    tag.insert_before(' *')
                    tag.insert_after('* ')
                    tag.unwrap()
                elif tag.has_attr('class') and 'bolditalic' in tag['class']:
                    tag.string = tag.string.strip()
                    tag.insert_before(' **')
                    tag.insert_after('** ')
                    tag.unwrap()
                else:
                    tag.unwrap()

    text = str(soup)

    # Remove repeated whitespace characters created by markdown parsing.
    text = re.sub(' +', ' ', text)

    # Remove whitespace between asterisks and certain punctuation marks.
    text = re.sub('\*\s([.,:)])', '*\\1', text)

    return text
