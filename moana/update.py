# Get todays pdf URL
import requests
from bs4 import BeautifulSoup # bs4
from datetime import datetime

# Parse todays pdf URL
import tabula # tabula-py

# Plot the lanes
import pandas as pd
import matplotlib.pyplot as plt

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
    formatted_date = now.strftime("%a-%d")
    pdf_hrefs = [href for href in hrefs if href and href.endswith('.pdf') and formatted_date in href]
    


    # Convert the hrefs to absolute URLs
    abs_pdf_hrefs = [requests.compat.urljoin(url, href) for href in pdf_hrefs]

    return abs_pdf_hrefs[0]

def extract_table_from_pdf(url):
    # Download the PDF file from the URL
    response = requests.get(url)
    with open('temp.pdf', 'wb') as f:
        f.write(response.content)
    f.close()

    # Extract the table data from the PDF file using Tabula
    df = tabula.read_pdf('temp.pdf', pages='all')

    return df

def plot_lanes(df):
    # TODO: Title based on first row
    # TODO: Check it removes the first row
    # TODO: Check parsing 1-3 style lanes is correct
    # TODO: Probably remove the 'Deep' part of lanes and use a range?
    
    # Otherwise thank mr gpt for helping with this project
    
    
    # Rename the columns to match the previous layout
    df.columns = ['Item', 'Start time', 'End time', 'Activity']

    # Exclude the first row, which contains the column names
    df = df.iloc[1:]

    # Convert the 'Start time' and 'End time' columns to datetime objects
    df['Start time'] = pd.to_datetime(df['Start time'])
    df['End time'] = pd.to_datetime(df['End time'])

    # Define the pool lanes
    pool_lanes = ['Deep 1', 'Deep 2', 'Deep 3', 'Deep 4']

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Set the y-axis ticks and labels
    ax.set_yticks(range(len(pool_lanes)))
    ax.set_yticklabels(pool_lanes)

    # Plot the activity bars for each pool lane
    for i, lane in enumerate(pool_lanes):
        lane_data = df[df['Item'].str.contains(lane)]
        for index, row in lane_data.iterrows():
            start_time = row['Start time']
            end_time = row['End time']
            activity = row['Activity']
            item = row['Item']
            if '-' in item:
                start_lane, end_lane = map(int, item.split('-'))
                lanes = range(start_lane, end_lane+1)
            else:
                lanes = [int(item.split()[-1])]
            for lane_num in lanes:
                ax.barh(i, end_time - start_time, left=start_time, height=0.5, align='center', label=activity)

    # Set the x-axis label
    ax.set_xlabel('Time')

    # Show the legend
    ax.legend()

    # Show the plot
    plt.show()



pdf_link = get_pdf_link('https://www.dunedin.govt.nz/news-and-events/public-notices/moana-pool-timetable')
print(pdf_link)

tables = extract_table_from_pdf(pdf_link)


plot_lanes(tables[0])
