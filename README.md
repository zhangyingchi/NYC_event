# NYC_Event

## Group Information
Group name: Group 31, Class Section: Section 2

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
+ tkinter


## Run Instructions - Python File

Two method for running this python script.

### Terminal 




### Jupyter Notebook

Google Maps Widget can not show on terminal, some functions in option 3,5,6 cannot be seen if you run NYC_event.py on terminal



![GitHub](https://github.com/zhangyingchi/NYC_event/blob/master/images/wordcloud.png)



![GitHub](https://github.com/zhangyingchi/NYC_event/blob/master/images/map%20marker.png)


## Run Instructions - GUI Events Filter 
We also provides a GUI filter for users to search the events

Bokeh_filter.ipynb provide function to construct a local server to run this GUI

This code should be executed on bash 

run **bokeh serve bokeh_filter.ipynb** 

follow the tips that display on the command line, open **http://localhost:5006/bokeh_filter** on broswer

![GitHub](https://github.com/zhangyingchi/NYC_event/blob/master/images/bokeh%20filter.png)


for more instructions, please see https://hub.mybinder.org/user/bokeh-bokeh-notebooks-qx6owzax/notebooks/tutorial/11%20-%20Running%20Bokeh%20Applictions.ipynb   
