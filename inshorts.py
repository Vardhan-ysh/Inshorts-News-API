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
# import requests
# import pytz
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

# def get_crime_and_justice_keywords():
#     """
#     Returns a list of ~400 crime and justice-related keywords and categories.
#     """
#     categories = [
#         'crime', 'law', 'india', 'top_stories', 'trending'
#     ]
    
#     keywords = [
#         # Crime Types (~100)
#         'murder', 'rape', 'assault', 'robbery', 'theft', 'kidnapping', 'arson', 'homicide', 
#         'smuggling', 'trafficking', 'cybercrime', 'fraud', 'burglary', 'extortion', 
#         'embezzlement', 'money laundering', 'vandalism', 'blackmail', 'bribery', 'forgery', 
#         'stalking', 'abduction', 'manslaughter', 'piracy', 'poaching', 'shoplifting', 
#         'trespassing', 'carjacking', 'hacking', 'phishing', 'identity theft', 'corruption', 
#         'perjury', 'sabotage', 'counterfeiting', 'drug trafficking', 'arms dealing', 
#         'domestic violence', 'child abuse', 'elder abuse', 'harassment', 'hit and run', 
#         'looting', 'mugging', 'pickpocketing', 'ransom', 'sex trafficking', 'white-collar crime', 
#         'terrorism', 'violent crime',
#         'aggravated assault', 'battery', 'grand theft', 'larceny', 'home invasion', 
#         'human trafficking', 'insider trading', 'tax evasion', 'ponzi scheme', 'pyramid scheme', 
#         'espionage', 'treason', 'sedition', 'hijacking', 'smash and grab', 'cyberstalking', 
#         'ransomware', 'data breach', 'wire fraud', 'mail fraud', 'corporate fraud', 
#         'animal cruelty', 'public intoxication', 'disorderly conduct', 'reckless endangerment', 
#         'false imprisonment', 'coercion', 'intimidation', 'torture', 'war crime', 'genocide', 
#         'ethnic cleansing', 'crimes against humanity', 'prostitution', 'pimping', 'solicitation', 
#         'drug possession', 'illegal gambling', 'match-fixing', 'doping', 'environmental crime', 
#         'illegal logging', 'wildlife trafficking', 'art theft', 'public corruption', 
#         'political assassination', 'hostage-taking', 'road rage',

#         # Justice and Legal Terms (~100)
#         'arrest', 'investigation', 'police', 'court', 'judiciary', 'legal', 'sentenced', 
#         'warrant', 'bail', 'trial', 'prosecution', 'suspect', 'accused', 'charge sheet', 
#         'conviction', 'acquittal', 'parole', 'probation', 'appeal', 'hearing', 'verdict', 
#         'testimony', 'evidence', 'witness', 'jury', 'judge', 'lawyer', 'attorney', 'defendant', 
#         'plaintiff', 'custody', 'detention', 'interrogation', 'confession', 'plea', 'lawsuit', 
#         'injunction', 'restraining order', 'forensic', 'autopsy', 'crime lab', 'penitentiary', 
#         'prison', 'jail', 'bailiff', 'magistrate', 'sentencing', 'extradition', 'pardon', 
#         'law enforcement', 'justice',
#         'subpoena', 'deposition', 'affidavit', 'indictment', 'arraignment', 'plea bargain', 
#         'settlement', 'mediation', 'arbitration', 'litigation', 'statute', 'ordinance', 
#         'regulation', 'precedent', 'jurisdiction', 'habeas corpus', 'due process', 'civil rights', 
#         'public defender', 'pro bono', 'legal aid', 'courtroom', 'docket', 'case law', 
#         'bench trial', 'grand jury', 'inquest', 'coroner', 'probate', 'trustee', 'executor', 
#         'compliance', 'ethics violation', 'malpractice', 'negligence', 'tort', 'damages', 
#         'restitution', 'fine', 'penalty', 'incarceration', 'rehabilitation', 'community service', 
#         'juvenile justice', 'diversion program', 'protective custody', 'search warrant', 
#         'wiretap', 'surveillance', 'amnesty',

#         # Crime and Justice Descriptors (~30)
#         'crime', 'criminal', 'victim', 'perpetrator', 'offender', 'felon', 'misdemeanor', 
#         'felony', 'accomplice', 'informant', 'fugitive', 'gang', 'syndicate', 'mob', 
#         'outlaw', 'culprit', 'delinquent', 'vigilante', 'recidivist', 'parolee', 'escapee', 
#         'crime scene', 'modus operandi', 'alibi', 'motive', 'cover-up', 'conspiracy', 
#         'racketeering', 'underworld', 'hitman',

