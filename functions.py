import json
from nltk.tokenize import RegexpTokenizer
import re
from datetime import date
import calendar
import csv
from nltk import word_tokenize
from nltk import pos_tag
from nltk import WhitespaceTokenizer
import emoji
from nltk.util import ngrams

tokenizer = RegexpTokenizer(r'\w+')
abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}

def extract_text(adr):
    temp = load_json_list(adr)
    data = []
    for item in temp:
        if 'extended_tweet' in item.keys():
            text = item['extended_tweet']['full_text']
        else:
            text = item['text']
        temp = WhitespaceTokenizer.tokenize(text)
        if temp[0] != 'Wind':
            text = re.sub(r"\s+", " ", text)
            text = text.strip()
            data.append(text)
    return data

def extract_location(data):
    x0 = data['place']['bounding_box']['coordinates'][0][0][0]
    y0 = data['place']['bounding_box']['coordinates'][0][0][1]
    x1 = data['place']['bounding_box']['coordinates'][0][2][0]
    y1 = data['place']['bounding_box']['coordinates'][0][2][1]
    longitude = (x0+x1)/float(2)
    latitude = (y0+y1)/float(2)
    longitude = round(longitude, 6)
    latitude = round(latitude, 6)
    longitude = str(longitude)
    latitude = str(latitude)
    return  latitude + '\t' + longitude


def load_json_list(adr):
    tweets = []
    with open(adr,'r') as f:
        for line in f.readlines():
            tweets.append(json.loads(line))
    return tweets

def load_json(adr):
    with open(adr) as f:
        data = json.load(f)
    return data

def write_json_lst(data, adr):
    with open(adr,'w') as f:
        for item in data:
            f.write(json.dumps(item))
            f.write('\n')
    f.close()
    return True

def write_json(data, adr):
    with open(adr, 'w') as outfile:  
        json.dump(data, outfile)
    return True

def load_json_en(adr):
    data = []
    with open(adr,'r') as f:
        for line in f.readlines():
            item = json.loads(line)
            if item['lang'] == 'en':
                data.append(item)
    return data

def load_txt(adr):
    labels = [[],[]]
    with open(adr,'r') as f:
        for line in f.readlines():
            labels[0].append(int(line.split()[1]))
            labels[1].append(int(line.split()[0]))
    del line
    f.close()
    return labels

def write(data, adr):
    with open(adr, 'w') as f:
        for line in data:
            f.write(str(line)+'\n')
    return True

def load(adr):
    with open(adr, 'r') as f:
        data = f.readlines()
    f.close()
    data = [x.rstrip() for x in data]
    return data

def acc_Rep(tweet):
    x = tweet['user']['followers_count']
    y = tweet['user']['friends_count']
    if (x+y) == 0:
        return 0
    else:
        return round(x/(x+y), 3)

def num_of_tokens(tweet):
    if 'extended_tweet' in tweet.keys():
        text = tweet['extended_tweet']['full_text']
    else:
        text = tweet['text']

    text = re.sub('@[^\s]+','',text)
    text = re.sub(r"http\S+", " ",text)
    text = re.sub('#[^\s]+','',text)
    tokens = tokenizer.tokenize(text)
    return len(tokens)

def cal_age(item):
    d0 = date(int(item['user']['created_at'].split()[-1]), abbr_to_num[item['user']['created_at'].split()[1]], int(item['user']['created_at'].split()[2]))
    d1 = date(int(item['created_at'].split()[-1]), abbr_to_num[item['created_at'].split()[1]], int(item['created_at'].split()[2]))
    age = d1 - d0
    return age.days

def save_csv(lst, adr):
    with open(adr, 'w') as f:  
        writer = csv.writer(f)
        for row in lst:
            writer.writerow(row)
    return True
def add_header():
    h = ['id', 'tweet']
    sv, fi, no, dk, ic = [], [], [], [], []
    sv.append(h)
    fi.append(h)
    no.append(h)
    dk.append(h)
    ic.append(h)
    return sv, fi, no, dk, ic
    
def add_geo_header():
    gh = ['city', 'longitude', 'latitude']
    sv_geo, fi_geo, no_geo, dk_geo, ic_geo = [], [], [], [], []
    sv_geo.append(gh)
    fi_geo.append(gh)
    no_geo.append(gh)
    dk_geo.append(gh)
    ic_geo.append(gh)
    return sv_geo, fi_geo, no_geo, dk_geo, ic_geo 

def id_text(data):
    temp = []
    temp.append(data['id_str'])
    if 'extended_tweet' in data.keys():
        t = data['extended_tweet']['full_text'].replace('\n', '')    
    else:
        t = data['text'].replace('\n', '')
    t = re.sub("[\n\t]", "", t)
    temp.append(str(t))
    return temp

