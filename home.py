import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pyperclip
def main():
	st.set_page_config(page_title="Afternoon Check In", page_icon=None, layout='centered', initial_sidebar_state='auto')
	#Header
	st.title("The Afternoon Check In")
	st.markdown(getQuestion())
	st.markdown(getTeam(),unsafe_allow_html=True)
	if st.button(label = "foobar"):
		pyperclip.copy(getQuestion() + getTeam())


#reads from the deliveryTeam CSV and randomizes the list. Puts Andy last
def getTeam():

	andy = pd.DataFrame(["Andy"])
	teamList = pd.read_csv('deliveryTeam.csv',sep=",",header=None)
	teamList = teamList.sample(frac=1)	#This randomizes it?
	teamList = teamList.append(andy)
	teamList = teamList.to_html(header=None,index=None)
	return teamList
#This curls the webpage and magically gets the paragraph with the question
def getQuestion():
	page = requests.get('https://conversationstartersworld.com/random-question-generator')
	soup = BeautifulSoup(page.content,'html.parser')
	html = list(soup.children)[2]
	randomQuestion = soup.find_all('p')[3].getText()
	
	return randomQuestion

if __name__ == '__main__':
	main()