"""Implements the ChatGPT Source Checker"""
import re
import urllib

class SourceChecker:
    """
    This class implements the ChatGPT Source Checker.

    Arg:
        path: the path of the file that stores ChatGPT's response
            - the file must contain the references after keywords "Reference:" or "References:"
            - example:
                References:
                    1. "WeChat: The Complete Guide." TechNode, 2020.
                    2. "WeChat: The Rise of China's All-in-One Super App." The Economist, 2020.
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

    Return:
        output the validity of each reference made by ChatGPT.
    """

    def __init__(self, path):
        references = self.loadSources(path)
        web, research = self.parseSources(references)
        print(web)
        print(research)

    @staticmethod
    def loadSources(path):
        # read in the file
        with open(path, "r") as file:
            texts = file.readlines()
            file.close()

        sources = []
        print(texts)

        # extract the references
        for i in range(len(texts)):
            if "reference:" in texts[i].lower() or "references:" in texts[i].lower():
                sources = texts[i + 1:]
                break

        if not sources:
            raise Exception("Missing keyword: "
                            "The inputted response doesn't contain the keywords 'reference:' or 'references:'")

        return sources

    @staticmethod
    def parseSources(sources):
        web, research = [], []

        for source in sources:
            # delete the indices at the beginning (if any)
            num_filter = lambda x: x.isalpha() or x == "\""
            i = source.find(next(filter(num_filter, source)))
            plain_source = source[i:]
            print(plain_source)

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
                            "author": None,
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
            else:
                raise Exception(f"The reference ({plain_source}) is in an unknown format.")

        return web, research

    # TODO: query google scholar and check whether the reference article exists
    @staticmethod
    def queryResearch(sources):
        pass

    # TODO: query google search and check whether the reference website exists
    @staticmethod
    def queryWeb(sources):
        pass


test = SourceChecker('Response.txt')