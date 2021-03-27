# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import libraries


import sys
import urllib.request
import urllib.parse
import re
from urllib.request import urlopen as ureqs
from bs4 import BeautifulSoup 
from googleapiclient.discovery import build
import pandas as pd
import numpy as np
import time
import random
import tweepy

# We put all the data in Twitter_Project
file = "/Users/louismockly/Documents/Twitter_Project/"

#twitter API

# Authenticate to Twitter
auth = tweepy.OAuthHandler("rAFLBz580J8s5ZCHdQHlTvTko", "ahdFYPOQgpBvfr6PEjMWKi8eyxcRtCarW08GUjpSrGCbIZcrlO")
auth.set_access_token("1493414900-vPziDbiHiQtJosGJu3TgUVCXne3wEjt5Jp0mxLB", 
                      "GwiT12EGANkcuWrPRs8mypOGOZmjXhGjdedMKwKWDtjHf")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

#We modifye the list in a clean dataframe

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def return_dataframe_list_name_domain():
    
    #We import the list truncated !
    res = pd.read_csv(file + "authors_names.csv",
                      sep='delimiter', header=None)
    res.columns = ['data']
    res = res.drop(res.index[0])
    res = res[res.data != ';']
    # Clean the data 
    list_names, list_firstnames, list_domain = [], [], []
    for text in res.values:
        pos = findOccurrences(text[0], ',')[1]
        dom = findOccurrences(text[0], ',')[0]
        mod_text = text[0][pos + 1:-1]
        virg = mod_text.find(',')
        list_names += [mod_text[:virg]]
        list_firstnames += [mod_text[virg + 1:]]
        list_domain += [text[0][:dom]]
        
        
    df_names = pd.DataFrame(list_names)
    df_firstnames = pd.DataFrame(list_firstnames)
    df_domain = pd.DataFrame(list_domain)
    df_final = pd.concat([df_names, df_firstnames, df_domain], 1)
    df_final.columns = ['names', 'firstnames', 'domain']   
        
    used = set()
    unique = [x for x in list_domain if x not in used and (used.add(x) or True)]
    
    # We import the excel with the new domains
    df_domain_bis = pd.read_excel(file+"domain_bis.xlsx")
    list_occurence = [list_domain.count(item) for item in unique]
    list_domain_mod = []
    i = 0
    for nb in list_occurence:
        list_domain_mod += nb*[df_domain_bis['domain'][i]]
        i += 1
    
    # And we build the final dataframe
    df_final_bis = df_final.copy().drop(['domain'], 1)
    df_domain_mod = pd.DataFrame(data = list_domain_mod, columns = ['domain'])
    df_final_mod = pd.concat([df_final_bis, df_domain_mod], 1)
    
    # We randomise
    df_final_mod = df_final_mod.sample(frac=1)
    df_final_mod = df_final_mod.reset_index()
    df_final_mod = df_final_mod.drop(['index'], 1)
    
    # We put in on a excel file in the file Project_Twitter
    df_final_mod.to_excel(file + "name_domain.xlsx")



# We build the scrapping functions

import time
import requests
from fake_useragent import UserAgent

# We randomise the user agent
ua = UserAgent()


def fetch_results(search_term, number_results, language_code):
    
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')
        
    USER_AGENT = {'User-Agent' : ua.random }
    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()
    
    return search_term, response.text

def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')
 
    found_results = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:
 
        link = result.find('a', href=True)
        title = result.find('h3')
        description = result.find('span', attrs={'class': 'st'})
        if link and title:
            link = link['href']
            title = title.get_text()
            if description:
                description = description.get_text()
            if link != '#':
                found_results.append({'keyword': keyword, 'rank': rank, 'title': title, 'description': description})
                rank += 1
    return found_results

def scrape_google(search_term, number_results, language_code):
    # The try here will sssart which arror can be found during the scrapping
    try:
        keyword, html = fetch_results(search_term, number_results, language_code)
        results = parse_results(html, keyword)
        return results
    except IndexError:
        return "inerror"
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")
        
# We take the first link of the google page for the list of name       
def scrape_page(list_name):
    list_page = []
    for name in list_name:
        list_page += [scrape_google(name + ' Twitter', 1, 'fr')]
    return list_page

# We only keep the name of the function scrape_page
def get_name(list_name):
    list_page_from_scrape = scrape_page(list_name)
    list_udl_name = []
    for page in list_page_from_scrape:
        if page == []:
            udl_name = ''
        else :
            text = page[0]['title']
            if '(' in text:
                start = text.find('(')
                end = text.find(')')
                udl_name = text[start +1 :end]
            else : 
                udl_name = ''
        list_udl_name += [udl_name]
    return list_udl_name


