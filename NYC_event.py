
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
import json
from sodapy import Socrata
import gmaps
import folium
import wordcloud
from tkinter import *
from tkinter.simpledialog import askstring
import matplotlib.pyplot as plt
import nltk
from scipy.misc.pilutil import imread, imsave,imresize
from wordcloud import WordCloud, STOPWORDS
from ipywidgets.embed import embed_minimal_html
import webbrowser


# In[2]:


ui='''
Choose your option (Please run the initialization first)
Option 1: Data Initialization 
Option 2: Events heatmap(this will take a little bit long, like 20 mins )
Option 3: Events wordcloud
Option 4: Search by Features
Option 5: Select a event
Option 6: Find route to the events 
'''

api_key = 'AIzaSyC3YTChJ9BafI70SDU4ZBcOcLvYumnSKW8'


# In[3]:


def get_data():
    MyAppToken='6v9nCt2L0Tftx31xuIhXQf5uv'
    username='cz2527@columbia.edu'
    password='Tools002'
    print ('Downloading From Internet......')
    client = Socrata('data.cityofnewyork.us',
                     MyAppToken,
                     username=username,
                     password=password)
    results = client.get("8end-qv57",limit=3000)
    print ('Download Complete!')
    df = pd.DataFrame.from_records(results)
    df['event_name']= df['event_name'].apply(lambda x:x.lower())
    df['event_id']= df['event_id'].apply(lambda x:int(x))
    return df


# In[4]:


def change_type(results_df,keywords,event_type):
    for i in range(len(results_df)):
        if results_df.loc[i]['event_type']=='Special Event':
            for j in keywords:
                if j in results_df.loc[i]['event_name']:
                    results_df.loc[i]['event_type']=event_type


# In[5]:


def initialize():
    global df
    print ('Initialize dataset......')
    change_type(df,('Closure','closure','CLOSED'),'Closure')
    change_type(df,('Construction','construction'),'Construction')
    change_type(df,('Maintenance',),'Maintenance')
    change_type(df,('Farmers Market',),'Farmers Market')
    #change_type(results_df,('Market',),'Special Market')
    change_type(df,('Celebration','celebration'),'Celebration')
    df['index']=df.index
    df['start_date_time']=df['start_date_time'].apply(lambda x: np.datetime64(x))
    df['end_date_time']=df['end_date_time'].apply(lambda x: np.datetime64(x))
    df['weekday']=df['start_date_time'].apply(lambda x: int(x.weekday())+1)
    df_show=df.iloc[:,[-2,6,3,5,-6,-4,1,-1]]
    print ('Complete!')
    return df_show


# In[6]:


def name_search(name,df): #
    df=df[df['event_name'].apply(lambda x: name.lower() in x.lower())]
    return df

def type_search(type_,df):
    df=df[df['event_type'].apply(lambda x: type_.lower() in x.lower())]
    return df

def date_search(time,df):# time format (yyyy,mm,dd)
    df=df[df['start_date_time'].apply(lambda x: (x.year==time[0])&(x.month==time[1])&(x.day==time[2]))]
    return df

def month_search(time,df):# time format (yyyy,mm)
    df=df[df['start_date_time'].apply(lambda x: (x.year==time[0])&(x.month==time[1]))]
    return df

def borough_search(borough,df):
    df=df[df['event_borough'].apply(lambda x: borough.lower() in x.lower())]
    return df

def weekday_search(weekday,df):
    df=df[df['weekday'].apply(lambda x: x==weekday)]
    return df


# In[7]:


def search(name=0,type_=0,date=0,borough=0,weekday=0):
    global df
    df_=df
    name=input('please enter the words that name contains, you can also skip it')
    type_=input ('please enter the event type, you can also skip it')
    try:
        date=tuple(input('''
please enter the date in one month
the format should be (yyyy,mm) or (yyyy,mm,dd)
you can also skip it 
'''))
    
    except:
        pass
    borough=input('please enter borough, you can also skip it')
    
    try:
        weekday=int(input('please enter 1-7 represented Mon-Sun, you can also skip it'))
    except:
        pass
    
    #search name
    if name !=0 and name !='':
        if type(name) is str:
            df_=name_search(name,df_)
        else:
            raise TypeError('Please enter name as string')
            
    #search type        
    if type_ !=0 and type_ !='':
        if type(type_) is str:
            df_=type_search(type_,df_)
        else:
            raise TypeError('Please enter type as string')
            
    #search date
    if date !=0 and date !='':
        if type(date) is tuple:
            if len(date)==3:
                df_=date_search(date,df_)
            elif len(date)==2:
                df_=month_search(date,df_)
        else:
            raise TypeError('Please enter date as tuple')
    
    #search weekday
    if weekday !=0:
        if type(weekday) is int:
            if 1<=weekday<=7:
                df_=weekday_search(weekday,df_)
            else:
                raise TypeError('weekday should be integer between 1 and 7')
        else:
            raise TypeError('Please enter weekday as int')
            
    #search borough        
    if borough !=0 and borough !='':
        if type(borough) is str:
            df_=borough_search(borough,df_)
        else:
            raise TypeError('Please enter borough as string')
        
    # check search result    
    if len(df_)==0:
        print ('No events found in the records, please check and search again!')
        return None
    else:
        print (str(len(df_))+' events are found in the coming month!')
        return df_


