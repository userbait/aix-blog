import os
import sys

import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config

import advertools as adv
from urllib.parse import urlparse
import dns.resolver


def is_indexed(url):
    """
    구글 색인에 url이 등록되어 있는지 확인
    하루 쿼리 개수가 100개로 제한됨(전일 17:00 ~ 금일 17:00)
    :param url: String
    :return: boolean
    """

    cx = config.search_engine_id  # search_engine_id
    key = config.google_cloud_key  # API key for GOOGLE cloud project

    url = [url]

    search_query = adv.serp_goog(cx=cx, key=key, q=url)
    search_results = search_query[['searchTerms', 'title']]

    is_indexed_ = True
    for row in range(0, len(search_results)):
        # print(search_results['title'].iloc[row])
        if pd.isnull(search_results['title'].iloc[row]):
            is_indexed_ = False

    return is_indexed_


def has_dns_record(url):
    """
    url이 네트워크의 dns 서버에 등록되었는지 확인
    :param url: String
    :return: boolean
    """

    domain = urlparse(url).netloc  # domain name with subdomain if exists

    #  references : https://gist.github.com/akshaybabloo/2a1df455e7643926739e934e910cbf2e
    types = [
        'NONE', 'A', 'NS', 'MD', 'MF', 'CNAME', 'SOA',
        'MB', 'MG', 'MR', 'NULL', 'WKS', 'PTR', 'HINFO',
        'MINFO', 'MX', 'TXT', 'RP', 'AFSDB', 'X25', 'ISDN',
        'RT', 'NSAP', 'NSAP-PTR', 'SIG', 'KEY', 'PX', 'GPOS',
        'AAAA', 'LOC', 'NXT', 'SRV', 'NAPTR', 'KX', 'CERT',
        'A6', 'DNAME', 'OPT', 'APL', 'DS', 'SSHFP', 'IPSECKEY',
        'RRSIG', 'NSEC', 'DNSKEY', 'DHCID', 'NSEC3', 'NSEC3PARAM',
        'TLSA', 'HIP', 'CDS', 'CDNSKEY', 'CSYNC', 'SPF', 'UNSPEC',
        'EUI48', 'EUI64', 'TKEY', 'TSIG', 'IXFR', 'AXFR', 'MAILB',
        'MAILA', 'ANY', 'URI', 'CAA', 'TA', 'DLV',
    ]

    dns_record_num = 0
    for type_ in types:
        try:
            answers = dns.resolver.resolve(domain)
            dns_record_num += 1

        except Exception as e:
            print(e, ' for ', type_)

    has_dns_record_ = True
    if dns_record_num < 1:
        has_dns_record_ = False

    return has_dns_record_


if __name__ == '__main__':
    print(is_indexed('https://naalksdfj28ocnNCsed.com'))
