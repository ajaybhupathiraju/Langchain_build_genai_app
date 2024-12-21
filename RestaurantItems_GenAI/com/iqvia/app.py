import dotenv
import streamlit as st
from langchain.chains.llm import LLMChain
from dotenv import load_dotenv
import os

from langchain.chains.sequential import SequentialChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import OpenAI,ChatOpenAI
from langchain_openai import OpenAI

load_dotenv()
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["GORQ_API_KEY"]=os.getenv("GORQ_API_KEY")
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

llm = OpenAI(model="gpt-3.5-turbo-instruct",temperature=0.6)
name_prompt = "I want to open a restaurant for {name} food. please suggest just one good restaurant name."
items_prompt = "Please suggest top 5 good menu items for {restaurant}. Return it as a comma separated list."

st.title("Restaurant app")

cuisine = st.sidebar.selectbox("Select Cuisine",options=["Indian","Mexican","Italian","American"])
print('cuisine selected :{}'.format(cuisine))


def generate_restaurant_items(cuisine):
    prompt_name_template = PromptTemplate(
        input_variables=["name"],
        template=name_prompt
    )

    prompt_items_template = PromptTemplate(
        input_variables=["restaurant"],
        template=items_prompt
    )

    chain1 = prompt_name_template|llm|StrOutputParser()
    chain2 = prompt_items_template|llm|StrOutputParser()

    chain = chain1 | chain2 | StrOutputParser()

    res = chain.invoke({"name": cuisine})
    return res.strip().split(",")

if cuisine:
   menu_items =generate_restaurant_items(cuisine)
   st.write("** Menu items **")
   for item in menu_items:
       print('item :{}'.format(item))
       st.write(item)


