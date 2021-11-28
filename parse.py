from bs4 import BeautifulSoup
import re

def all(block, outline, outline_only=True):
    nietzsche_number = parse_nietzsche_number(block)

    if outline_only and nietzsche_number is None:
        return

    kgw_numbers = parse_kgw_numbers(block)
    book_number = outline[nietzsche_number].get('book_number')
    title = outline[nietzsche_number].get('title')
    text = parse_text(block)

    return {
        'nietzsche_number': nietzsche_number,
        'kgw_notebook_number': kgw_numbers[0],
        'kgw_text_number': kgw_numbers[1],
        'book_number': book_number,
        'title': title,
        'text': text
    }

def parse_nietzsche_number(block):
    '''
    Find the first instance in the text where 1-3 digits are set in parentheses.
    This is not perfect, as the odd text (e.g., 9[1]) contains more than one
    Nietzsche number. It saves a great deal of manual work though.
    '''
    parenthetical_digits = re.search(r'\(\d{1,3}?\)', block.text)
    nietzsche_number = int(parenthetical_digits.group().strip('()')) if parenthetical_digits else None

    return nietzsche_number

def parse_kgw_numbers(block):
    text = block.text
    notebook_number = int(text[0 : text.index('[')])
    text_number = int(text[text.index('[') + 1 : text.index(']')])
    return (notebook_number, text_number)

def parse_text(block):
    html = block.get_attribute('innerHTML').replace('\n', '')
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
            # Insert a linebreak after each <p>, and render a centered <p> as a Markdown heading.
            if tag.name == 'p':
                if tag.has_attr('class') and 'Zentriert' in tag['class']:
                    tag.insert_before('# ')

                tag.insert_after('\n')
                tag.unwrap()
            # Render italics and boldface in Markdown.
            elif tag.name == 'span':
                if tag.string and tag.has_attr('class') and 'bold' in tag['class']:
                    tag.string = tag.string.strip()
                    tag.insert_before(' *')
                    tag.insert_after('* ')
                    tag.unwrap()
                elif tag.string and tag.has_attr('class') and 'bolditalic' in tag['class']:
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

    text = text.strip()

    return text

def parse_outline(outline):
    html = outline.get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')

    rows = soup.find_all('tr')

    entries = {}
    for row in rows:
        paragraphs = row.findChildren('p')

        try: 
            nietzsche_number = int(paragraphs[0].text.replace(u'\xa0', '').strip('()'))
        except:
            pass

        title = paragraphs[1].text if len(paragraphs) > 1 else None

        if len(paragraphs) > 2:
            if paragraphs[2].text == 'I':
                book_number = 1
            elif paragraphs[2].text == 'II':
                book_number = 2
            elif paragraphs[2].text == 'III':
                book_number = 3
            elif paragraphs[2].text == 'IV':
                book_number = 4
            else:
                book_number = None

        if nietzsche_number is not None:
            entries[nietzsche_number] = {
                    'title': title,
                    'book_number': book_number
                }

    return entries