# We get the excel of all the names
def uld_twitter_excel_format():
    
    # We import the excel file with the name, firstname and domain
    print("loading excel names")
    df_name_domain = pd.read_excel(file + "name_domain.xlsx")
    print('end loading')
    # We get the names in a list with the domain
    print("Loading the list of names with good domain")
    List_name = []
    i = 0
    for names in df_name_domain['names']:
        try :
            List_name += [df_name_domain['firstnames'][i] + ' ' + names + ' ' + df_name_domain['domain'][i]]
        except TypeError:
            List_name += ['None']
        i += 1
    print("List is ready to be scrapped")
    print("Start Scrapping names")
    #We start scapping
    list_twitter_scrapp = []
    for j in range(len(List_name)):
        try :
            list_twitter_scrapp += [get_name(List_name[j:1 +j])]
            # random time sleep
            time.sleep(random.choice([i/10 for i in range(0,20)]))
        except requests.RequestException:
            time.sleep(10)
            list_twitter_scrapp += ['']  
    print("end scrapping names")
    # On enlève les @
    list_twitter_scrapp_bis = [[text[0][1:]] for text in list_twitter_scrapp]
    
    df_name = pd.DataFrame(list_twitter_scrapp_bis, columns = ["twitter names"])
    
    # We save it in an excel file in the file Scrapping_Twitter
    df_name.to_excel(file + "twitter_names.xlsx")

# We get the full info of users
def full_data_twitter():
    
    df_udl_twitter = pd.read_excel(file + "twitter_names.xlsx")
    df_init_name = pd.read_excel(file + "name_domain.xlsx")
    df_full_associate = pd.concat([df_init_name[['names','firstnames']].reset_index(drop=True), 
                                   df_udl_twitter], 1)
    df_full_associate = df_full_associate.dropna()
    df_full_associate = df_full_associate[df_full_associate != '']
    df_full_associate = df_full_associate.dropna()
    df_full_associate = df_full_associate.reset_index(drop=True)
    
    # info par user
    list_info = []
    i = 0
    for name in df_full_associate['twitter names']:
        try:
            list_info += [api.get_user(name)]
            i += 1
        except tweepy.TweepError:
            list_info += ['NaN']
    
    # list of info per users
    list_location = [info.location if info != 'NaN' else None for info in list_info]
    list_followed = [info.friends_count if info != 'NaN' else None for info in list_info]
    list_following = [info.followers_count if info != 'NaN' else None for info in list_info]
    list_favourites_count = [info.favourites_count if info != 'NaN' else None for info in list_info]
    list_listed_count = [info.listed_count if info != 'NaN' else None for info in list_info]
    list_statuses_count = [info.statuses_count if info != 'NaN' else None for info in list_info]
    list_description = [info.description if info != 'NaN' else None for info in list_info]

    
    # info in dataframe
    df_location = pd.DataFrame(list_location, columns = ['location'])
    df_followed = pd.DataFrame(list_followed, columns = ['followed'])
    df_following = pd.DataFrame(list_following, columns = ['following'])
    df_favourites_count = pd.DataFrame(list_favourites_count, columns = ['favorite_count'])
    df_listed_count = pd.DataFrame(list_listed_count, columns = ['listed_count'])
    df_statuses_count = pd.DataFrame(list_statuses_count, columns = ['statused_count'])
    df_description = pd.DataFrame(list_description, columns = ['description'])

    # tweets par user (20 default)
    list_tweets = []
    i = 0 
    for name in df_full_associate['twitter names']:
        try:
            list_tweets += [api.user_timeline(name)]
            i += 1
            print(i)
        except tweepy.TweepError:
            list_tweets += [['NaN']*20]

    columns_tweets = ['tweet %i'%(i) for i in range(20)]
    df_last_tweets = pd.DataFrame(list_tweets, columns = columns_tweets)
    
    # We concatenate every thing in an entire datafrme
    df_full_info = pd.concat([df_full_associate, df_location, df_followed, 
                          df_following, df_favourites_count, 
                          df_listed_count, df_statuses_count, 
                          df_description, df_last_tweets], 1)

    # We dave it in an excel file
    df_full_info.to_excel(file + "twitter_full_info.xlsx")
    
    return df_full_info


def get_data():
    #To get the list with good domain :
    
    return_dataframe_list_name_domain()
    
    #To get the dataframe with name, first name and udl_name
    
    uld_twitter_excel_format()
    
    #To get the full info dataframe :
    
    full_info = full_data_twitter()
    return full_info