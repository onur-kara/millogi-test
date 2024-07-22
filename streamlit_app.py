import streamlit as st 
import pandas as pd
import pymongo

# SOURCE:
# https://docs.streamlit.io/develop/tutorials/databases/mongodb#add-username-and-password-to-your-local-app-secrets

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

client = init_connection()


# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    db = client.test
    items = db.fixedwing.large_airframes.find()
    items = list(items)  # make hashable for st.cache_data
    return items

# Fetch the data
data = get_data()

# Convert the data to a DataFrame
df = pd.DataFrame(data)

st.title("Onur's Aircraft News Tracker")
st.markdown("This is a simple application that connects a MongoDB Atlas database to a Streamlit frontend.  \n")

st.markdown("TODO list:  \n"
             "- Data validation: see whether all triggers detected by Inoreader is being added.  \n"
             "- Remove all HTML formattting from title and details, automatically translate the column into English.  \n")

st.write(df)

