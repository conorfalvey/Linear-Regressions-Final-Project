API_KEY = "" #Add key here
DB_USER = "postgres"
DB_PASSWORD = "" # postgres password

#Heres the commands to create the database table so it all inserts properly
'''
CREATE TABLE maps (
time integer,
route integer,
model varchar(40),
distance integer,
durationText varchar(40),
duration integer,
durationTrafficText varchar(40),
durationTraffic integer
);
'''
