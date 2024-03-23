# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session  #this code is for SiS
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(  "Choose your fruits you want in your Smoothie")
#option=st.selectbox("What is your favorite fruit",('Banana','Strawberry','Peach'))
#st.write( 'Your favorite fruit is : ', option)
name_on_order=st.text_input('Name on the order:')
st.write('Name on the order:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session() #SiS code 
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('choose upto 5 ingredients :'
                                , my_dataframe
                                , max_selections=5)

if ingredients_list:
   # st.write(ingredients_list)
   # st.text(ingredients_list)
    ingredients_string=''
    

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon" + fruit_chosen )
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    time_to_submit = st.button('Submit Order')

    if time_to_submit:
        success_message="Your Smoothie is ordered", name_on_order, "!"
        session.sql(my_insert_stmt).collect()
        st.success(success_message, icon="✅")

    