# In[8]:


def select():
    global df
    index=int(input('Please type the index of selected event'))
    if 0<=index<len(df):
        return df[df['index']==index]
    else:
        print('The index is out of range, please look carefully and try again!')
        select()

def to_dict(event):
    dict_=dict()
    dict_['event_name']=event.iloc[0,1]
    dict_['event_borough']=event.iloc[0,2]
    dict_['event_location']=event.iloc[0,3]
    dict_['event_type']=event.iloc[0,4]
    dict_['start_date_time']=event.iloc[0,5].ctime()
    dict_['end_date_time']=event.iloc[0,6].ctime()
    return dict_


# In[9]:


def get_location(address):
    global api_key
    address=address.replace(' ','+')
    url='https://maps.googleapis.com/maps/api/place/textsearch/json?key=%s&query=%s&fields=formatted_address'% (api_key,address) 
    response = requests.get(url)
    result = json.loads(response.content)
    try:
        location = result['results'][0]['geometry']['location']
        lat = location['lat']    
        lng = location['lng'] 
        return lat, lng
    except:
        address_=input('The location is ambiguous, please search on internet for the event location, type q to quit')
        if address_=='q':
            return 
        else:
            return get_location(address_)


# In[10]:


def map_marker(event): 
    gmaps.configure(api_key)
    location=get_location(event['event_location'])
    event_location=[location]
    info_box_template = '''
    <dl>
    <dt>Event Name</dt><dd>{event_name}</dd>
    <dt>Event Borough</dt>{event_borough}</dd>
    <dt>Event Location</dt>{event_location}</dd>
    <dt>Event Type</dt>{event_type}</dd>
    <dt>Event Borough</dt>{event_borough}</dd>
    <dt>Event Start</dt>{start_date_time}</dd>
    <dt>Event End</dt>{end_date_time}</dd>
    </dl>
    '''
    event_info = [info_box_template.format(**event)]
    marker_layer = gmaps.marker_layer(event_location,info_box_content=event_info)
    fig=gmaps.figure()
    fig.add_layer(marker_layer)
    return fig


# In[11]:


def find_path(start, end, method = 'BICYCLING'):
    "Method could be 'DRIVING','WALKING','BICYCLING','TRANSIT'"
    my_key = api_key
    gmaps.configure(api_key=my_key)
    
    start = str(start)
    end = str(end)
    start_location = get_location(start)
    end_location = get_location(end)
    
    fig = gmaps.figure()
    path = gmaps.directions_layer(start_location, end_location, travel_mode= method)#we can add waypoints and travel_mode
    fig.add_layer(path)

    return fig

def information_of_route(start, end, method):
    my_key = api_key
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&mode={method}&key={my_key}'
    response = requests.get(url)
    
    routes = response.json()['routes'][0]
    legs = routes['legs'][0]
    distance = legs['distance']['text']
    duration = legs['duration']['text']
    start, end = legs['start_address'], legs['end_address']
    
    print(f'It takes {duration} to go from {start} to {end} by {method} and the distance is {distance}')


# In[12]:


class mclass:
    def __init__(self,  window):
        self.window = window
        self.label = Label(window, text='We can help you find the right path!',font=("Arial Bold", 25))
        self.label_from = Label(window, text='from')
        self.box_start = Entry(window)
        self.label_to = Label(window, text='to')
        self.box_end = Entry(window)
        
        self.button_1 = Button (window, text="Drive", command=self.driving)
        self.button_2 = Button (window, text="Walk", command=self.walking)
        self.button_3 = Button (window, text="Transit", command=self.transit)
        self.button_4 = Button (window, text="Bicycle", command=self.bicycling)
        
        self.label.pack()
        self.label_from.pack()
        self.box_start.pack ()
        self.label_to.pack()
        self.box_end.pack ()
        self.button_1.pack()
        self.button_2.pack()
        self.button_3.pack()
        self.button_4.pack()
        
    def driving(self):
        start = self.box_start.get()
        end = self.box_end.get()
        fig = find_path(start, end, method = 'DRIVING')
        self.fig = fig
        information_of_route(start, end, method = 'DRIVING')
        from ipywidgets.embed import embed_minimal_html
        embed_minimal_html('export.html', views=[fig])
        import webbrowser
        webbrowser.open_new('export.html')
    
    def walking(self):
        start = self.box_start.get()
        end = self.box_end.get()
        fig = find_path(start, end, method = 'WALKING')
        self.fig = fig
        information_of_route(start, end, method = 'WALKING')
        from ipywidgets.embed import embed_minimal_html
        embed_minimal_html('export.html', views=[fig])
        import webbrowser
        webbrowser.open_new('export.html')
        
    def transit(self):
        start = self.box_start.get()
        end = self.box_end.get()
        fig = find_path(start, end, method = 'TRANSIT')
        self.fig = fig
        information_of_route(start, end, method = 'TRANSIT')
        from ipywidgets.embed import embed_minimal_html
        embed_minimal_html('export.html', views=[fig])
        import webbrowser
        webbrowser.open_new('export.html')
        
    def bicycling(self):
        start = self.box_start.get()
        end = self.box_end.get()
        fig = find_path(start, end, method = 'BICYCLING')
        self.fig = fig
        information_of_route(start, end, method = 'BICYCLING')
        from ipywidgets.embed import embed_minimal_html
        embed_minimal_html('export.html', views=[fig])
        import webbrowser
        webbrowser.open_new('export.html')


