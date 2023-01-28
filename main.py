"""Main program here"""
from SourceChecker import SourceChecker
import ssl


def main():

    # query the class to receive the output
    path = input("Please input the file's path (请输入文件路径)：")

    print("Processing (正在处理中)...")

    checker = SourceChecker(path)
    research_res, web_res = checker.research_res, checker.web_res

    # lists that store the conclusion to be outputted
    research_con = ["Conclusion for research article references (学术论文引用结果概述)：\n"]
    web_con = ["Conclusion for web article references (网络文章引用结果概述)：\n"]

    # categorize
    true_research = [source for source in research_res if source['status']]
    false_research = [source for source in research_res if not source['status']]

    true_web = [source for source in web_res if source['status']]
    false_web = [source for source in web_res if not source['status']]

    # handle the output
    research_con.append("  Genuine references (真实存在的引用): \n")
    for reference in true_research:
        research_con.append("    -- " + reference['title'] + " --\n")
        research_con.append("     " + reference['url'] + "\n")

    research_con.append("  Fake references (检索不到的引用): \n")
    for reference in false_research:
        research_con.append("    -- " + reference['title'] + " --\n")
        research_con.append("      " + reference['url'] + "\n")

    if web_res:
        web_con.append("  Genuine references (真实存在的引用): \n")
        for reference in true_web:
            web_con.append("    -- " + reference['title'] + " --\n")
            web_con.append("     " + reference['url'] + "\n")

        web_con.append("  Fake references (检索不到的引用): \n")
        for reference in false_web:
            web_con.append("    -- " + reference['title'] + " --\n")
            web_con.append("     " + reference['url'] + "\n")
    else:
        web_con.append("Fails to produce an output. Please try connecting to other proxy servers...")

    with open("Result.txt", "w") as file:
        file.writelines(research_con + web_con)
        file.close()

    print("Processing succeeds. Please find the Result.txt file under the current directory.")
    print("(处理结束，请找到此路径下的Response.txt)")


if __name__ == "__main__":
    main()