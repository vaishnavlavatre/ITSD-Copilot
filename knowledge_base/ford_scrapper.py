import requests
from bs4 import BeautifulSoup
import json
import time
import re

class FordKBScraper:
    def __init__(self):
        self.base_url = "https://www.techatford.com"
        self.session = requests.Session()
        # Add any required headers for authentication
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_kb_index(self, url):
        """Scrape the main Unix KBA index page"""
        try:
            print(f"Scraping: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            kb_articles = []
            
            # Look for knowledge base articles - this selector might need adjustment
            articles = soup.find_all('div', class_=re.compile(r'kb|article|item', re.I))
            
            for article in articles:
                try:
                    title_elem = article.find(['h1', 'h2', 'h3', 'h4', 'a'], class_=re.compile(r'title|heading', re.I))
                    link_elem = article.find('a', href=True)
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        link = link_elem['href']
                        if not link.startswith('http'):
                            link = self.base_url + link
                        
                        kb_articles.append({
                            'title': title,
                            'url': link,
                            'kb_number': self.extract_kb_number(title) or self.extract_kb_number(link)
                        })
                except Exception as e:
                    print(f"Error parsing article: {e}")
                    continue
            
            return kb_articles
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []

    def extract_kb_number(self, text):
        """Extract KB number from text"""
        match = re.search(r'KB(\d+)', text, re.IGNORECASE)
        return match.group(0) if match else None

    def scrape_article_content(self, url):
        """Scrape content from individual KB article"""
        try:
            print(f"Scraping article: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_elem = soup.find(['h1', 'h2', 'h3'], class_=re.compile(r'title|heading', re.I))
            title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
            
            # Extract content - this will vary based on the page structure
            content_elems = soup.find_all(['p', 'div'], class_=re.compile(r'content|body|description', re.I))
            content = "\n".join([elem.get_text(strip=True) for elem in content_elems if elem.get_text(strip=True)])
            
            # Extract tags/categories
            tag_elems = soup.find_all(['span', 'div'], class_=re.compile(r'tag|category|label', re.I))
            tags = [elem.get_text(strip=True) for elem in tag_elems if elem.get_text(strip=True)]
            
            return {
                'title': title,
                'content': content,
                'tags': tags,
                'url': url
            }
            
        except Exception as e:
            print(f"Error scraping article {url}: {e}")
            return None

def main():
    scraper = FordKBScraper()
    
    # Main Unix KBA index URL
    index_url = "https://www.techatford.com/now/nav/ui/classic/params/target/kb_view.do?sys_kb_id=33e3ffa99f702a54611ed07e1124ab51&searchTerm=unix%20index"
    
    print("Starting Ford Knowledge Base scraping...")
    
    # Scrape the index page
    articles = scraper.scrape_kb_index(index_url)
    
    print(f"Found {len(articles)} articles in index")
    
    # Scrape each article (limited to 5 for demo)
    kb_data = []
    for i, article in enumerate(articles[:5]):
        print(f"Processing article {i+1}/{len(articles[:5])}: {article['title']}")
        content = scraper.scrape_article_content(article['url'])
        if content:
            kb_data.append(content)
        time.sleep(1)  # Be respectful to the server
    
    # Save to file
    with open('knowledge_base/ford_scraped_kb.json', 'w', encoding='utf-8') as f:
        json.dump(kb_data, f, indent=2, ensure_ascii=False)
    
    print(f"Scraping complete. Saved {len(kb_data)} articles to ford_scraped_kb.json")

if __name__ == "__main__":
    main()