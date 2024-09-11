import os
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_html(content, path):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)

def get_lines_from_file(file_path):
    with open(file_path, 'r') as file:
        whitelist = file.read().splitlines()
    return whitelist

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

        # If the whitelist is empty, add all subpages
        if not whitelist:
            subpages.append(full_url)
        # Otherwise, check if the full URL ends with any of the whitelist items
        elif any(full_url.endswith(allowed_url) for allowed_url in whitelist):
            subpages.append(full_url)

    return list(set(subpages))  # removes duplicates

def sanitize_directory_name(name):
    # Remove leading slash if present
    if name.startswith("/"):
        name = name[1:]

    invalid_chars = [":", "*", "?", "\"", "<", ">", "|", "\\", "/"]
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

def convert_links_to_relative(base_url, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)

    for link in links:
        href = link['href']
        absolute_url = urljoin(base_url, href)
        
        # if the first char is a /, remove it
        local_filename = sanitize_directory_name(href)

        # If the local filename is empty, its the index page
        if local_filename == "":
            local_filename = "index"

        # Ignore third-party links
        if local_filename.startswith("http"):
            print(f"Skipping {absolute_url} as it is a third-party link.")
            continue

        # Update the href to the correct relative file path
        local_filename = f"./{local_filename}.html"
        link['href'] = local_filename

    return str(soup)

def get_args():
    parser = argparse.ArgumentParser(description="Download a website and its subpages")
    parser.add_argument("-url", "--base_url", help="Path to the base URL", required=True)
    parser.add_argument("-w", "--whitelist", help="Whitelist of URLs to download", nargs='+', default=[])
    parser.add_argument("-wf", "--whitelist_file", help="Path to a file containing URLs to download", default=None)
    parser.add_argument("-o", "--output", help="Output directory for the downloaded pages", default="")

    args = parser.parse_args()
    return args

def main(base_url, whitelist, pages_directory):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_base_url_name = sanitize_directory_name(base_url.replace("https://", "").replace("http://", "").replace("/", ""))

    if pages_directory == "":
        pages_directory = os.path.join("pages", f"{timestamp}_{sanitized_base_url_name}")
    else:
        pages_directory = os.path.join(pages_directory, f"{timestamp}_{sanitized_base_url_name}")

    create_directory(pages_directory)

    base_html = download_page(base_url)
    if base_html is None:
        return

    # Embed CSS into the base page
    base_html_with_css = embed_css(base_url, base_html)

    # Convert links to absolute paths with .html suffix
    base_html_with_links = convert_links_to_relative(base_url, base_html_with_css)
    save_html(base_html_with_links, os.path.join(pages_directory, 'index.html'))

    subpages = find_subpages(base_url, base_html, whitelist)
    print(f"Found subpages: {subpages}")  # Debugging statement

    for subpage_url in subpages:
        html_content = download_page(subpage_url)
        if html_content:
            # Embed CSS into the subpage
            html_with_css = embed_css(base_url, html_content)

            # Convert links to absolute paths with .html suffix
            html_with_links = convert_links_to_relative(base_url, html_with_css)

            subpage_name = sanitize_directory_name(subpage_url.replace(base_url, "").replace("/", "_"))
            subpage_path = os.path.join(pages_directory, f"{subpage_name}.html")
            save_html(html_with_links, subpage_path)
            print(f"Content of {subpage_url} is downloaded and saved.")

if __name__ == "__main__":
    args = get_args()

    if args.whitelist and args.whitelist_file:
        print("Please provide either a whitelist or a whitelist file, not both.")
        exit(1)

    base_url = args.base_url
    whitelist = args.whitelist
    pages = args.output

    if args.whitelist_file:
        whitelist = get_lines_from_file(args.whitelist_file)

    main(base_url, whitelist, pages)
