import re
import pandas as pd

def remove_non_breaking_space(time_string):
    """Removes the non-breaking space character from a time string."""
    return time_string.replace('\u202f', '')

def remove_am_pm(time_string):
    """Removes the AM/PM indicator from a time string."""
    return time_string[:-2]

def preprocess(data):
    pattern = r'(\d{2}/\d{2}/\d{4}), (\d{1,2}:\d{2}\s[ap]m) - (.+?): (.+)'
    messages=re.split(pattern,data)
    # len(messages)


    dates_times = []
    messages_ = []
    users=[]

    matches = re.findall(pattern, data)
    for match in matches:
        date = match[0]
        time = match[1]
        time = remove_non_breaking_space(time)
        time = remove_am_pm(time)
        name = match[2]
        message_text = match[3]

        # Convert the tuple to a string
        dates_times.append('{} {}'.format(date, time))
        messages_.append('{}'.format(message_text))
        users.append('{}'.format(name))

    df=pd.DataFrame({'user_message':messages_,'message_date':dates_times,'user':users})
    # df.head()
    df['message_date'] = df['message_date'].astype(str)  # Convert column to string type

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y %H:%M')

    df['only_date'] = df['message_date'].dt.date
    df['year'] = df['message_date'].dt.year
    df['month_num'] = df['message_date'].dt.month
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.day_name()
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
