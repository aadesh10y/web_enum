import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Define the project tasks with their start and end dates
tasks = {
    'Task': [
        'Setup Project Environment',
        'Design GUI Layout',
        'Implement Input Fields',
        'Develop URL Request Handling',
        'Multithreading and Queue Setup',
        'Implement Proxy and User-Agent',
        'Develop Output and Filtering',
        'Add Save and Stop Functionality',
        'Testing and Debugging',
        'Finalize and Document Code'
    ],
    'Start': [
        '2024-08-01', '2024-08-02', '2024-08-03', '2024-08-04',
        '2024-08-05', '2024-08-06', '2024-08-07', '2024-08-08',
        '2024-08-09', '2024-08-10'
    ],
    'End': [
        '2024-08-02', '2024-08-03', '2024-08-04', '2024-08-05',
        '2024-08-06', '2024-08-07', '2024-08-08', '2024-08-09',
        '2024-08-10', '2024-08-15'
    ]
}

# Convert to DataFrame
df = pd.DataFrame(tasks)

# Convert the dates to datetime format
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])

# Calculate the duration of each task
df['Duration'] = df['End'] - df['Start']

# Create the Gantt chart
fig, ax = plt.subplots(figsize=(10, 6))

# Plot each task as a bar
for i, task in enumerate(df.itertuples(), 1):
    ax.barh(task.Task, task.Duration.days, left=task.Start)

# Format the x-axis to show dates
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# Add labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Task')
ax.set_title('Gantt Chart for Web Enumeration Tool Project')

# Show grid lines for better readability
ax.grid(True)

# Show the Gantt chart
plt.tight_layout()
plt.show()
