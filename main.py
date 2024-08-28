import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_html(content, path):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)

def download_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error when downloading {url}: {response.status_code}")
        return None
    return response.text

def find_subpages(base_url, html_content, whitelist):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)
    subpages = []

    for link in links:
        href = link['href']
        full_url = urljoin(base_url, href)

        if any(allowed_url in full_url for allowed_url in whitelist):
            subpages.append(full_url)

    return list(set(subpages))  # removes duplicates

def main(base_url, whitelist):
    # generate root directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_url_name = base_url.replace("https://", "").replace("http://", "").replace("/", "")

    pages_directory = os.path.join("pages", f"{timestamp}_{base_url_name}")
    create_directory(pages_directory)

    # download base page
    base_html = download_page(base_url)
    if base_html is None:
        return

    # save index page
    save_html(base_html, os.path.join(pages_directory, 'index.html'))

    # get subpages
    subpages = find_subpages(base_url, base_html, whitelist)
    for subpage_url in subpages:
        html_content = download_page(subpage_url)
        if html_content:
            # Generate subpage name
            subpage_name = subpage_url.replace("https://", "").replace("http://", "").replace("/", "_")
            subpage_path = os.path.join(pages_directory, f"{subpage_name}.html")
            save_html(html_content, subpage_path)
            print(f"Content of {subpage_url} is downloaded and saved.")

if __name__ == "__main__":
    base_url = 'https://www.kauz.ch/'
    whitelist = ['https://www.kauz.ch/services', 'https://www.kauz.ch/integration']

    main(base_url, whitelist)
