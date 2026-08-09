from bs4 import BeautifulSoup
 
 
def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find('h1')
    title_tag = soup.find('title')
    desc_tag = soup.find('meta', attrs={'name': 'description'})

    if h1_tag:
        h1 = h1_tag.get_text(strip=True)
    else:
        h1 = ''

    if title_tag:
        title = title_tag.get_text(strip=True)
    else:
        title = ''

    if desc_tag:
        description = desc_tag.get('content', '')
    else:
        description = ''

    return {
        'h1': h1,
        'title': title,
        'description': description,
    }
