from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df = df[df['users'] == selected_user]

    # fetching number of messages
    num_messages = df.shape[0]

    # number of words
    words = []
    temp = df[df['users'] != 'Group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    for message in temp['message']:
        words.extend(message.split())

    #number of media files
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    #fetching number of links
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media, len(links)

def most_busy_users(df):
    x=df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'users':'name','count':'percent'})
    return x,df

def create_word_cloud(selected_user,df):
    f = open('stop_hinglish .txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'Group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    #internal function
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return ' '.join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc= wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish .txt','r')
    stop_words=f.read()

    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    temp = df[df['users']!='Group notification']
    temp = temp[temp['message']!='<Media omitted>\n']

    words=[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    most_common_df = most_common_df.rename(columns={'Unnamed: 0':'Words','Unnamed: 1':'Occurences'})
    return most_common_df

def emoji_finder(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time']=time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users']==selected_user]

    user_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap
