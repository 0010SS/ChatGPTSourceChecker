# ChatGPT SourceChecker

A program checking the validity of references created by ChatGPT. Powered by `python` and `scholarly`.

Recently when surfing China's social media, I found out that people are complaining about how ChatGPT creates false or "hallucinated" references, including references to both news articles and research articles. Hence, I decided to write this simple program to check the validity of sources returned by ChatGPT. 

近日在刷小红书的时候发现不少人在吐槽ChatGPT提供的学术引用是虚构的....... 因此决定写这个简单的Python程序来验证ChatGPT给提供引用的真实性（他们是否能在互联网上检索到）。

### Input

The main program asks you to enter **the path of the text file that stores ChatGPT's response**.

A typical file `Response.txt` might look like below:

```
Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention.
References:
1. Alpaydin, E. (2010). Introduction to machine learning (2nd ed.). Cambridge, MA: MIT Press.
2. Murphy, K. P. (2012). Machine learning: a probabilistic perspective (1st ed.). Cambridge, MA: MIT Press.
3. Bishop, C. M. (2006). Pattern recognition and machine learning (1st ed.). New York: Springer.
4. Hastie, T., Tibshirani, R., & Friedman, J. (2017). The elements of statistical learning: data mining, inference, and prediction (2nd ed.). New York: Springer.
5. Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep learning (1st ed.). Cambridge, MA: MIT Press.
1. Isaacson, Walter. "Steve Jobs." Simon and Schuster, 2011.
2. "Apple Inc. Form 10-K for the Fiscal Year Ended September 29, 2018." Securities and Exchange Commission, 2018.
3. "Apple: A History of Innovations." Apple, 2020.
4. "Apple Inc. SWOT Analysis." MarketLine, 2020.
```

The references could be either from a web article or a research article. But please format the reference as below (This is the typical reference format returned by ChatGPT):

* **For research articles:**

```
(Author's name). (year). (Title). (Place): (Press).
```

* **For web articles:**

```
(Author's name). "(Title)" (Publisher), (Year)
```

The author's name isn't compulsory.

### Output

The main program will then create a text file `result.txt` under the same directory as the program.

For references that are identified as genuine, the text file will provide the URLs to the references.

For references that are identified as hallucinated, the text file will provide the URL of the most relevant sources to the references.

A typical `result.txt` contains:

```
Conclusion for research article references (学术论文引用结果概述)：
  Genuine references (真实存在的引用): 
    -- Introduction to machine learning --
     https://www.cambridge.org/core/journals/knowledge-engineering-review/article/abs/introduction-to-machine-learning-second-editon-by-alpaydinethem-mit-press-584-pp-5500-isbn-978-0-262-01243-0/CFF344B73EA5CFA0205375212C1D4000
    -- Machine learning: a probabilistic perspective --
     https://books.google.com/books?hl=en&lr=&id=RC43AgAAQBAJ&oi=fnd&pg=PR7&dq=Machine+learning:+a+probabilistic+perspective&ots=ummyhFSxZ9&sig=Urlepwny6uS7yeXthvGWUJvVNZU
    -- Pattern recognition and machine learning --
     https://link.springer.com/book/9780387310732
    -- Deep learning --
     https://books.google.com/books?hl=en&lr=&id=omivDQAAQBAJ&oi=fnd&pg=PR5&dq=Deep+learning&ots=MNT2ivsIPT&sig=-FEEoGUpvg6VB6oBZPCdjH-VcQY
  Fake references (检索不到的引用): 
    -- The elements of statistical learning: data mining, inference, and prediction --
      https://link.springer.com/book/10.1007/978-0-387-21606-5
Conclusion for web article references (网络文章引用结果概述)：
  Genuine references (真实存在的引用): 
    -- Steve Jobs --
     https://www.amazon.com/Steve-Jobs-Walter-Isaacson/dp/1451648537
  Fake references (检索不到的引用): 
    -- Apple Inc. Form 10-K for the Fiscal Year Ended September 29, 2018 --
     https://www.sec.gov/Archives/edgar/data/320193/000032019318000145/a10-k20189292018.htm
    -- Apple: A History of Innovations --
     https://www.apple.com/environment/pdf/Apple_Environmental_Progress_Report_2020.pdf
    -- Apple Inc. SWOT Analysis --
     https://store.marketline.com/report/apple-inc-strategy-swot-and-corporate-finance-report-3/
```

## Download 

#### 1. Python Program (Recommended)

* **if you have a Python3 interpreter on your computer**

Clone/download this repository, download the related libraries, and run `main.py`.

#### 2. Application (Testing)

For **Mac Users**

* download a ZIP of this repository at Release, and run `MacChatGPTSourceChecker.app`. It will open a terminal window. Please wait for some moments... The program takes a long time to start and run as it and its dependencies are all published onto a single file.

For **Win Users**

* download a ZIP of this repository at Release, and run `WinChatGPTSourceChecker.app`. It will open a terminal window. Please wait for some moments... The program takes a long time to start and run as it and its dependencies are all published onto a single file.

## Issues

* If the program returns an error, it could be...

##### 1. File path not found

* Please ensure the path of the text file you inputted is correct.

##### 2. Reference format not supported

* Please ensure the references are in the correct formats as mentioned above.

##### 3. Connection Error / Max number of retries exceeded

* Please ensure that your internet is well-connected, and try more times...

Sorry for this buggy version. Are there other ways to make my published application lighter and faster? Thanks.