#         # Specific Contexts (~70)
#         'serial killer', 'gangster', 'mafia', 'sexual assault', 'hate crime', 'economic crime', 
#         'cyber attack', 'scam', 'encounter', 'encounter killing', 'serial crime', 
#         'organized crime', 'criminal gang', 'terror attack', 'mass shooting', 'bombing', 
#         'genocide', 'war crime', 'delhi crime', 'mumbai crime',
#         'bank heist', 'jewel theft', 'smuggling ring', 'drug cartel', 'extortion racket', 
#         'cyber espionage', 'election fraud', 'voter suppression', 'police brutality', 
#         'custodial death', 'fake encounter', 'honor killing', 'dowry death', 'acid attack', 
#         'roadside robbery', 'train robbery', 'pirate attack', 'maritime crime', 'air piracy', 
#         'corporate espionage', 'trade secret theft', 'patent infringement', 'price fixing', 
#         'antitrust violation', 'insider dealing', 'stock manipulation', 'real estate scam', 
#         'land grabbing', 'illegal mining', 'sand mafia', 'forest mafia', 'poaching syndicate', 
#         'organ trafficking', 'blood diamond', 'arms smuggling', 'nuclear smuggling', 
#         'chemical attack', 'biological attack', 'radiological attack', 'school shooting', 
#         'workplace violence', 'bar fight', 'riot', 'lynching', 'mob justice', 'vigilante justice', 
#         'political violence', 'coup attempt', 'rebellion', 'insurgency',

#         # Law Enforcement Agencies and Operations (50)
#         'police raid', 'sting operation', 'undercover agent', 'swat team', 'riot police', 
#         'task force', 'special forces', 'border patrol', 'customs service', 'intelligence agency', 
#         'fbi', 'cia', 'Interpol', 'narcotics bureau', 'crime branch', 'vigilance department', 
#         'anti-terror squad', 'rapid action force', 'paramilitary', 'security detail', 
#         'patrol unit', 'k9 unit', 'mounted police', 'traffic police', 'cyber police', 
#         'forensic team', 'bomb squad', 'hostage negotiation', 'surveillance team', 'drone operation', 
#         'wiretapping', 'covert mission', 'operation crackdown', 'joint operation', 'raid seizure', 
#         'checkpoint', 'roadblock', 'barricade', 'lockdown', 'curfew enforcement', 'public safety', 
#         'crime prevention', 'community policing', 'beat patrol', 'night watch', 'arrest warrant', 
#         'field interrogation', 'informant network', 'police intelligence', 'counter-terrorism',

#         # Judicial Systems and Courts (50)
#         'supreme court', 'high court', 'district court', 'sessions court', 'family court', 
#         'juvenile court', 'tribunal', 'appellate court', 'constitutional court', 'military court', 
#         'court martial', 'arbitration panel', 'mediation board', 'judicial review', 'case backlog', 
#         'court order', 'legal precedent', 'bench warrant', 'court clerk', 'judicial custody', 
#         'remand', 'bail hearing', 'trial date', 'court adjourned', 'cross-examination', 
#         'opening statement', 'closing argument', 'objection', 'overruled', 'sustained', 
#         'court transcript', 'legal brief', 'amicus curiae', 'public prosecutor', 'defense counsel', 
#         'legal representation', 'court fees', 'judicial reform', 'fast-track court', 'lok adalat', 
#         'people’s court', 'virtual hearing', 'e-court', 'judicial inquiry', 'contempt of court', 
#         'court security', 'judicial oversight', 'legal jurisdiction', 'circuit court', 'small claims',

#         # Punishment and Corrections (50)
#         'death penalty', 'life sentence', 'solitary confinement', 'hard labor', 'capital punishment', 
#         'execution', 'lethal injection', 'hanging', 'electric chair', 'firing squad', 
#         'imprisonment', 'lockup', 'detention center', 'correctional facility', 'reformatory', 
#         'open jail', 'house arrest', 'electronic monitoring', 'ankle bracelet', 'work release', 
#         'halfway house', 'boot camp', 'juvenile detention', 'rehabilitation center', 'parole board', 
#         'early release', 'commutation', 'sentence reduction', 'good behavior', 'prison riot', 
#         'jailbreak', 'escape attempt', 'prison gang', 'inmate rights', 'prison reform', 
#         'overcrowding', 'prison conditions', 'visitation rights', 'conjugal visit', 'prison labor', 
#         'recidivism rate', 'reentry program', 'ex-convict', 'stigma', 'post-release', 
#         'probation officer', 'curfew violation', 'mandatory sentencing', 'three-strike law', 'restitution order',

