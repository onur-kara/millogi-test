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

st.title("Onur's MiLoGi Tracker")
st.markdown("This is a simple application that connects a MongoDB Atlas database to a Streamlit frontend.  \n")
st.markdown("Data is uploaded to MongoDB using a straightforward script. The basic functionality requires the following:  \n"
             "- Automatically generate JSON data using generative AI and upload the results.  \n"
             "- Regularly export Inoreader content into generative AI, search for relevant entries, and generate JSON data.  \n"
             "- Implement various UI improvements.  \n"
             "- Add the following columns: contract_value, units_required, timestamp.  \n"
             "- Find a way to update items instead of adding new rows.  \n")

st.write(df['items'][0])

