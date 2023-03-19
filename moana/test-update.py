# Plot the lanes
import pandas as pd
import plotly.express as px

df = pd.DataFrame([
    {'Lane' : '1', 'Start time': '2023-03-19 05:30:00', 'End time': '2023-03-19 06:59:59', 'Activity': 'Dunedin Swim Coaching'},
    {'Lane' : '2', 'Start time': '2023-03-19 05:30:00', 'End time': '2023-03-19 06:59:59', 'Activity': 'Dunedin Swim Coaching'},
    {'Lane' : '3', 'Start time': '2023-03-19 05:30:00', 'End time': '2023-03-19 06:59:59', 'Activity': 'Dunedin Swim Coaching'},
    {'Lane' : '4', 'Start time': '2023-03-19 05:30:00', 'End time': '2023-03-19 06:59:59', 'Activity': 'Dunedin Swim Coaching'},
    
    {'Lane' : '5', 'Start time': '2023-03-19 05:30:00', 'End time': '2023-03-19 06:59:59', 'Activity': 'Public Swimming'},
    {'Lane' : '6', 'Start time': '2023-03-19 05:30:00', 'End time': '2023-03-19 06:59:59', 'Activity': 'Public Swimming'},
    {'Lane' : '7', 'Start time': '2023-03-19 05:30:00', 'End time': '2023-03-19 06:59:59', 'Activity': 'Public Swimming'},
    {'Lane' : '8', 'Start time': '2023-03-19 05:30:00', 'End time': '2023-03-19 06:59:59', 'Activity': 'Public Swimming'},
    
    {'Lane' : '1', 'Start time': '2023-03-19 07:00:00', 'End time': '2023-03-19 08:14:00', 'Activity': 'Public Swimming'},
    {'Lane' : '2', 'Start time': '2023-03-19 07:00:00', 'End time': '2023-03-19 08:14:00', 'Activity': 'Public Swimming'},
    {'Lane' : '3', 'Start time': '2023-03-19 07:00:00', 'End time': '2023-03-19 08:14:00', 'Activity': 'Public Swimming'},
    {'Lane' : '4', 'Start time': '2023-03-19 07:00:00', 'End time': '2023-03-19 08:14:00', 'Activity': 'Public Swimming'},
    {'Lane' : '5', 'Start time': '2023-03-19 07:00:00', 'End time': '2023-03-19 08:14:00', 'Activity': 'Public Swimming'},
    {'Lane' : '6', 'Start time': '2023-03-19 07:00:00', 'End time': '2023-03-19 08:14:00', 'Activity': 'Public Swimming'},
    {'Lane' : '7', 'Start time': '2023-03-19 07:00:00', 'End time': '2023-03-19 08:14:00', 'Activity': 'Public Swimming'},
    {'Lane' : '8', 'Start time': '2023-03-19 07:00:00', 'End time': '2023-03-19 08:14:00', 'Activity': 'Public Swimming'},
])

df['Start time'] = pd.to_datetime(df['Start time'])
df['End time'] = pd.to_datetime(df['End time'])

# df['Start time'] = df['Start time'].dt.strftime('%I:%M %p')
# df['End time'] = df['End time'].dt.strftime('%I:%M %p')

fig = px.timeline(df, x_start="Start time", x_end="End time", y="Lane", color="Activity")
fig.show()