#         # Social and Political Crime Issues (50)
#         'civil unrest', 'protest violence', 'political prisoner', 'state repression', 'martial law', 
#         'emergency decree', 'human rights abuse', 'police state', 'dictatorship', 'oppression', 
#         'whistleblower', 'leak scandal', 'government corruption', 'kickback', 'nepotism', 
#         'cronyism', 'slush fund', 'public scam', 'misappropriation', 'fund embezzlement', 
#         'black money', 'hawala', 'tax haven', 'offshore account', 'money trail', 
#         'social justice', 'inequality', 'discrimination', 'hate speech', 'racial profiling', 
#         'caste violence', 'communal riot', 'religious extremism', 'radicalization', 'sedition charge', 
#         'defamation case', 'libel suit', 'press freedom', 'censorship', 'fake news', 
#         'propaganda', 'public outrage', 'vigilante mob', 'lynch mob', 'class action', 
#         'citizen arrest', 'public inquiry', 'truth commission', 'reconciliation', 'amnesty deal'
#     ]
    
#     exclude_keywords = [
#         'movie plot', 'film story', 'fictional crime', 'tv series', 'book review'
#     ]
    
#     print(f"Total Crime and Justice Keywords: {len(keywords)}")
#     return categories, keywords, exclude_keywords

# def filter_news_by_keywords(news_list, keywords=None, exclude_keywords=None, min_keyword_match=1):
#     """
#     Filters news articles based on crime and justice keywords.
#     """
#     if not keywords and not exclude_keywords:
#         return news_list
    
#     filtered_news = []
    
#     for news in news_list:
#         search_text = (news['title'] + ' ' + news['content']).lower()
        
#         if exclude_keywords:
#             if any(keyword.lower() in search_text for keyword in exclude_keywords):
#                 continue
        
#         if keywords:
#             keyword_matches = sum(1 for keyword in keywords if keyword.lower() in search_text)
#             if keyword_matches < min_keyword_match:
#                 continue
        
#         filtered_news.append(news)
    
#     return filtered_news

# def getNews(category='all'):
#     """
#     Fetch crime and justice news from Inshorts for 2025 only, returning as a dictionary.
#     """
#     categories=None, keywords=None, exclude_keywords=None

#     if categories is None:
#         categories, keywords, exclude_keywords = get_crime_and_justice_keywords()
    
#     news_set = set()
#     all_news_data = []
#     news_dict = {"news": [], "status": "success"}
    
#     for cat in categories:
#         try:
#             if cat in ['top_stories', 'trending']:
#                 response = requests.get(
#                     'https://inshorts.com/api/en/news?category=all_news&include_card_data=true')
#             else:
#                 response = requests.get(
#                     f'https://inshorts.com/api/en/search/trending_topics/{cat}', 
#                     headers=headers, 
#                     params=(('category', cat), ('include_card_data', 'true'))
#                 )
            
#             news_data = response.json()['data']['news_list']
#             if news_data:
#                 all_news_data.extend(news_data)
#         except Exception as e:
#             print(f"Error fetching {cat}: {str(e)}")
#             continue
    
#     if not all_news_data:
#         news_dict["status"] = "no_data"
#         news_dict["message"] = "No Crime or Justice News Available for 2025"
#         return news_dict
    
#     # Filter news by keywords and year (2025 only)
#     filtered_news = filter_news_by_keywords(
#         [{'title': entry['news_obj']['title'], 'content': entry['news_obj']['content']} 
#          for entry in all_news_data],
#         keywords, 
#         exclude_keywords,
#         min_keyword_match=1
#     )
    
#     if not filtered_news:
#         news_dict["status"] = "no_filtered_data"
#         news_dict["message"] = "No Crime or Justice News Available for 2025"
#         return news_dict
    
#     # Prepare dictionary and print output
#     output = "🔄 Auto-refresh: ON\n\n"
    
#     for entry in all_news_data:
#         news = entry['news_obj']
#         if news['title'] not in news_set and news['title'] in [n['title'] for n in filtered_news]:
#             timestamp = news['created_at'] / 1000
#             dt_utc = datetime.datetime.utcfromtimestamp(timestamp)
#             tz_utc = pytz.timezone('UTC')
#             dt_utc = tz_utc.localize(dt_utc)
#             tz_ist = pytz.timezone('Asia/Kolkata')
#             dt_ist = dt_utc.astimezone(tz_ist)
            
#             # Filter for 2025 only
#             if dt_ist.year != 2025:
#                 continue
                
#             news_set.add(news['title'])
#             title = news['title']
#             content = news['content']
#             url = news['shortened_url']
#             time_str = dt_ist.strftime('[%B %d, %Y | %I:%M %p]')
            
#             # Add to dictionary
#             news_dict["news"].append({
#                 "timestamp": time_str,
#                 "title": title,
#                 "content": content,
#                 "url": url
#             })
            
#             # Prepare print output
#             output += f"{time_str} {title}\n{content} - Know More: {url}\n\n"
    
#     if len(news_set) == 0:
#         news_dict["status"] = "no_2025_data"
#         news_dict["message"] = "No Crime or Justice News Available for 2025"
#         return news_dict
    
#     # Print the formatted output
#     print(output.strip())
    
#     return news_dict