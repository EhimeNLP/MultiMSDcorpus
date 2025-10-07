import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import os
import time
from playwright.sync_api import sync_playwright, TimeoutError, Page

BASE_URL = "https://www.msdmanuals.com"
TOPICS_URL = f"{BASE_URL}/professional/health-topics"

OUTPUT_DIR = "raw_data"

LANG_LIST = ["de", "en", "es", "fr", "it", "pt", "ru", "zh"]
ALL_LANGS = ["ja"] + LANG_LIST

# Mapping from the visible text in the language dropdown menu to language codes
# This is used by Playwright to find and click the correct language link.
# Excludes English (base language) and Chinese (handled with a special rule).
LANG_TEXT_MAP = {
    "日本語 (JAPANESE)": "ja",
    "DEUTSCH (GERMAN)": "de",
    "ESPAÑOL (SPANISH)": "es",
    "FRANÇAIS (FRENCH)": "fr",
    "ITALIANO (ITALIAN)": "it",
    "PORTUGUÊS (PORTUGUESE)": "pt",
    "РУССКИЙ (RUSSIAN)": "ru",
}

# Finds the 'relatedLinks' in the page source to get the consumer (amateur) version URL.
RE_RELATED_LINKS = re.compile(r'"relatedLinks":\["(.*?)"\]')
# Extracts topic URLs from the __NEXT_DATA__ script tag on section pages.
RE_TOPIC_URL = re.compile(r'"TopicUrl":{"path":"(.*?)"}')


def get_data(section_index: int, topic_index: int, pro_soup: BeautifulSoup, ama_soup: BeautifulSoup, lang: str):
    # --- Process the Professional version page ---
    previous_line = ""
    # Remove unwanted elements like lists, section heads, and tables to clean the text.
    for ul in pro_soup.find_all('ul'): ul.decompose()
    for ol in pro_soup.find_all('ol'): ol.decompose()
    for sec in pro_soup.find_all(class_='TopicFHead_topicFHeadTitle__pl6da'): sec.decompose()
    for table in pro_soup.find_all('div', {'data-testid': 'baseillustrative', 'class': 'undefined professional false false'}): table.decompose()
    
    # Select only the desired text-containing elements.
    elements = pro_soup.select('span.TopicPara_topicText__CUB0d, span.TopicXLink_formatText__5UPAp, a[class*=professional]')

    pro_filepath = os.path.join(OUTPUT_DIR, lang, "professional", f"section{section_index+1}", f"{section_index+1}-{topic_index+1}.pro")
    with open(pro_filepath, "w", encoding="utf-8") as output_file:
        for element in elements:
            element_str = element.decode()
            text_data = re.sub("<.+?>", "", element_str).strip()
            if text_data and text_data != previous_line:
                output_file.write(text_data+"\n")
                previous_line = text_data

    # --- Process the Consumer (amateur) version page ---
    previous_line = ""
    for ul in ama_soup.find_all('ul'): ul.decompose()
    for ol in ama_soup.find_all('ol'): ol.decompose()
    for sec in ama_soup.find_all(class_='TopicFHead_topicFHeadTitle__pl6da'): sec.decompose()
    for table in ama_soup.find_all('div', {'data-testid': 'baseillustrative', 'class': 'undefined consumer false false'}): table.decompose()
    
    elements = ama_soup.select('span.TopicPara_topicText__CUB0d, span.TopicXLink_formatText__5UPAp, a[class*=home]')
    
    ama_filepath = os.path.join(OUTPUT_DIR, lang, "amateur", f"section{section_index+1}", f"{section_index+1}-{topic_index+1}.ama")
    with open(ama_filepath, "w", encoding="utf-8") as output_file:
        for element in elements:
            element_str = element.decode()
            text_data = re.sub("<.+?>", "", element_str).strip()
            if text_data and text_data != previous_line:
                output_file.write(text_data+"\n")
                previous_line = text_data


