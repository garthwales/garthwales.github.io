# Get todays pdf URL
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Parse todays pdf URL
import tabula # tabula-py

# Plot the lanes
import pandas as pd
import plotly
import plotly.express as px

# Save files
import os
import shutil

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
        try:
            # Ends with number
            start, end = map(int, row[row.rfind(' ')+1:].split('-'))
        except:
            # Ends with text after number (eg 1-3 West)
            shorter = row[:row.rfind(' ')]
            start, end = map(int, shorter[shorter.rfind(' ')+1:].split('-'))
    else:
        try:
            start = end = int(row[-1]) # Fails on Waterslides
        except:
            start = end = 1
    
    return ",".join(map(str, range(start,end+1)))  

def do_stuff_to_df(df, max_lanes):
    # Remove any additional columns that aren't always there (e.g. comments)
    df = df.iloc[:, : 4]
    
    # Rename the columns to match the previous layout
    df.columns = ['Item', 'Start time', 'End time', 'Activity']

    # Exclude the first row, which contains the column names from extracting
    df = df.iloc[1:]

    # Convert the 'Start time' and 'End time' columns to datetime objects
    df['Start time'] = pd.to_datetime(df['Start time'])
    df['End time'] = pd.to_datetime(df['End time'])

    # Convert to 12hr time
    # df['Start time'] = df['Start time'].dt.strftime('%I:%M %p')
    # df['End time'] = df['End time'].dt.strftime('%I:%M %p')
    
    
    lanes = list(range(1, max_lanes+1))
    
    new_df = pd.DataFrame(columns =['Lane','Start time', 'End time', 'Activity'])

    for index in df.index:
        df.loc[index, 'Item'] = laneify_item(df.loc[index,'Item'], max_lanes)
        for lane in lanes:
            if str(lane) in df.loc[index, 'Item']:
                new_row = pd.DataFrame([{'Lane' : str(lane), 'Start time': df.loc[index,'Start time'], 'End time': df.loc[index,'End time'], 'Activity': df.loc[index,'Activity']}])
                new_df = pd.concat([new_df, new_row])
    
    return new_df   

pdf_link = get_pdf_link('https://www.dunedin.govt.nz/news-and-events/public-notices/moana-pool-timetable')
print(pdf_link)

tables = extract_table_from_pdf(pdf_link)
# TODO: If sat/sunday, then check which day and start from deep 1 or deep 2 (or just display both for the weekend and have twice as many)

MAX_LANES = 8 # TODO: Not hardcode total here

# TODO: Setup colours based on a dictionary...
# TODO: Either it is like using color_discrete_map in timeline
#       or use a dict to append another column and use the column to specify?

# Yellow for public lane and long course
# blue for aqua jogging
# red for Coaching / training (or for Facicility Closed)
# gold for club
# gold for championship
# Facility Closed
# polo
# synchronised
# diving
# Public Fun Area
# other greyed out colour for everything else?
# maybe something for 25m Lane hire

# TODO: take a screenshot and colour it in a photo editor, to visualise the palette and then set these (currently looks bad)
colour_map = {'Dunedin Swim Coaching':'rgb(30, 157, 247)', 'Long Course Lane Swimming':'rgb(247, 218, 30)', 'Pool Set-Up Short Course':'rgb(247, 218, 140)', 'Public Lane Swimming':'rgb(247, 243, 30)', 'Neptune Swim Club':'rgb(171, 30, 247)', 'Pool Staff Training':'rgb(236, 30, 247)', 'Aqua Jogging':'rgb(59, 30, 247)',}

# TODO:
# Just process every single link of the page...
# and then have tabs like https://www.w3schools.com/howto/howto_js_tabs.asp
# sat/sunday can be a single tab and just create images for all of them
    # and for sat/sunday use https://stackoverflow.com/questions/54634571/create-new-files-dont-overwrite-existing-files-in-python
    # to loop through the index of how many of that days things need to be made
    # make folders for each day

outputs = []
for table in tables:
    title = table.columns[0].replace(' ', '_').replace('/','-')
    df = do_stuff_to_df(table, MAX_LANES)

    fig = px.timeline(df,title=title, x_start="Start time", x_end="End time", y="Lane", color="Activity", color_discrete_map=colour_map)
    
    # Delete existing folder and create a new one
    if not os.path.exists('images-pool'):
        os.mkdir("images-pool")
    elif os.path.exists(f'images-pool/{title}.png'):
        os.remove(f'images-pool/{title}.png')
    
    fig.update_yaxes(categoryorder='array', categoryarray= ['1', '2', '3', '4', '5', '6', '7', '8']) # TODO: Not hardcode total here

    if title not in outputs:
        fig.write_image(f'images-pool/{title}.png')
        outputs.append(title)
        
        # TODO: Save each of these and imbed as iframe?
        # each < 10MB so is big for a website but doable? might be other better ways but eh
        plotly.offline.plot(fig,filename=f'images-pool/{title}.html',config={'displayModeBar': False})