# Get todays pdf URL
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Parse todays pdf URL
import tabula # tabula-py

# Plot the lanes
import pandas as pd
import plotly.express as px

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
        try:
            start = end = int(row[-1]) # Fails on Waterslides
        except:
            start = end = 1
    
    return ",".join(map(str, range(start,end+1)))  

def do_stuff_to_df(df, max_lanes):
    # Rename the columns to match the previous layout
    df.columns = ['Item', 'Start time', 'End time', 'Activity']

    # Exclude the first row, which contains the column names
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

MAX_LANES = 8 # TODO: Determine this number from the data

outputs = []
for table in tables:
    title = table.columns[0].replace(' ', '_').replace('/','-')
    df = do_stuff_to_df(table, MAX_LANES)

    fig = px.timeline(df, x_start="Start time", x_end="End time", y="Lane", color="Activity")
    
    if title not in outputs:
        fig.write_image(f'{title}.png')
        outputs.append(title)