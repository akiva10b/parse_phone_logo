import concurrent.futures
import sys
import logging
from datetime import datetime
from traceback import format_exc

from helpers import is_logo, parse_image_url, valid_phone_number, chunks, load_data, fetch_page_elements


def fetch_logo_image(url, root):
    """
    :param url: Must be a url that can be scraped via requests module
    :param root: List of html elements
    :return: Website logo. Only elements of type <img> will be returned,
     the parser will not catch images in css background
    """
    image_elements = root.xpath('//img')
    for img in image_elements:
        if is_logo(img):
            uri = img.attrib.get('src')
            image_url = parse_image_url(uri, base_url=url)
            return image_url
    return "No logo found"


def extract_phone_numbers(text):
    """
    A function that parses text character by character to identify phone numbers
    :param text: Entire html element text
    :return: Valid phone numbers
    """
    phone_numbers = []
    record_phone_number = False
    phone_number = ''
    for char in text:
        if char in ['+', '('] or char.isdigit() or \
                (record_phone_number and char in [')', '-', '.']):
            record_phone_number = True
            if char not in ['-', '.']:
                phone_number = phone_number + char
        else:
            if record_phone_number and valid_phone_number(phone_number):
                phone_numbers.append(phone_number)
            record_phone_number = False
            phone_number = ''
    # if the loop has ended and the phone number is valid, record it
    if record_phone_number and valid_phone_number(phone_number):
        phone_numbers.append(phone_number)

    return phone_numbers


def fetch_phone_numbers(root):
    """
    :param root: List of html elements
    :return: List of phone numbers
    """
    elements = root.xpath('//*')
    phone_numbers = []
    for element in elements:
        if element.text:
            for phone_number in extract_phone_numbers(element.text):
                phone_numbers.append(phone_number)
    return phone_numbers


def run_phone_logo_parser(urls):
    """
    :param urls: list of urls to parse
    :return: prints json object containing pne numbers, logos and website
    """
    for url in urls:
        root = fetch_page_elements(url)
        logo = fetch_logo_image(url, root)
        phone_numbers = fetch_phone_numbers(root)
        print({
            "logo": logo,
            "phone_numbers": phone_numbers,
            "website": url
        })


def run(urls):
    """
    The function will run up to 10 parsers at a time, this can be a variable and can be optimized further
    """
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for u in chunks(urls, 10):
                executor.submit(run_phone_logo_parser, u)
    except Exception:
        e_data = format_exc()
        logging.error("Traceback:" + e_data)


if __name__ == "__main__":
    log_name = "logs/" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".log"
    logging.basicConfig(filename=log_name, filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
    if len(sys.argv) == 1:
        print("Please enter a file path")
    else:
        filename = sys.argv[1]
        urls_data = load_data(filename)
        run(urls_data)
