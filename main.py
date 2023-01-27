"""Main program here"""
from SourceChecker import SourceChecker


def main():
    # query the class to receive the output
    path = input("Please input the file's path (请输入文件路径)：")
    research_res, web_res = SourceChecker(path)

    # lists that store the conclusion to be outputted
    research_con = ["Conclusion for research article references (学术论文引用结果概述)："]
    web_con = ["Conclusion for web article references (网络文章引用结果概述)："]

    # handle the output
    for index, source in enumerate(research_res):
        if source["status"]:
            research_con.append()
