#This Function will return the number of messages by a user
from urlextract import URLExtract
extract=URLExtract()
import matplotlib.pyplot as plt
import nltk
import pandas as pd
import emoji
from collections import Counter



def fetch_stats(selected_user,df):
     
    if selected_user=='Overall':
        #fetch number of messages
        num_message=df.shape[0]

        #number of wo rds
        words=[]
        for mess in df['user_message']:
             words.extend(mess.split())

        #Now Fetch the media one messages
        num_media=df[df['user_message']=='<Media omitted>'].shape[0]
        #Now Just fetch the Links
        links=[]
        for mess in df['user_message']:
            links.extend(extract.find_urls(mess))

        
        return num_message,len(words),num_media,len(links)
    else:
        new_df=df[df['user']==selected_user]
        #Total Number of messages
        num_message=new_df.shape[0]

        words=[]
        for mess in new_df['user_message']:
            words.extend(mess.split())
        
        #now fetch the media one messages
        num_media=df[df['user_message']=='<Media omitted>'].shape[0]

        #Now Just fetch the Links
        links=[]
        for mess in new_df['user_message']:
            links.extend(extract.find_urls(mess))

        return num_message,len(words),num_media,len(links)
    
def most_busy_users(df):
            x= df['user'].value_counts().head()
            count= round((df['user'].value_counts()/df.shape[0])*100,1).reset_index().rename(columns={'index':'name','user':'percent'})

            return x,count

def most_common_words(selected_user,df):
     
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    temp=df[df['user_message']!='group_notification']
    temp=temp[temp['user_message']!='<Media omitted>']

    # Import the stop words list from NLTK
    stopwords = nltk.corpus.stopwords.words('english')

    # Create a list of words from the data
    words = []
    for message in temp['user_message']:
     words.extend(message.split())

    # Remove the stop words from the list of words
    filtered_words = [word for word in words if word not in stopwords]

    # Print the most common 20 words
    from collections import Counter
    data=pd.DataFrame(Counter(filtered_words).most_common(20))

    return data

def emoji_select(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    emojis=[]
    for m in df['user_message']:
       emojis.extend([c for c in m if c in emoji.EMOJI_DATA])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

     
def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['user_message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['user_message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='user_message', aggfunc='count').fillna(0)

    return user_heatmap