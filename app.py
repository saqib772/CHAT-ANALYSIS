import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

import processing,helper
st.sidebar.title("Chat Analyzer")
 
uploaded_file=st.sidebar.file_uploader("Upload a File")

if uploaded_file is not None:
    st.sidebar.write("File uploaded successfully!")
    bytes_data=uploaded_file.getvalue()
    data= bytes_data.decode("utf-8")
    df=processing.preprocess(data)

    # st.dataframe(df)

    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.sort()
    #Here I'm inserting the Overall case for group char analysis
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox(" Analysis with respect to ",user_list)

    if st.sidebar.button("Show Analysis"):
        #we will get the number of Messages
        num_messages,words,media,links=helper.fetch_stats(selected_user,df)

        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)
        with col1:
            #This will Show the Total Number of Messages by a User
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            #This will Show the Total Number of Messages by a User
            st.header("Total Words")
            st.title(words)
        with col3:
            #This will Show the Total Number of Messages by a User
            st.header("Total Media Shared")
            st.title(media)
        with col4:
            #This will Show the Total Number of Messages by a User
            st.header("Total Links Shared")
            st.title(links)
        
        
        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['user_message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

         # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['user_message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

         # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig) 

        #find Active users in Group
        if selected_user=='Overall':
            st.title("Most Busy Users")
        x,new_data=helper.most_busy_users(df)

        fig,ax=plt.subplots()
           

        column1,columns2=st.columns(2)

        with column1:
            ax.bar(x.index,x.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with columns2:
            st.dataframe(new_data)
        
        #most common Words
        most_common_words=helper.most_common_words(selected_user,df)
        st.header("Most Common words")
        # st.dataframe(most_common_words)
        fig,ax=plt.subplots()
        ax.barh(most_common_words[0],most_common_words[1])
        plt.xticks(rotation='vertical')
        plt.xlabel("Number of Words")
        plt.ylabel("Words")
        st.pyplot(fig)

        #emoji analysis
        emoji_df=helper.emoji_select(selected_user,df)
        st.header("Emoji Analysis")

        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        
        with col2:
            st.header("Top 5 Emojis")
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
        

               



