import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import newspaper
import os

gemini_api_key = st.sidebar.text_input('Enter the Gemini API Key', type='password')

st.header('AI News Summarizer')

llm = ChatGoogleGenerativeAI(model = 'gemini-3.5-flash', temperature = 0.56, api_key = gemini_api_key)
news_url = st.text_input('Enter News URL')

def extract_article(url):
    article = newspaper.article(url)
    article.download()
    return {'title': article.title, 'text': article.text, 'authors': article.authors}


### LLM Chain

parser = StrOutputParser()
prompt = PromptTemplate.from_template(""" You are an experienced proessional News Analyst. Analyse the following news article and provide: 1) Executive Summary (under 250 words) 2) Key Highlights 
- Buller Points 3) Sentiment Analysis 4) Important Persons mentioned

Article: {article_text}""")

chain = prompt | llm | parser

col1, col2 = st.columns(2)
with col1:
    extract_btn = st.button('Extract News')

with col2:
    summarize_btn = st.button('Summarize News')


#Extract Article
article_data = None
if news_url:
    try:
        article_data = extract_article(news_url)
        
        if extract_btn:
            st.subheader('Article Details')
            st.markdown(f'{article_data["title"]}')
            
            st.write('** Authors **')
            st.write(" ".join(article_data['authors']) if article_data['authors'] else 'Not Available')
            st.write(authors)
            
            with st.expander('ReadFull Article'):
                st.write(article_data['text'])

    except:
        st.write('Unable to Extract News')

#Summarize Article
if summarize_btn:
    if not news_url:
        st.write('Enter the news URL first and then click on Summarize')
    else:
        try:
            article_data = extract_article(news_url)
            with st.spinner('Gemini is summarizing the news Article'):
            
                result = chain.invoke({'article_text': article_data['text']})

                st.subheader('AI generated News Summary')
                st.write(result)
                st.success('Summary generated successfully')
        except:
            st.write('Unable to Summarize')