# In[13]:


def get_address(event_index):
    if 0<=event_index<len(df):
        address = df['event_location'].iloc[event_index]
        return address 
    else:
        print('The index is out of range, please look carefully and try again!')
        event_index = int(input('Please enter the index of the event that you are interested in:'))
        address = df['event_location'].iloc[event_index]
        return address
    
def get_zip_code(address):
    address=address.replace(' ','+')
    url='https://maps.googleapis.com/maps/api/place/textsearch/json?key=%s&query=%s&fields=formatted_address'% (api_key,address) 
    response = requests.get(url)
    result = json.loads(response.content)
    try:
        zip_code = result['results'][0]['formatted_address'].split('NY ')[1].split(',')[0]  # get zip code
        return zip_code
    except:
        return 'The location is ambiguous, you should search for detailed information by yourself.'
        pass


# In[14]:


def get_heatmap():
    address_1 = []            #list of address
    for i in range(len(df)):
        address_1.append(get_address(i))
        
    zip_code_list = []        #list of zip code(raw)
    for i in range(len(address_1)):
        zip_code_list.append(get_zip_code(address_1[i]))
        
    zip_code_list2 = []       #remove the wrong return
    for i in range(len(zip_code_list)):
        if zip_code_list[i] != 'The location is ambiguous, you should search for detailed information by yourself.':
            zip_code_list2.append(zip_code_list[i])
            
    zip_code_list3 = list(set(zip_code_list2))  #unique zip & sort
    zip_code_list3.sort()
    
    zip_count_list = []       #list of sizes of each zip code
    for i in range(len(zip_code_list3)):
        zip_count_list.append(zip_code_list2.count(zip_code_list3[i]))

    dict_zip = {"Zip Code" : zip_code_list3,
                "Size" : zip_count_list}
    sizes = pd.DataFrame(dict_zip)
    
    m = folium.Map(location = [40.7589,-73.9851],zoom_start=11)    #draw the heatmap

    m.choropleth(geo_data='zipcode.geojson', data=sizes,
                 columns=[ 'Zip Code','Size'],
                 key_on='feature.properties.postalCode',
                 fill_color='RdYlGn', fill_opacity=0.7, line_opacity=0.8,
                 legend_name='Distribution of Incidents')
    folium.LayerControl().add_to(m)
    
    return m


# In[15]:


def text_cloud(df):
    motive=df['event_name'].str.cat(sep = '-')

    words=nltk.tokenize.word_tokenize(motive)

    word_dist = nltk.FreqDist(words)
    stopwords = nltk.corpus.stopwords.words('english')

    origin_image = imread("20181201194036.png")
    origin_mask = origin_image
    words_without_stop = nltk.FreqDist(w for w in words if w not in stopwords) 
    wc = WordCloud(stopwords=STOPWORDS,background_color='white',mask=origin_mask, contour_width=3, 
                   contour_color='steelblue').generate(" ".join(words_without_stop))
    plt.imshow(wc)
    fig=plt.gcf()
    fig.set_size_inches(14,9)
    plt.axis('off')
    
    return plt.show()


# In[3]:


option=1
df=0
while option!='q':
    option=input(ui+'''
Type option number to continue
type "q" to end the program  ''')
    
    if option=='q':
        break
    try:
        option=int(option)
    except:
        print ("please type integer between 1 and 5")
        continue
    if option not in [1,2,3,4,5,6]:
        print ("please type integer between 1 and 5")
        continue
    
    # initialization 
    if option ==1:
        if df==0:
            df=get_data()
            df=initialize()
        else:
            print('you have already initialized it!')
            continue
    
    # heatmap 
    if option ==2:
        if df is 0:
            print ('Please initialize data first!')
            continue
        get_heatmap()
            
            
    # wordcloud
    if option ==3:
        if df is 0:
            print ('Please initialize data first!')
            continue
        print('working')
        text_cloud(df)
        
        
    #search feature 
    if option ==4:
        if df is 0:
            print ('Please initialize data first!')
            continue
        df_search =search()
        
        print(df_search)
    
    
    #select event
    if option ==5:
        if df is 0:
            print ('Please initialize data first!')
            continue
        event=select()
        event=to_dict(event)
        fig = map_marker(event)
        
        embed_minimal_html('export.html', views=[fig])
        
        webbrowser.open_new('export.html')
        

    #find route
    if option ==6:
        window= Tk()
        start= mclass (window)
        window.mainloop()

