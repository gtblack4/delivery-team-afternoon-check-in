import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from random import randrange

def main():
	st.set_page_config(page_title="Afternoon Check In", page_icon=None, layout='centered', initial_sidebar_state='auto')
	#Header
	st.title("The Afternoon Check In")
	st.text(getEasterText())

	team = getTeam()
	copyText = buildCopy(getTeam())
	copy_button = Button(label="Copy to Clipboard", width = 150, css_classes=['css-qbe2hsedgvbvh1'])
	copy_button.js_on_event("button_click", CustomJS(args=dict(copyText=copyText.to_csv(sep='\t',header=None,index=None)), code="""
    navigator.clipboard.writeText(copyText);"""))

	st.button("Refresh Question")
	
	no_event = streamlit_bokeh_events(
    copy_button,
    events="GET_TEXT",
    key="get_text",
    refresh_on_update=True,
    override_height=40,
    debounce_time=0)

	st.markdown(copyText.to_html(header=None,index=None),unsafe_allow_html=True,'style.css')
	
	#this is a container running the button code. Stolen from stack overflow. Not quite sure how it works
	

	
	
#Takes the team and randomizes the list, resets the index, and then puts Andy last

def buildCopy(team):
	team = pd.DataFrame(team)
	#needs the brackets to turn it to a dataframe
	question = [getQuestion()]
	andy = pd.DataFrame(["Andy"])

	#adds the question into -1 index
	team.loc[-1] = question
	#moves everything up
	team.index = team.index + 1
	#sorts the index back to normal
	copyText = team.sort_index()

	copyText = copyText.append(andy)
	return copyText

def getTeam():
	#reads from the csv file and randomizes the list
	teamList = pd.read_csv('deliveryTeam.csv',sep=",",header=None)
	teamList = teamList.sample(frac=1)	#This randomizes it?
	teamList.reset_index(drop=True,inplace=True)
	return teamList

#This curls the webpage and magically gets the paragraph with the question
def getQuestion():
	page = requests.get('https://conversationstartersworld.com/random-question-generator')
	soup = BeautifulSoup(page.content,'html.parser')
	html = list(soup.children)[2]
	randomQuestion = soup.find_all('p')[3].getText()
	
	return randomQuestion

def getEasterText():
	randInt = randrange(1,200)
	easterText = " "
	if randInt == 1:
		easterText = "please give me a raise"
	elif randInt == 2:
		easterText = "If you want to support our development. Venmo me @gtblack4"
	elif randInt == 3:
		easterText = "I developed this during work hours! Don't tell Andy."
	elif randInt== 4:
		easterText = "Thank you https://conversationstartersworld.com for supplying the questions"
	elif randInt== 5:
		easterText = "AHHHH"
	else:
		easterText = "Welcome to the Afternoon question Generator v1.3"
	return easterText

if __name__ == '__main__':
	main()