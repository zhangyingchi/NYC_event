# NYC_Event

## Group Information
Group name: Group 31

Class Section: Section 2

Group Member : 
+ Chi Zhang: cz2527
+ Haoran Tang: ht2491
+ Shangyou Wu: sw3320
+ Huimin Wang: hw2671

## Project Description


### Motivation:

When we started our study at Columbia University, we have realized that international students want to fit in the culture and attend interesting events while there is no way recommending events on New York City based on users’ location, interests and availability.

 

### Goal:

We want to design a project to fulfill the need for event recommendation for international students and everyone who eagers to engage in the activities and events in NYC. Meanwhile, companies can benefit from the gathered event information.

 
### Realization:



## Python Package Requirements
+ pandas
+ numpy
+ request
+ json
+ sodapy
+ gmaps
+ bokeh
+ folium
+ wordcloud


## Run Instructions

### Python File 

### GUI Events Filter 
We also provides a GUI filter for users to search the events

Bokeh_filter.ipynb provide function to construct a local server to run this GUI

This code should be executed on bash 

run **bokeh serve bokeh_filter.ipynb** 

follow the tips that display on the command line, open **http://localhost:5006/bokeh_filter** on broswer



for more instructions, please see https://hub.mybinder.org/user/bokeh-bokeh-notebooks-qx6owzax/notebooks/tutorial/11%20-%20Running%20Bokeh%20Applictions.ipynb



function:

type '1': find your favorate event

  step 1: 
  users can input the keyword, type and date for the future event they are interested in. As a result, a table matched their requirements will be returned. Detailed information about the events.
  step 2:
  users can choose what specific information they want to know about the event. If they type '1', a brief introduction about the event will be return.


type '2': show the frequency of events
  show the heatmap and word cloud of upcoming events in the following month.


type '3': the route to the event
  users can type the index of event. they need to input their starting location. A route will be returned.   
