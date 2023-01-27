"""Implements the ChatGPT Source Checker"""
import re
from scholarly import scholarly
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote, urlparse


class SourceChecker:
    """
    This class implements the ChatGPT Source Checker.

    Arg:
        path: the path of the file that stores ChatGPT's response
            - the file must contain the references after keywords "Reference:" or "References:"
            - example:
                References:
                    1. Alpaydin, E. (2010). Introduction to machine learning (2nd ed.). Cambridge, MA: MIT Press.
                    2. Bishop, C. M. (2006). Pattern recognition and machine learning (1st ed.). New York: Springer.
                    3. "WeChat: The Chinese App That's Eating the World." Forbes, 2018.
                    4. "WeChat: The App Changing China's Online Landscape." BBC, 2016.
                    5. "WeChat: The App That's Taking Over China." Business Insider, 2015.

    Procedure:
        1. Read ChatGPT's response from a file (default "Response.txt" under the same directory)
        2. Parse the output to obtained the references made by ChatGPT
            - if no references mentioned, return
        3. Check whether the article is from a website or a research/textbook
        4. Extract the content of each source into a dictionary
            - the references could be either from a website or a research article
            - extract the date, title and author
        5. Check the validity of each reference
            - scrawl Google Scholar for research articles
            - Raw google search for web articles
                * the web article might not exist, so recommend the most similar reference

    Return:
        output the validity of each reference made by ChatGPT.
    """

    def __init__(self, path):
        references = self.loadSources(path)
        web, research = self.parseSources(references)
        research_res = self.queryResearch(research, 5)
        print(research_res)
        web_res = self.queryWeb(web, 5)
        print(web_res)

    @staticmethod
    def loadSources(path):
        # read in the file
        with open(path, "r") as file:
            texts = file.readlines()
            file.close()

        sources = []

        # extract the references
        for i in range(len(texts)):
            if "reference:" in texts[i].lower() or "references:" in texts[i].lower():
                sources = texts[i + 1:]
                break

        if not sources:
            raise Exception("Missing keyword: "
                            "The inputted response doesn't contain the keywords 'reference:' or 'references:'")

        # filter the sources to avoid \n or null string
        string_filter = lambda x: not x == "\n" and not x == ""
        sources = list(filter(string_filter, sources))

        return sources

    @staticmethod
    def parseSources(sources):

        web, research = [], []

        for source in sources:
            # delete the indices at the beginning (if any)
            num_filter = lambda x: x.isalpha() or x == "\""
            i = source.find(next(filter(num_filter, source)))
            plain_source = source[i:]

            # categorize the sources
            web_regex1 = re.compile(r'(.+). "(.+)." (.+), (\d{4}).')
            web_regex2 = re.compile(r'"(.+)." (.+), (\d{4}).')
            research_regex = re.compile(r'(.+). \((\d{4})\). (.+)\. (.+): (.+).')

            match = None
            for i, regex in enumerate([web_regex1, web_regex2, research_regex]):
                match = regex.search(plain_source)
                if match:
                    if i == 0:
                        web.append({
                            "title": match.groups()[1],
                            "publisher": match.groups()[2],
                            "author": match.groups()[0],
                            "year": match.groups()[3]
                        })
                    elif i == 1:
                        web.append({
                            "title": match.groups()[0],
                            "publisher": match.groups()[1],
                            "author": "",
                            "year": match.groups()[2]
                        })
                    else:
                        research.append({
                            "title": match.groups()[2],
                            "publisher": match.groups()[4],
                            "author": match.groups()[0],
                            "year": match.groups()[1]
                        })
                    break
            else:  # cannot parse the reference
                raise Exception(f"The reference ({plain_source}) is in an unknown format.")

        return web, research

    @staticmethod
    def queryResearch(sources, count):

        research_result = []

        for source in sources:
            # clean the edition mark
            if "ed." in source['title']:
                title = re.search("(.+) \(", source['title'])
                title = title.group(1)
            else:
                title = source['title']

            # query scholarly
            results = scholarly.search_pubs(title, citations=False, year_low=source['year'], year_high=source['year'])

            # parse the output and compare
            match = False
            author = source['author'].split(",")
            author = author[0]
            for counter, result in enumerate(results):
                if title.lower() in result['bib']['title'].lower():
                    for person in result['bib']['author']:
                        if author in result['bib']['title'] or author in person:
                            # this reference is genuine
                            research_result.append({
                                "title": title,
                                "status": True,
                                "url": result['pub_url']
                            })
                            match = True
                            break
                if match:
                    break

                if counter == count:
                    break

            if not match:
                # find the best match
                nearest_result = scholarly.search_single_pub(title)
                research_result.append({
                    "title": title,
                    "status": False,
                    "url": nearest_result['pub_url']
                })

        return research_result

    # TODO: query google search and check whether the reference website exists
    def queryWeb(self, sources, count):

        web_result = []

        for source in sources:
            # init
            query = source['title'] + " " + source['author'] + source['publisher'] + source['year']
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/47.0.2526.106 Safari/537.36'}
            response = ""

            # query
            try:  # try google
                url = f"https://www.google.com/search?q={quote(query)}&oq=google+robots.txt&aqs=chrome.0" \
                      f".0i512l3j0i30i625l4j69i60.3955j0j4&sourceid=chrome&ie=UTF-8 "

                response = requests.get(url, headers=headers).text

                # parse output
                soup = BeautifulSoup(response, "lxml")
                headings = soup.find_all("h3")

                for counter, heading in enumerate(headings):
                    if source['title'] in heading.getText():
                        if source['title'] in heading.getText():
                            web_result.append({
                                "title": source['title'],
                                "status": False,
                                "url": self.GoogleHTML2URLs(soup)[counter]
                            })
                        break

                    if counter == count:
                        web_result.append({
                            "title": source['title'],
                            "status": False,
                            "url": self.GoogleHTML2URLs(soup)[0]
                        })
                        break

            # if google fails, try bing
            except:
                url = f"https://www.bing.com/search?q={quote(query)}&qs=n&form" \
                      f"=QBRE&sp=-1&pq=&sc=0-0&sk=&cvid=69C9D9AE5AC64773BB29D000B4D28FC7&ghsh=0&ghacc=0&ghpl= "

                response = requests.get(url, headers=headers).text

                # parse output
                soup = BeautifulSoup(response, "lxml")
                headings = soup.find_all("h2")

                for counter, heading in enumerate(headings):
                    if source['title'] in heading.getText():
                        # the source might come from bing.com/videos, which is unfavourable
                        url = soup.find_all("cite")[counter].getText()
                        if "bing.com" in url:
                            continue

                        web_result.append({
                            "title": source['title'],
                            "status": True,
                            "url": url
                        })
                        break

                    if counter == count:
                        web_result.append({
                            "title": source['title'],
                            "status": False,
                            "url": soup.find_all("cite")[0].getText()
                        })
                        break

        return web_result

    @staticmethod
    def GoogleHTML2URLs(soup):

        urls = []

        # extract the urls
        a = soup.find_all('a')
        for i in a:
            k = i.get('href')

            try:
                m = re.search("(?P<url>https?://[^\s]+)", k)
                n = m.group(0)
                url = n.split('&')[0]
                domain = urlparse(url)
                if re.search('google.com', domain.netloc):  # if the url domains in Google, exclude it
                    continue
                else:
                    urls.append(url)

            except BaseException:
                continue

        return urls


test = SourceChecker('Response.txt')
