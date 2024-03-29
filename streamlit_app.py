# Import python packages
import streamlit as st
import requests

from snowflake.snowpark.functions import col

# Write directly to the app

st.title(" :cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want with custom Smoothie!
    """);

name_on_order = st.text_input('Name on Smoothie:')
st.write('Name on Smoothie will be:', name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True);

ingradients_list=st.multiselect('Choose upto 5 ingradients:',my_dataframe)
ingredients_string=''
if ingradients_list:
    ingredients_string=''
    for fruit_choosen in ingradients_list:
        ingredients_string+=fruit_choosen+ " "
        st.subheader(fruit_choosen+'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choosen)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    #st.write(ingredients_string)
        
my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""


#st.write(my_insert_stmt)
time_to_insert=st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is Ordered!',icon="✅")



#st.text(fruityvice_response)


