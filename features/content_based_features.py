import requests
from bs4 import BeautifulSoup


def get_nb_hyperlinks(url):
    """
    url html 파일의 <a> 개수 확인
    :param url: String
    :return: int, -1이 반환값이면 에러 의미
    """

    # 부적절한 input에 대한 validation
    try:
        headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
        html_content = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html_content, 'html.parser')

        nb_hyperlinks = len(soup.find_all('a'))

        return nb_hyperlinks
    except Exception as e:
        print(e)
        nb_hyperlinks = -1

        return nb_hyperlinks


if __name__ == '__main__':
    print(get_nb_hyperlinks('https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&sid1=001&sid2=140&oid=001&isYeonhapFlash=Y&aid=0013603471'))
