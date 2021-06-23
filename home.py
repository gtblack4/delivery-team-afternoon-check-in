import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
def main():
	st.set_page_config(page_title="Afternoon Check In", page_icon=None, layout='centered', initial_sidebar_state='auto')
	#Header
	st.title("The Afternoon Check In")
	team = getTeam()
	copyText = buildCopy(team)
	#question = pd.DataFrame[question]

	#teamList = team.to_html(header=None,index=None)
	#st.write(getQuestion())
	st.markdown(copyText.to_html(header=None,index=None),unsafe_allow_html=True)
	

	#st.dataframe(df)
	
	
	copy_button = Button(label="Copy to Clipboard")

	copy_button.js_on_event("button_click", CustomJS(args=dict(copyText=copyText.to_csv(sep='\t',header=None,index=None)), code="""
    navigator.clipboard.writeText(copyText);
    """))

	no_event = streamlit_bokeh_events(
    copy_button,
    events="GET_TEXT",
    key="get_text",
    refresh_on_update=True,
    override_height=75,
    debounce_time=0)
	
#reads from the deliveryTeam CSV and randomizes the list. Puts Andy last

def buildCopy(team):
	team = pd.DataFrame(team)
	question = [getQuestion()]
	andy = pd.DataFrame(["Andy"])
	



	team.loc[-1] = question
	team.index = team.index + 1

	copyText = team.sort_index()

	copyText = copyText.append(andy)
	return copyText

def getTeam():
	
	teamList = pd.read_csv('deliveryTeam.csv',sep=",",header=None)
	teamList = teamList.sample(frac=1)	#This randomizes it?
	
	#st.write(teamList)
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

