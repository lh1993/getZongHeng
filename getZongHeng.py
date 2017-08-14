# -*- coding:utf-8 -*-

import urllib2, re, os
import HTMLParser
# import sys
# reload(sys)
# sys.setdefaultcoding('utf-8')

# 获取纵横网主页的网页源码
def getHtml(url):
    Heasers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.7 Safari/537.36'}
    request = urllib2.Request(url, headers=Heasers)
    response = urllib2.urlopen(request)
    html = response.read()
    return html

# 获取免费小说超链接
def getHref(html):
    pattern = re.compile('<a class="fb" href="(.*?)">免费小说</a>')
    href = re.findall(pattern, html)
    # print href[0]
    return href[0]

# 获取免费小说新书榜中书名的超链接
def getBookHref(url):
    html = getHtml(url)
    pattern = re.compile('<em class=".*?" bookId=".*?" order=".*?">.*?</em><a class=".*?" href=".*?"></a><a href="(.*?)" title=".*?" target="_blank">.*?</a></li>')
    items = re.findall(pattern, html)
    # for item in items:
    #     print item
    return items

# 获取书名
def getBookName(href):
    html = getHtml(href)
    pattern = re.compile('<body monkeyId=".*?" scriptSign="book" bookId=".*?" bookName="(.*?)"')
    items = re.findall(pattern, html)
    # print items[0]
    return items[0]

# 获取小说简介
# def getBookIntro(href):
#     html = getHtml(href)
#     # print html
#     pattern = re.compile('<div class="info_con"><p>(.*?)</p></div>')
#     items = re.findall(pattern, html)
#     print items

# 获取小说目录超链接
def getBookCatalogHref(href):
    html = getHtml(href)
    pattern = re.compile('<span class="btn_as list"><a href="(.*?)"')
    items = re.findall(pattern, html)
    # print items
    return items[0]

# 获取小说章节超链接
def getSectionHref(href):
    html = getHtml(href)
    pattern = re.compile('<td class="chapterBean" chapterId=".*?" chapterName=".*?" chapterLevel=".*?" wordNum=".*?" updateTime=".*?"><a href="(.*?)"')
    items = re.findall(pattern, html)
    # print items
    return items

# 获取章节名称
def getSectionName(href):
    html = getHtml(href)
    pattern_name = re.compile('<h1><em itemprop="headline">(.*?)</em></h1>')
    items_name = re.findall(pattern_name, html)

    # pattern_content = re.compile('<div id="readerFs" class=""><script>.*?</script>(.*?)</div>')
    # items_content = re.findall(pattern_content, html)

    # print items_name[0]
    return items_name[0]

# 获取章节内容
def getSectionContent(href):
    html = getHtml(href)
    pattern = re.compile('<div id="readerFs" class="">(.*?)</div>', re.S)
    items = re.findall(pattern, html)
    # print items[0]
    item = htmlFilter(items[0])
    # print item[0]
    return item

def htmlFilter(html):
    htmlParser = HTMLParser.HTMLParser()
    pattern = re.compile('<p>(.*?)</p>', re.S)
    items = re.findall(pattern, html)
    result = []
    for item in items:
        if item != '':
            html_tag = re.search('&', item)
            if html_tag:
                item = htmlParser.unescape(item)
                result.append(item)
            else:
                result.append(item)
    return result

def main():
    novel = open('novel.txt', 'wb')
    novel.write("##### 纵横网小说新书前15名排行榜 #####" + os.linesep)
    url = "http://www.zongheng.com"
    html = getHtml(url)
    freebookhrefs = getHref(html)
    bookhreks = getBookHref(freebookhrefs)
    num = 1

    for bookhrek in bookhreks:
        bookname = getBookName(bookhrek)
        novel.write(str(num) + '、' + bookname + os.linesep)
        num += 1
        if num == 16:
            novel.write('#'*10 + ' 小说部分 ' + '#'*10 + os.linesep)

    for bookhrek in bookhreks:
        try:
            bookname = getBookName(bookhrek)
            novel.write(os.linesep * 2)
            novel.write('######### ' + bookname + ' #########' + os.linesep)
            BookCatalogHref = getBookCatalogHref(bookhrek)
            SectionHrefs = getSectionHref(BookCatalogHref)
            for SectionHref in SectionHrefs:
                novel.write(os.linesep)
                SectionName = getSectionName(SectionHref)
                print SectionName
                novel.write('### ' + SectionName + ' ###' + os.linesep)
                SectionContents = getSectionContent(SectionHref)
                for SectionContent in SectionContents:
                    print SectionContent
                    novel.write(SectionContent + os.linesep)
                novel.write('#' * 136 + os.linesep)

        except Exception, e:
            print e

    novel.close()

if __name__ == '__main__':
    main()
