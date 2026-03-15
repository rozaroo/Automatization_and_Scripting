import pandas as pd
import matplotlib.pyplot as plt
import sendgrid 
from sendgrid.helpers.mail import Mail
import logging
import schedule
import time
import os
# Load the dataset
df = pd.read_csv("sports_data_missing.csv")
# limpiar espacios en nombres de columnas
df.columns = df.columns.str.strip()
# Display the first few rows
print(df.head())

# Display info about DataFrame
df.info()

# Drop rows with invalid data
df = df.dropna()
# Inspect the cleaned data
df.info()

# Function to create scatter plot
def create_scatter_plot(df, x_col, y_col, title):
    plt.figure(figsize = (10, 6)) # Figure size is provided
    # Make the plot a scatter plot with the DataFrame's x_col and y_col as parameters
    plt.scatter(df[x_col], df[y_col])
    # Set the plot title to the title parameter
    plt.title(title)
    # Set the x_label to the x_col parameter
    plt.xlabel(x_col)
    # Set the y_label to the y_col parameter
    plt.ylabel(y_col)
    # Switch gridlines on (True)
    plt.grid(True)
    plt.show()

create_scatter_plot(df, 'BB', 'SO', 'Walk (BB) vs Strikeout (SO) Ratio')
create_scatter_plot(df, 'HR', 'AB', 'Home Runs (HR) vs At Bats (AB) Ratio')

# Create box plots using Matplotlib
plt.figure(figsize = (10, 6)) 

# Set up data to contain the Singles, Doubles, Triples, and Home Runs from the DataFrame "df"
data = [df['Singles'].values, df['Doubles'].values,df['Triples'].values,df['HR'].values]

# Create the boxplot with specified options
plt.boxplot(data, vert=False, patch_artist=True) 
plt.yticks(range(1, 5), ['Singles', 'Doubles', 'Triples', 'Home Runs'])
# set xlabel to Hits
plt.xlabel('Hits')
# set ylabel to Hit Type
plt.ylabel('Hit Type')
# set title to Distribution of Hits
plt.title('Distribution of Hits')
# Switch gridlines on (True)
plt.grid(True)
plt.show()

# Remove all players with 0 walks or 0 strikeouts
df = df[(df['BB'] != 0) & (df['SO'] != 0)]

# Create column with Strikeout/Walk Ratio
df["SO/BB"] = df["SO"] / df["BB"]

# Calculate means
average_singles = df['Singles'].mean()
average_doubles = df['Doubles'].mean()
average_triples = df['Triples'].mean()
average_hr = df['HR'].mean()

# Calculate max and min SO/BB ratio
max_SO_BB = df["SO/BB"].max()
min_SO_BB = df["SO/BB"].min()

print(f"Singles: {average_singles}")
print(f"Doubles: {average_doubles}")
print(f"Triples: {average_triples}")
print(f"Home Runs: {average_hr}")
print(f"Max SO/BB Ratio: {max_SO_BB}")
print(f"Min SO/BB Ratio: {min_SO_BB}")

# Set up SendGrid API credentials
SENDGRID_API_KEY = 'F4kG7dL9pM2aB5nR8eJ1cK6oI3hN4gD5qE6fT7yU8wX9zA0bC1vM2aB5nR8eJ1cK6oI3h' # Replace with your API Key

sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)

message = Mail(
    from_email = 'admin@example.com',
    to_emails = 'rshah@example.com',
    subject = 'Analysis completed for today',
    plain_text_content = 'Baseball analysis is completed for today. Please view the statistics_CURRENT.csv to review details.'# YOUR CODE HERE - Add content
)

try:
    response = sg.send(message)
    logging.info("Email Sent Successfully") 
    
except Exception as e:
    logging.info("Email Message Failure") 

# Mock function for emailing a message. Call this function using schedule below.
def email_message():
    pass

# Schedule the job to run every day at 9 AM
schedule.every().day.at("09:00").do(email_message)

if os.path.exists(current_file):
    # Delete the old file
    if os.path.exists(old_file):
        os.remove(old_file)
        logging.info("Deleted old backup")
        
    # Rename the current file to old
    os.rename(current_file, old_file) 
    logging.info("Backed up current file") 
    
# Save the DataFrame to the new CSV file
df.to_csv(current_file, index=False)
logging.info("Statistics written to file")