def get_all_language_urls(page: Page, start_en_url: str):
    found_urls = {"en": start_en_url}
    try:
        # Manually construct the Chinese URL since it uses a different TLD (.cn)
        found_urls['zh'] = start_en_url.replace(".com/", ".cn/", 1)

        # Use Playwright to find the URLs for all other languages.
        for lang_text, lang_code in LANG_TEXT_MAP.items():
            try:
                page.goto(start_en_url, wait_until='networkidle', timeout=60000)
                try:
                    page.click("#onetrust-accept-btn-handler", timeout=3000)
                    time.sleep(1)
                except TimeoutError:
                    pass
                
                page.click('#langswitcherDropdown', timeout=15000)
                with page.expect_navigation(wait_until="networkidle", timeout=60000):
                    page.get_by_text(lang_text, exact=True).click(timeout=10000)
                
                found_urls[lang_code] = page.url
            except Exception:
                continue
    except Exception:
        pass
    return found_urls


def jump_ama_page(page: Page, section_index: int, topic_index: int, topic_path: str):
    en_pro_url = f"{BASE_URL}{topic_path}"

    # Get the list of all language URLs using Playwright.
    all_lang_urls = get_all_language_urls(page, en_pro_url)
    if not all_lang_urls:
        return

    # Scrape the professional/consumer page pair for each language found.
    for lang, pro_url in all_lang_urls.items():
        try:
            lang_pro_bytes = urllib.request.urlopen(pro_url).read()
            lang_pro_soup = BeautifulSoup(lang_pro_bytes, "html.parser")

            lang_ama_urls = RE_RELATED_LINKS.findall(lang_pro_soup.decode())
            if not lang_ama_urls:
                continue
            
            lang_ama_url = lang_ama_urls[0].replace("localhost", "msdmanuals.com")
            if lang == 'zh':
                lang_ama_url = lang_ama_url.replace(".com/", ".cn/", 1)
            
            lang_ama_url_encoded = urllib.parse.quote(lang_ama_url, safe=':/')
            
            lang_ama_bytes = urllib.request.urlopen(lang_ama_url_encoded).read()
            lang_ama_soup = BeautifulSoup(lang_ama_bytes, "html.parser")

            if RE_RELATED_LINKS.search(lang_ama_soup.decode()):
                get_data(section_index, topic_index, lang_pro_soup, lang_ama_soup, lang)
        except Exception:
            continue
        
        time.sleep(1)


def jump_column(page: Page, section_index: int, section_path: str):
    # Get the HTML of the main section page.
    content_bytes = urllib.request.urlopen(f"{BASE_URL}{section_path}").read()
    soup = BeautifulSoup(content_bytes, "html.parser")

    # Extract all topic URLs contained within that section.
    script_tag = soup.select_one('script[id="__NEXT_DATA__"]')
    topic_paths = RE_TOPIC_URL.findall(script_tag.decode())
    
    for topic_index, path in enumerate(topic_paths):
        jump_ama_page(page, section_index, topic_index, path)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            content_bytes = urllib.request.urlopen(TOPICS_URL).read()
            soup = BeautifulSoup(content_bytes, "html.parser")
        except Exception:
            browser.close()
            return
        
        section_links = soup.select('.SectionList_sectionListItem__NNP4c')
        
        for section_index, link_tag in enumerate(section_links):
            try:
                for lang in ALL_LANGS:
                    os.makedirs(os.path.join(OUTPUT_DIR, lang, "professional", f"section{section_index+1}"), exist_ok=True)
                    os.makedirs(os.path.join(OUTPUT_DIR, lang, "amateur", f"section{section_index+1}"), exist_ok=True)            
                
                section_path_tag = link_tag.select_one('a[href]')
                if section_path_tag:
                    section_path = section_path_tag.get('href')
                    jump_column(page, section_index, section_path)
            except Exception:
                continue
        
        browser.close()


if __name__ == '__main__':
    main()
