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

        # Remove any trailing slash for consistent matching
        if full_url.endswith('/'):
            full_url = full_url[:-1]

        # Check if the full URL ends with any of the whitelist items
        if any(full_url.endswith(allowed_url) for allowed_url in whitelist):
            subpages.append(full_url)

    return list(set(subpages))  # removes duplicates

def sanitize_directory_name(name):
    invalid_chars = [":", "*", "?", "\"", "<", ">", "|", "\\"]
    for char in invalid_chars:
        name = name.replace(char, "_")
    return name

def embed_css(base_url, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    css_links = soup.find_all('link', rel='stylesheet')
    
    for link in css_links:
        css_url = urljoin(base_url, link['href'])
        css_content = download_page(css_url)
        
        if css_content:
            # Create a <style> tag with the downloaded CSS
            style_tag = soup.new_tag('style')
            style_tag.string = css_content
            link.replace_with(style_tag)
    
    return str(soup)

def main(base_url, whitelist):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_base_url_name = sanitize_directory_name(base_url.replace("https://", "").replace("http://", "").replace("/", ""))

    pages_directory = os.path.join("pages", f"{timestamp}_{sanitized_base_url_name}")
    create_directory(pages_directory)

    base_html = download_page(base_url)
    if base_html is None:
        return

    # Embed CSS into the base page
    base_html_with_css = embed_css(base_url, base_html)
    save_html(base_html_with_css, os.path.join(pages_directory, 'index.html'))

    subpages = find_subpages(base_url, base_html, whitelist)
    print(f"Found subpages: {subpages}")  # Debugging statement

    for subpage_url in subpages:
        html_content = download_page(subpage_url)
        if html_content:
            # Embed CSS into the subpage
            html_with_css = embed_css(base_url, html_content)
            subpage_name = sanitize_directory_name(subpage_url.replace("https://", "").replace("http://", "").replace("/", "_"))
            subpage_path = os.path.join(pages_directory, f"{subpage_name}.html")
            save_html(html_with_css, subpage_path)
            print(f"Content of {subpage_url} is downloaded and saved.")

if __name__ == "__main__":
    base_url = ''
    whitelist = []

    main(base_url, whitelist)
