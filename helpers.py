import requests
from lxml import html


def parse_image_url(uri, base_url):
    if uri[0:4] != 'http':
        if uri[0] == '/':
            return base_url + uri
        else:
            return base_url + '/' + uri
    return uri


def is_logo(img_element):
    img_attrib = img_element.attrib
    for key in img_attrib.keys():
        if 'logo' in img_attrib[key]:
            return True
    return False


def valid_phone_number(phone_number):
    return 14 >= len([x for x in phone_number if x.isdigit()]) >= 10 \
           and ('+' not in phone_number or phone_number[0] == '+') \
           and ('()' not in phone_number) and ('((' not in phone_number) and ('))' not in phone_number)


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def load_data(filename):
    with open(filename) as f:
        reader = f.read()
        return list([x for x in reader.split('\n')])


def fetch_page_elements(url):
    page = requests.get(url)
    return html.fromstring(page.text)
