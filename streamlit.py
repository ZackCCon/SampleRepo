import streamlit
import pandas
import requests
from urllib.error import URLError
import snowflake.connector

streamlit.title('Zack has created an app')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#API Header
streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

#API Response
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice )

# Normalize API Response data 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Display Normalized data as Dataframe
streamlit.dataframe(fruityvice_normalized)

streamlit.stop()
# Snowflake Steps Begin Below

# Get Snowflake metadata
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("In the Fruit Load List, We Have:")
streamlit.dataframe(my_data_rows)

add_chosen_fruit = streamlit.text_input('What additional fruit would you like to add?','Jackfruit')
streamlit.write('Thanks for adding ', add_chosen_fruit, '!')

# Insert data to Snowflake
# my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')



