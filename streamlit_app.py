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

st.write(df)

# Extracting the required values
item = data['items'][0]
id = item['id']
item_title = item['title']
item_published = item['published']
origin_title = item['origin']['title']
summary_content = item['summary']['content']

# Displaying the values using st.write
st.write("ID:", id)
st.write("Item Title:", item_title)
st.write("Item Published:", item_published)
st.write("Origin Title:", origin_title)
st.write("Summary Content:", summary_content)