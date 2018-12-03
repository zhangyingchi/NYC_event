<div align="center">
  <img src="https://github.com/zhangyingchi/NYC_event/blob/master/images/Logo.png"><br>
</div>

-----------------
# Group Information
Group name: Group 31, Class Section: Section 2

# Project Description

### Motivation:

When we started our study at Columbia University, we have realized that international students want to fit in the culture and attend interesting events while there is no way recommending events on New York City based on users’ location, interests and availability.

### Goal:

We want to design a project to fulfill the need for event recommendation for international students and everyone who eagers to engage in the activities and events in NYC. Meanwhile, companies can benefit from the gathered event information.


# Python Package Requirements
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

# Run Instructions - Python File in terminal 

**Note that option 6 can only run in Windows, since tkinter package does not fullly support Mac OS**

+ open terminal at target file
+ type 
```
python NYC_event.py
```

## Option menu
+ Option 1: Data Initialization
+ Option 2: Events heatmap(this will take a little bit long, like 20 mins )
+ Option 3: Events wordcloud
+ Option 4: Search by Features
+ Option 5: Select a event
+ Option 6: Find route to the events
### Option 1: Data Initialization ###

> This data is provided by Office of Citywide Event Coordination and Management (CECM)

> NYC OPEN DATA provides the API to fetch the events data in the coming month.

> The dataset is updated daily

> Click here to see the reference: https://data.cityofnewyork.us/City-Government/NYC-Permitted-Event-Information/tvpp-9vvx

Download and initialize the dataset, this is the necessary step for option 2,3,4,5

![GitHub](https://github.com/zhangyingchi/NYC_event/blob/master/images/option1.PNG)

### Option 2: Events heatmap(this will take a little bit long, like 20 mins ) ###

This option doesn't work on terminal method, the google map would only work in jupyter notebook

### Option 3: Events wordcloud ###

![GitHub](https://github.com/zhangyingchi/NYC_event/blob/master/images/option3.PNG)

### Option 4: Search by Features ###

![GitHub](https://github.com/zhangyingchi/NYC_event/blob/master/images/option4.PNG)

We provide a events filter accoridng to the **event name,  event type,  start time,  borough and weekdays**

The format of function input should be :

+ event_name = string
+ event_type = string 
+ date = (yyyy,mm) or (yyyy,mm,dd)
+ borough = string
+ weekday = integer between 1-7, (1=Monday,7=Sunday)

### Option 5: Select a event ###


![GitHub](https://github.com/zhangyingchi/NYC_event/blob/master/images/map%20marker.png)

### Option 6: Find route to the events ###

![GitHub](https://github.com/zhangyingchi/NYC_event/blob/master/images/pop_up_interface.PNG)

![GitHub](https://github.com/zhangyingchi/NYC_event/blob/master/images/path.PNG)


Due to the supportting issue of gmaps package, the directions layer cannot be exported temporarily. 

# Run Instructions - GUI Events Filter 
We also provides a GUI filter for users to search the events

Bokeh_filter.ipynb provide function to construct a local server to run this GUI

This code should be executed on bash 

run 
```
bokeh serve bokeh_filter.ipynb
```

follow the tips that display on the command line, open **http://localhost:5006/bokeh_filter** on broswer

![GitHub](https://github.com/zhangyingchi/NYC_event/blob/master/images/bokeh%20filter.png)


*Due to the bokeh library issue, we temporarily do not support date filter on html*

for more instructions, please see https://hub.mybinder.org/user/bokeh-bokeh-notebooks-qx6owzax/notebooks/tutorial/11%20-%20Running%20Bokeh%20Applictions.ipynb   
