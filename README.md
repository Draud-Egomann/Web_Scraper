# Web_Scraper
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/downloads/release/python-3121/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.12.3-blue.svg)](https://pypi.org/project/beautifulsoup4/)
[![Requests](https://img.shields.io/badge/Requests-2.32.3-blue.svg)](https://pypi.org/project/requests/)


This web scraper allows you to download a website, including CSS and Navigation. This tool is ideal for creating offline versions of websites for archival or local browsing purposes.

## Prerequisites
- [Python 3.x](https://www.python.org/downloads/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [Requests](https://pypi.org/project/requests/)

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/Draud-Egomann/Web_Scraper.git
   cd web_scraper
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To download a website's pages, run the script with the following options:

```bash
python main.py -url <base_url> [-w <whitelist>] [-wf <whitelist_file>] [-o <output_directory>]
```

- `-url` or `--base_url`: The base URL of the website to download (required).
- `-w` or `--whitelist`: A list of subpage paths or URLs to whitelist (optional, default: `[]`).
- `-wf` or `--whitelist_file`: A file containing the whitelist URLs (optional, default: `None`).
- `-o` or `--output`: The directory where the downloaded pages will be saved (optional, default: `pages`).

## Example

**Download a website in custom output directory:**
```bash
python main.py -url https://example.com -o mywebsite
```

**Download a website with a whitelist:**
```bash
python main.py -url https://www.iana.org -w /domains /about
```

## Important Notes
- In the current state, the scraper only downloads subpages, whose links are in the base_url
- Only subpages matching the base URL and whitelist are downloaded. Third-party links are skipped.