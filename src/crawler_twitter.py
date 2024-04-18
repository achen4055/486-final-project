import sys
import requests
import re
import json

from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import datetime
import collections
from mediawikiapi import MediaWikiAPI


headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
}
mediawikiapi = MediaWikiAPI()
summary_issue = set()

def generate_dates():
    """Generate the dates of the websites we are crawling"""
    starting_date = datetime.date(2016, 4, 1)
    ending_date = datetime.date(2024, 4, 1)
    delta = datetime.timedelta(days=1)
    dates = []
    while starting_date <= ending_date:
        dates.append(f"{starting_date}")
        starting_date += delta
    return dates


def norm_link(link):
    """Normalize link."""
    if link is None or link == '#' or link == '':
        return "invalid"
    if link[-1] == '/': # remove trailing slash
        link = link[:-1]
    if 'http:' in link: # convert http to https
        link = link.replace('http', 'https')
    if link.startswith('//'):
        link = 'https:' + link
    # check fragment
    frag_idx = link.find('#')
    if frag_idx != -1:
        link = link[:frag_idx]
    link = link.replace(' ', '')
    return link

def rel_link(url, link):
    """Fix relative links."""
    # non-relative links
    if (link.startswith('http://') or link.startswith('https://')
        or link == "invalid" or link ==  "" or '/cdn-cgi/l/email-protection' in link):
        return link
    # matches if link var is in email format
    if re.match(r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$', link, re.IGNORECASE):
        return link
    # matches if link contains non-standard characters
    for char in link:
        if ord(char) > 127:
            return link
    # else, fixes relative links
    return urljoin(url, link)


def check_html(content_type):
    """Check if page is HTML."""
    if 'html' in content_type:
        return True
    return False


def crawl_page(output_dict, date, top_n):
    """Crawl a web page."""
    print(f"Getting trends from: {date}")
    try:
        resp = requests.get(f"https://us.trend-calendar.com/trend/{date}.html", headers=headers)
    except Exception as e:
        print(f"Error w/ request for {date}, skipping")
        return

    try:
        soup = BeautifulSoup(resp.text, 'html.parser')
    except Exception as e:
        print(f"BeautifulSoup error, skipping {date}")
        return
    count = 0
    for twitter_div in soup.find_all('div', class_='readmoretable_line'):
        if count == top_n:
            break
        try:
            trending_topic = twitter_div.find('a').text
        except Exception as e:
            print(f"No data found for date {date}... skipping")
            return
        # Remove possible hashtag
        trending_topic = trending_topic.replace('#', '')
        try:
            results = mediawikiapi.search(trending_topic)
        except Exception as e:
            print(f"Timeout error for {trending_topic}, skipping...")
            continue
        if len(results) == 0: # no results found on Wikipedia
            continue
        top_result = results[0]

        if top_result in summary_issue:
            print(f"Issue finding summary for {top_result}... skipping")
            continue
        try:
            summary = mediawikiapi.summary(top_result)
        except Exception as e:
            print(f"Issue finding summary for {top_result}... skipping")
            summary_issue.add(top_result)
            continue

        count += 1
        output_dict[top_result].append({"summary": summary, "date": date, "rank": count})


def crawl(output_dict, dates, top_n):
    """Perform linear pre-determined web traversal."""
    for date in dates:
        crawl_page(output_dict, date, top_n)

def main():
    # Output dictionary:
    # key: word/trend
    # value: dictionary of {"summary": string, "date": date, "rank": rank}
    output_dict = collections.defaultdict(list) 
    dates = generate_dates()

    crawl(output_dict, dates, 10)
    print("Done")

    with open(f'twitter.json', 'w+', encoding='utf-8') as outfile:
        json.dump(output_dict, outfile, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()