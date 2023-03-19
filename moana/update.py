# Get todays pdf URL
import requests
from bs4 import BeautifulSoup # bs4
from datetime import datetime

# Parse todays pdf URL
import tabula # tabula-py

# Plot the lanes
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import plotly.graph_objs as go

def get_pdf_link(url):
    # Send a request to the URL and get the HTML response
    response = requests.get(url)
    html = response.text

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the <a> tags on the page
    a_tags = soup.find_all('a')

    # Extract the href attribute of each <a> tag
    hrefs = [a.get('href') for a in a_tags]

    # Filter the hrefs to only keep the ones that end with '.pdf' and contain the formatted date
    now = datetime.now()
    formatted_date = now.strftime("%a-%d") # TODO: remove this
    pdf_hrefs = [href for href in hrefs if href and href.endswith('.pdf')] # and formatted_date in href
    
    # Convert the hrefs to absolute URLs
    abs_pdf_hrefs = [requests.compat.urljoin(url, href) for href in pdf_hrefs]

    return abs_pdf_hrefs[-1] # Latest is always the last, so should be updated everyday at closing time

def extract_table_from_pdf(url):
    # Download the PDF file from the URL
    response = requests.get(url)
    with open('temp.pdf', 'wb') as f:
        f.write(response.content)
    f.close()

    # Extract the table data from the PDF file using Tabula
    df = tabula.read_pdf('temp.pdf', pages='all', multiple_tables=True, lattice=True)

    return df

def last_word(s):
    """
    Return the substring from the last whitespace character onward in the input string s.
    """
    last_space_index = s.rfind(' ')
    if last_space_index == -1:
        # If there are no whitespace characters in s, return s.
        return s
    else:
        # Otherwise, return the substring from the last whitespace character onward.
        return s[last_space_index+1:]
    
def laneify_item(row, max):
    if 'All' in row:
        start, end = 1, max
    elif '-' in row:
        start, end = map(int, row[row.rfind(' ')+1:].split('-'))
    else:
        start = end = row[-1]
    
    return ",".join(map(str, range(start,end+1)))  

def do_stuff_to_df(df):
    # Rename the columns to match the previous layout
    df.columns = ['Item', 'Start time', 'End time', 'Activity']

    # Exclude the first row, which contains the column names
    df = df.iloc[1:]

    # Convert the 'Start time' and 'End time' columns to datetime objects
    # df['Start time'] = pd.to_datetime(df['Start time'])
    # df['End time'] = pd.to_datetime(df['End time'])
    
    for index in df.index:
        df.loc[index, 'Item'] = laneify_item(df.loc[index,'Item'], 8)
    return df   

def plot_lanes(df):
    # TODO: Title based on first row
    # TODO: Check it removes the first row
    # TODO: Check parsing 1-3 style lanes is correct
    # TODO: Probably remove the 'Deep' part of lanes and use a range?
    
    # Otherwise thank mr gpt for helping with this project
    title = df.columns[0].replace('All ', '') # Deep main,
    
    # TODO: Dynamically caluclate this :)
    max_lanes = 8 # exclusive of the top
        
    good = ['Public Lane Swimming', 'Long Course Lane Swimming']
    # Define the pool lanes
    pool_lanes = range(1, max_lanes+1)
    pool_lanes = [str(num) for num in pool_lanes]

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Set the y-axis ticks and labels
    ax.set_yticks(range(len(pool_lanes)))
    ax.set_yticklabels(pool_lanes)


    # Hacky fix, but will ask chatgpt later
    # TODO: Fix this (original fix based on https://stackoverflow.com/questions/52696447/avoid-duplicate-legends-in-broken-barh)
    lbl_pool = []

    # Plot the activity bars for each pool lane
    for i, lane in enumerate(pool_lanes):
        lane_data = df[df['Item'].str.contains(lane)]
        for index, row in lane_data.iterrows():
            start_time = row['Start time']
            end_time = row['End time']
            activity = row['Activity']
            if activity in lbl_pool:
                prefix = '_'
            else:
                lbl_pool.append(activity)
                prefix=''  
            ax.barh(i, end_time - start_time, left=start_time, height=0.5, align='center', label=prefix+activity)

    # Set the x-axis label
    # TODO: Fix this https://stackoverflow.com/questions/66577395/python-plot-with-24-hrs-x-and-y-axis-using-only-hours-and-minutes-from-timestamp
    ax.set_xlabel('Time')
    hh_mm = DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(hh_mm)


    # Show the legend
    ax.legend()
    
    ax.set_title(title)

    # Show the plot
    plt.show()

def plot_lanes2(df):
    # TODO: Dynamically caluclate this :)
    max_lanes = 8 # exclusive of the top

    # Create plotly traces
    traces = []
    lanes = list(range(1, max_lanes+1))
    for i, row in df.iterrows():
        for lane in lanes:
            if str(lane) in row['Item']:
                trace = go.Bar(
                    x=[row['Start time'], row['End time']],
                    y=[lane],
                    orientation='h',
                    name=row['Item'],
                    text=f"Activity: {row['Activity']}<br>Start time: {row['Start time']}<br>End time: {row['End time']}",
                    hoverinfo='text'
                )
                traces.append(trace)
    
    # Create layout
    layout = go.Layout(
        title='Swim Lanes Schedule',
        xaxis=dict(
            title='Time',
            tickformat='%H:%M:%S'
        ),
        yaxis=dict(
            title='Lanes',
            tickvals=list(lanes),
            ticktext=[f"Lane {i}" for i in lanes]
        )
    )

    # Create figure
    fig = go.Figure(data=traces, layout=layout)

    # Show figure
    fig.show()

pdf_link = get_pdf_link('https://www.dunedin.govt.nz/news-and-events/public-notices/moana-pool-timetable')
print(pdf_link)

tables = extract_table_from_pdf(pdf_link)
# TODO: If sat/sunday, then check which day and start from deep 1 or deep 2 (or just display both for the weekend and have twice as many)

df = do_stuff_to_df(tables[0])

plot_lanes2(df)
