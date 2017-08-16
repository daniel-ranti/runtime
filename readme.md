# What is this app?

1. A dinky website that tells you when you should go for a run today! Takes into account longitude and latitude at this point, and will tell you when you should run based on a preset ideal temperature. 

# What can you do with it? 

Not really that much. Hit it with a lon and a lat query param and it will return a list of forecast data by hour. Well its supposed to. It doesnt work right now. 

http://whenshouldirun.com/

# To Do list:

1. Restrict the hours that one can recieve for run suggestions. 
	1. build out the prediction algorithm: sliding scale for temperatures, humidity, wind gusts, etc
1. fix the query in the first place because that shit is borked
1. Build out a front end, so the user can input data and preferences 
	1. familiarize with jinja templates!
	1. clean up the output of the query
1. Get longitude and latitude by IP address
