# Coded by Sumanjay on 29th Feb 2020
import datetime
import uuid
import requests
import pytz
import random


headers = {
    'authority': 'inshorts.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.5',
    'content-type': 'application/json',
    'referer': 'https://inshorts.com/en/read',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

params = (
    ('category', 'top_stories'),
    ('include_card_data', 'true')
)


def getNews(category='all'):
    categories = ['top_stories', 'trending', 'india', 'business', 'politics', 'technology', 'entertainment', 'sports']
    
    news_set = set()  # Using set to avoid duplicates
    all_news_data = []

    # Get news from all categories
    for cat in categories:
        if cat == 'top_stories':
            response = requests.get(
                'https://inshorts.com/api/en/news?category=all_news&include_card_data=true')
        else:
            response = requests.get(
                f'https://inshorts.com/api/en/search/trending_topics/{cat}', 
                headers=headers, 
                params=params
            )
        
        try:
            news_data = response.json()['data']['news_list']
            if news_data:
                all_news_data.extend(news_data)
        except Exception as e:
            print(f"Error fetching {cat}: {str(e)}")
            continue

    newsDictionary = {
        'success': True,
        'category': 'all',
        'data': []
    }

    if not all_news_data:
        newsDictionary['success'] = False
        newsDictionary['error'] = 'No News Available'
        return newsDictionary

    # Shuffle the all_news_data list randomly
    random.shuffle(all_news_data)

    for entry in all_news_data:
        try:
            news = entry['news_obj']
            # Use title as unique identifier to avoid duplicates
            if news['title'] in news_set:
                continue
            news_set.add(news['title'])
            
            author = news['author_name']
            title = news['title']
            imageUrl = news['image_url']
            url = news['shortened_url']
            content = news['content']
            timestamp = news['created_at'] / 1000
            dt_utc = datetime.datetime.utcfromtimestamp(timestamp)
            tz_utc = pytz.timezone('UTC')
            dt_utc = tz_utc.localize(dt_utc)
            tz_ist = pytz.timezone('Asia/Kolkata')
            dt_ist = dt_utc.astimezone(tz_ist)
            date = dt_ist.strftime('%A, %d %B, %Y')
            time = dt_ist.strftime('%I:%M %p').lower()
            readMoreUrl = news['source_url']

            newsObject = {
                'id': uuid.uuid4().hex,
                'title': title,
                'imageUrl': imageUrl,
                'url': url,
                'content': content,
                'author': author,
                'date': date,
                'time': time,
                'readMoreUrl': readMoreUrl
            }
            newsDictionary['data'].append(newsObject)
        except Exception as e:
            print(f"Error processing news entry: {str(e)}")
            continue

    return newsDictionary

# import datetime
# import uuid
# import requests
# import pytz
# import random
# import re

# headers = {
#     'authority': 'inshorts.com',
#     'accept': '*/*',
#     'accept-language': 'en-GB,en;q=0.5',
#     'content-type': 'application/json',
#     'referer': 'https://inshorts.com/en/read',
#     'sec-ch-ua': '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"macOS"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'sec-gpc': '1',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
# }

# def get_comprehensive_crime_keywords():
#     """
#     Returns an extensive list of crime-related keywords and categories.
#     """
#     categories = [
#         'crime',          # Direct crime category
#         'law',            # Legal and justice-related news
#         'india',          # For region-specific crime news
#         'top_stories',    # To catch more potential crime news
#         'trending'        # To expand search
#     ]
    
#     keywords = [
#         # Comprehensive Crime Types
#         'murder', 'rape', 'assault', 'robbery', 'theft', 
#         'kidnapping', 'arson', 'homicide', 'smuggling', 
#         'trafficking', 'cybercrime', 'fraud', 'burglary', 
#         'extortion', 'embezzlement', 'money laundering',
        
#         # Legal and Investigation Terms
#         'arrest', 'investigation', 'police', 'court', 
#         'judiciary', 'legal', 'sentenced', 'warrant', 
#         'bail', 'trial', 'prosecution', 'suspect', 
#         'accused', 'investigation', 'charge sheet',
        
#         # Crime-Related Descriptors
#         'crime', 'criminal', 'victim', 'perpetrator', 
#         'evidence', 'case', 'charges', 'police case',
        
#         # Specific Crime Contexts
#         'serial killer', 'gangster', 'mafia', 'terrorism', 
#         'violent crime', 'sexual crime', 'hate crime', 
#         'economic crime', 'cyber attack', 'scam',
        
#         # High-Profile or Sensational Terms
#         'encounter', 'encounter killing', 'serial crime', 
#         'organized crime', 'criminal gang', 'terror attack',
        
#         # Geographic Specific
#         'delhi crime', 'mumbai crime', 'crime scene', 
#         'police station', 'law enforcement'
#     ]
    
#     # Minimal exclusion to capture more news
#     exclude_keywords = [
#         'movie plot', 'film story', 'fictional crime'
#     ]
    
#     print("Crime-Related Categories and Search Strategy:")
#     for category in categories:
#         print(f"- {category}")
#     print(f"\nTotal Keywords: {len(keywords)}")
    
#     return categories, keywords, exclude_keywords

# def filter_news_by_keywords(news_list, keywords=None, exclude_keywords=None, min_keyword_match=1):
#     """
#     Enhanced filtering to ensure more comprehensive news capture.
    
#     :param news_list: List of news articles to filter
#     :param keywords: List of keywords to include (case-insensitive)
#     :param exclude_keywords: List of keywords to exclude (case-insensitive)
#     :param min_keyword_match: Minimum number of keywords to match
#     :return: Filtered list of news articles
#     """
#     if not keywords and not exclude_keywords:
#         return news_list
    
#     filtered_news = []
    
#     for news in news_list:
#         # Convert title and content to lowercase for case-insensitive matching
#         search_text = (news['title'] + ' ' + news['content']).lower()
        
#         # Check exclusion keywords first
#         if exclude_keywords:
#             if any(keyword.lower() in search_text for keyword in exclude_keywords):
#                 continue
        
#         # Check inclusion keywords
#         if keywords:
#             # Count keyword matches
#             keyword_matches = sum(
#                 1 for keyword in keywords 
#                 if keyword.lower() in search_text
#             )
            
#             # If matches are below threshold, skip
#             if keyword_matches < min_keyword_match:
#                 continue
        
#         filtered_news.append(news)
    
#     return filtered_news

# def getNews(categories=None, keywords=None, exclude_keywords=None):
#     """
#     Fetch comprehensive news related to crime.
    
#     :param categories: List of categories to fetch from
#     :param keywords: Optional list of keywords to include in news
#     :param exclude_keywords: Optional list of keywords to exclude from news
#     :return: Dictionary containing filtered news articles
#     """
#     # Use crime-related categories and keywords if not specified
#     if categories is None:
#         categories, keywords, exclude_keywords = get_comprehensive_crime_keywords()
    
#     news_set = set()  # Using set to avoid duplicates
#     all_news_data = []
    
#     # Get news from specified categories
#     for cat in categories:
#         try:
#             # Adjust API calls based on category
#             if cat in ['top_stories', 'trending']:
#                 response = requests.get(
#                     'https://inshorts.com/api/en/news?category=all_news&include_card_data=true')
#             else:
#                 response = requests.get(
#                     f'https://inshorts.com/api/en/search/trending_topics/{cat}', 
#                     headers=headers, 
#                     params=(
#                         ('category', cat),
#                         ('include_card_data', 'true')
#                     )
#                 )
            
#             news_data = response.json()['data']['news_list']
#             if news_data:
#                 all_news_data.extend(news_data)
#         except Exception as e:
#             print(f"Error fetching {cat}: {str(e)}")
#             continue
    
#     newsDictionary = {
#         'success': True,
#         'category': 'comprehensive_crime',
#         'data': []
#     }
    
#     if not all_news_data:
#         newsDictionary['success'] = False
#         newsDictionary['error'] = 'No News Available'
#         return newsDictionary
    
#     # Shuffle the all_news_data list to randomize results
#     random.shuffle(all_news_data)
    
#     for entry in all_news_data:
#         try:
#             news = entry['news_obj']
#             # Use title as unique identifier to avoid duplicates
#             if news['title'] in news_set:
#                 continue
#             news_set.add(news['title'])
            
#             author = news['author_name']
#             title = news['title']
#             imageUrl = news['image_url']
#             url = news['shortened_url']
#             content = news['content']
#             timestamp = news['created_at'] / 1000
#             dt_utc = datetime.datetime.utcfromtimestamp(timestamp)
#             tz_utc = pytz.timezone('UTC')
#             dt_utc = tz_utc.localize(dt_utc)
#             tz_ist = pytz.timezone('Asia/Kolkata')
#             dt_ist = dt_utc.astimezone(tz_ist)
#             date = dt_ist.strftime('%A, %d %B, %Y')
#             time = dt_ist.strftime('%I:%M %p').lower()
#             readMoreUrl = news['source_url']
#             newsObject = {
#                 'id': uuid.uuid4().hex,
#                 'title': title,
#                 'imageUrl': imageUrl,
#                 'url': url,
#                 'content': content,
#                 'author': author,
#                 'date': date,
#                 'time': time,
#                 'readMoreUrl': readMoreUrl
#             }
#             newsDictionary['data'].append(newsObject)
#         except Exception as e:
#             print(f"Error processing news entry: {str(e)}")
#             continue
    
#     # Apply keyword filtering with relaxed constraints
#     newsDictionary['data'] = filter_news_by_keywords(
#         newsDictionary['data'], 
#         keywords, 
#         exclude_keywords,
#         min_keyword_match=1  # Relax matching requirement
#     )
    
#     return newsDictionary
