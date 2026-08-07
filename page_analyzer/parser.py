from bs4 import BeautifulSoup
 
 
def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
 
    h1_tag = soup.find('h1')
    title_tag = soup.find('title')
    desc_tag = soup.find('meta', attrs={'name': 'description'})
 
    h1 = h1_tag.get_text(strip=True) if h1_tag else ''
    title = title_tag.get_text(strip=True) if title_tag else ''
    description = desc_tag.get('content', '') if desc_tag else ''
 
    return {
        'h1': h1,
        'title': title,
        'description': description,
    }