def nltk_tagger(data):
    tags = []
    data = data[1:]
    for tweet in data:
        temp = []
        word_list = word_tokenize(tweet[1])
        temp = pos_tag(word_list)
        lst = []
        for item in temp: 
            lst.append(item[0]+ '_' + item[1])
        tags.append(" ".join([item for item in lst]))
    return tags

def extract_date(s):
    date = s.split('.')[0].split('-')
    day = date[2]
    year = date[0]
    month = month = [s.rstrip("0") for s in date[1]]
    month = month[1]
    month = calendar.month_name[int(month)]
    d =str(day) +' '+ str(month) +' '+ str(year)
    return d

def clean_text(text):
    text = re.sub('@[^\s]+','',text)
    text = re.sub(r"http\S+", " ",text)
    text = re.sub('#[^\s]+','',text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text

def clean_troll_text(item):
    item = re.sub(r'xmentionx', '', item)
    item = re.sub(r'xhashtagx', '', item)
    item = re.sub(r'xurlx', '', item)
    item = give_emoji_free_text(item)
    item = " ".join(item.split())
    item = item.strip()
    return item

def remove_emoji(s):
    emoji_pattern = re.compile("["
                       u"\U0001F600-\U0001F64F"  # emoticons
                       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                       u"\U0001F680-\U0001F6FF"  # transport & map symbols
                       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                       u"\U00002702-\U000027B0"
                       u"\U000024C2-\U0001F251"
                       u"\U0001f926-\U0001f937"
                       u"\u200d"
                       u"\u2640-\u2642" 
                       "]+", flags=re.UNICODE)

    s = emoji_pattern.sub(r'', s)
    return s

def give_emoji_free_text(text):
    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
    return clean_text

def additional_remove(text):
    allchars = [str for str in text]
    lst = [ b'\xe2\x83\xa30', b'\xe2\x83\xa31', b'\xe2\x83\xa37', b'\xe2\x83\xa3']
    s = [i for i in allchars if i.encode(encoding='utf-8') not in lst]
    s = [i for i in allchars if i not in emoji.UNICODE_EMOJI]
    new_text = ''
    for i in s:
        if i != ' ':
            new_text += i
        else:
            new_text += ' '
    return new_text

def spacy_tags_dictionary():
    tag_class = {'NN':'Noun', 'NNP':'Noun', 'NNPS':'Noun', 'NNS':'Noun',
             'PR':'Pronoun', 'PRP':'Pronoun', 'PRP$':'Pronoun', 'WDT':'Pronoun',
             'WP':'Pronoun', 'WP$':'Pronoun', 'JJ':'Adjective',
             'JJR':'Adjective', 'JJS':'Adjective', 'RB':'Adverb',
             'RBR':'Adverb', 'RBS':'Adverb', 'RP':'Adverb', 'WRB':'Adverb',
             'VB':'Verb', 'VBD':'Verb', 'VBG':'Verb', 'VBN':'Verb',
             'VBP':'Verb', 'VBZ':'Verb', 'BES':'Verb', 'HVS':'Verb',
             'MD':'Verb', 'IN':'Preposition', 'DT':'Article',
             'UH':'Interjection', 'CC':'Conjunction', 'HYPH':'Punctuation',
             'NFP':'Punctuation', '-LRB-':'Punctuation', '-RRB-':'Punctuation',
             ',':'Punctuation', ':':'Punctuation', ';':'Punctuation',
             '.':'Punctuation', '""':'Punctuation', '``':'Punctuation',
             "'":'Punctuation', 'POS':'Possessive', 'EX':'There_ex', 'TO':'TO-inf'}
    return tag_class


def ratio(tweets):
    
    nom = ["aint", "ain’t"] 
    denom = ['isn’t', 'aren’t', 'wasn’t', 'weren’t', 'haven’t', 
             'hasn’t', 'hadn’t', 'isnt', 'arent', 'wasnt', 'werent',
             'hasnt', 'havent', 'hadnt', 'is not', 'are not', 'was not',
             'were not', 'have not', 'has not', 'had not']
    nom_counter, denom_counter = 0, 0
    for tweet in tweets:
        tokens = WhitespaceTokenizer().tokenize(tweet)
        for item in tokens:
            if item in nom:
                nom_counter+=1
            if item in denom:
                denom_counter+=1
    if denom_counter == 0:
        r = nom_counter
    else:
        r = round(nom_counter/denom_counter, 4)
    
    return r, nom_counter, denom_counter


def safe_div(x,y):
    if y == 0:
        return 0
    return round(x/y, 3)

def month_to_num(name):
    return abbr_to_num[name]