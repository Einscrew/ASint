## Admin
--

# Setup Buildings
To configure the building list:
(AUTHENTICATION MISSING)
```
method: PUT,
url: /API/admin/building/manage
datatype: "text",
contentType: "application/plainText",
data: 'buildingId1, buildingName1, lat1, lon1\n
       buildingId2, buildingName2, lat2, lon2\n '
```
The server will process each line, and retrieve the building that failed to insert,
in case of success the number of buildings inserted is returned

curl -X POST --data "@/home/einstein/IST/ASInt/repo/Project/src/buildings.txt" http://127.0.0.1:5000/API/admin/building/manage
	

--

# ListLoggedUsers
To receive the list of users that are logged-in in the system
```
method: POST,
url: /API/admin/users/loggedin
datatype: ,
contentType: ,
data:
```
__

# ListUsersInBuilding
--
```
method: POST,
url: /API/admin/building/#buildingID/users/
datatype: "",
contentType: "",
data: ""
```

# History
--

View all logs (probably best to segment all records)
```
method: POST,
url: '/API/admin/logs/',
```
Filter by:
- messages exganged within a builing
```
method: POST,
url: '/API/admin/building/#buildingID/logs/',
```
- messages & movements of a given user
```
method: POST,
url: '/API/admin/users/#userId/logs',
```

## Users

# Login

_Redirects_ user to fenix API login page, which after authentication redirects user to app homepage

# Send Message

Broadcasts msg to all users in certain range

```
method: POST
url: '/API/users/#istID/message'
datatype:'text' ,
contentType: 'text/plain',
data:'Hey there people near me'
```

# Set User Range

\#istID is the user identification
\#range is the range to be defined to the user

```
method: PUT
url: '/API/users/#istID/range/#range'
datatype:'' ,
contentType: '',
data:''
```

# Get users in range

Get users near the user
If he is in a certain building all users in the same will be retrieved

Shall current user's position be send?

```
method: POST
url: '/API/users/#istID/range/'
datatype: 'json',
contentType: 'application/json',
data:'{"lat":0.0000,"lon":12.3523}'
```

# Update user location

AWDNAWNAWJDAWLDBJAWJDBAWDJB
```
method: POST
url: '/API/users/#istID/range/'
datatype: 'json',
contentType: 'application/json',
data:'{"lat":0.0000,"lon":12.3523}'
```

# Get received messages

Should user periodicly apply for new messages or, only a callback function be used each time?

## Bots

# Register

Periodicity _crontab_ alike ??
```
method: POST
url: '/API/building/#buildingID/bot/register/'
datatype:'json' ,
contentType: 'application/json',
data:'{	"periodicity":"40 * 0 0 0 0",
	"message":"Communication:\n\t All useres should leave the build in 1 hour"}'
```
