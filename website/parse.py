from lxml import etree
import requests
import json
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


parse_date_stamp = datetime.date.today().strftime('%Y-%m-%d')


def parse(xml, timestamp, date_stamp=parse_date_stamp):
    """A function for parsing the list of XML objects returned by the consume function. 
    Returns a list of Json objects in a format that can be recognized by the OSF scrapi."""
    terms_url = 'http://purl.org/dc/terms/'
    elements_url = 'http://purl.org/dc/elements/1.1/'
    record = etree.XML(xml)
    json_scrapi = {
        'title': record.find(str(etree.QName(elements_url, 'title'))).text,
        'contributors': record.find(str(etree.QName(elements_url,'creator'))).text,
        'properties': {
            'doi': record.find(str(etree.QName(elements_url,'doi'))).text,
            'description': record.find(str(etree.QName(elements_url,'description'))).text,
            'article_type': record.find(str(etree.QName(elements_url,'type'))).text,
            'url': record.find(str(etree.QName(terms_url,'identifier-purl'))).text,
            'date_entered': record.find(str(etree.QName(elements_url,'dateEntry'))).text,
            'research_org': record.find(str(etree.QName(terms_url,'publisherResearch'))).text,
            'research_sponsor': record.find(str(etree.QName(terms_url, 'publisherSponsor'))).text,
            'tags': record.find(str(etree.QName(elements_url, 'subject'))).text,
            'date_retrieved': date_stamp,
            'date_published': record.find(str(etree.QName(elements_url, 'date'))).text
        },
        'meta':{},
        'id': record.find(str(etree.QName(elements_url, 'ostiId'))).text,
        'source':'SciTech'
    }
    payload = {
        'doc': json.dumps(json_scrapi),
        'timestamp': timestamp
    }
    return requests.get('http://0.0.0.0:1337/process', params=payload) 


def json_to_text(json_scrapi, date_time=parse_date_stamp):
    """A function to help with debugging. Saves Json produced by parsing XML as a file."""
    with open('SciTech_parsed_'+date_time+'.json', 'w') as json_txt:
        json.dump(json_scrapi, json_txt, indent=4, sort_keys=True)
