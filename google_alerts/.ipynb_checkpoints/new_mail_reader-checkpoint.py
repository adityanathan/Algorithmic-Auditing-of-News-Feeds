# Earliest Date on which alert was received- Feb 26, 2019

import imaplib
import email
import pprint
from bs4 import BeautifulSoup as BS
import newspaper
from newspaper import Article
from pymongo import MongoClient
from  bson import objectid
import itertools
import pickle
from datetime import date, timedelta
import time

def daterange(date1=date(2019, 2, 26), date2=date.today()):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def get_body(b): #b=email_message_instance
    body = ""
    if b.is_multipart():
        for part in b.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
    # not multipart - i.e. plain text, no attachments, keeping fingers crossed
    else:
        body = b.get_payload(decode=True)
    return body

def extractURL(body):
    #list of lines in body text
    body_l=body.split('\n')
    url_list=[]
    #Extract the very first hyperlink from body text (rest are generally not required)
    for line in body_l:
        if ('https://' in line or 'http://' in line) and '&url' in line:
            url=line.replace('<','')
            url=url.replace('>','')
            url_list.append(url)

    return url_list

def extract_article(url_list):
    headline = []
    body = []
    urls = []
    # f_url=open("filtered_urls.txt",'w')
    for url_one in url_list:
        try:
            pos_start = url_one.find('&url=')
            pos_end = url_one.find('&ct')
            url_one = url_one[(pos_start+5):pos_end] #cleaning the url
            # print(url_one)
            article = Article(url=url_one)
            article.download()
            article.parse()
            headline.append(article.title)
            body.append(article.text)
            urls.append(url_one)
            # pp = pprint.PrettyPrinter(indent=4, stream=f_url)
            # pp.pprint(url_one)

        except Exception as e:
            f_exception = open("errors_url.txt",'a')
            pp = pprint.PrettyPrinter(indent=4, stream=f_exception)
            pp.pprint("Exception with URL:"+url_one)
            pp.pprint(str(e))
            f_exception.close()
            continue
    # f_url.close()
#     return [headline,body,urls]
    return list(zip(headline,body,urls))

def get_mail():
    # Extracts mail body and crawls it to find urls and enters
    #   urls and extracts heading and article body and source url.

    # Dumps list of headings, list of corresponding article bodies,
    #   list of corresponding source urls
    pp = pprint.PrettyPrinter(indent=4)

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('act4dnewsapp@gmail.com', 'change!me')
    mail.select("inbox") # connect to inbox.
    
    _, temp = mail.uid('search', None, "ALL")
    len_mail = len(temp[0].decode('utf-8').split())

    f = open('articles.pkl','wb')
    
    for dt in daterange():
    #    for dt in daterange():
            dt_str = dt.strftime("%d-%b-%Y")
            resp, data = mail.search(None, "(ON "+dt_str+")".format(time.strftime("%d-%b-%Y")))
            mail_ids = data[0]
            uid_list = mail_ids.split()
            uid_list = [int(i) for i in uid_list]
            print('Date:', dt_str)

            for uid in uid_list:
                try:
                    pp.pprint("Downloading Mail No: "+str(uid)+" / "+str(len_mail))

                    result, data = mail.fetch(str(uid), '(RFC822)')
                    raw_email = data[0][1]
                    email_message = email.message_from_bytes(raw_email)

                    body = get_body(email_message).decode("utf-8")

                    url_list = extractURL(body)
                    articles = extract_article(url_list)

                    for h, art_bod, ur in articles:
                        pickle.dump((dt_str,h,art_bod,ur),f)

                except Exception as e:
                    pp.pprint("EXCEPTION!")
                    pp = pprint.PrettyPrinter(indent=4,stream=f_exception)
                    pp.pprint("Exception with Email_UID:"+str(uid))
                    pp.pprint(str(e))
                    pp = pprint.PrettyPrinter(indent=4)

                    mail = imaplib.IMAP4_SSL('imap.gmail.com')
                    print(mail.login('act4dnewsapp@gmail.com', 'change!me'))
                    print(mail.select("inbox")) # connect to inbox.
    f_exception.close()
    f.close()
    return 1

if __name__ == '__main__':
    get_mail()