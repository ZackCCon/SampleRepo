import streamlit
import pandas
import requests

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

#API Response
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "watermelon")

# Normalize API Response data 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Display Normalized data as Dataframe
streamlit.dataframe(fruityvice_normalized)
