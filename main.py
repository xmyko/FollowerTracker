import soundcloud
import os
# use a databse for some simple storage
import sqlite3
# use datetime to track when followers are counted
import datetime

#make keys for your username and password
# I have a secret and a id somewhere I need to find them

# create a database connection for the program to use 
connection = sqlite3.connect("soundcloud.db")
database = connection.cursor()

# initialize soundcloud connection for program
client = soundcloud.Client(client_id = os.environ['sc_client_id'], client_secret = os.environ['sc_apikey'], username = os.environ['sc_username'], password = os.environ['sc_password']  )

total_follows = client.get('/me').followers_count

# get the current time 
current_time = datetime.datetime.now()
# convert time to somthing more freindly to use, drop nanoseconds will look like 2021-06-18 02:31:19

string_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

print(f"the follower count is {total_follows} at {string_current_time}")

# test if database exists if not create it

database.execute("CREATE TABLE IF NOT EXISTS soundcloud_follows(key INTEGER PRIMARY KEY AUTOINCREMENT, follows INT(30), time_of_reading TEXT)" )

# make sure the database table is created with a commit
connection.commit()

# lets grab everything we recorded so far
database.execute("SELECT follows, time_of_reading FROM soundcloud_follows")

# database stores results here
result_rows= database.fetchall()

list_follows = list()
list_time_of_reading = list() # you could also say list_time_of_reading = []
for result_row in result_rows:
# matplotlib is picky about having a list of all the x values and a seperate list of the y_values
    if result_row[1] not in list_time_of_reading:
        # this keeps us from loading duplicate readings (our design should prevent this)  
        # but I was having problems with this in my program
        list_follows.append(result_row[0])
        list_time_of_reading.append(result_row[1])

# now that lists are constructed we can add the new readings

if string_current_time not in list_time_of_reading: # again no duplicates
    list_follows.append(total_follows)
    list_time_of_reading.append(string_current_time)
    # lets store the new data to the database
    database.execute("INSERT INTO soundcloud_follows (follows, time_of_reading) VALUES ( ?, ?)", (total_follows, string_current_time) )
    # lets make sure the data is added to the database
    connection.commit()
print(result_rows)