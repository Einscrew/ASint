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

```
method: POST,
url: '/API/admin/logs/',
```
```
method: POST,
url: '/API/admin/building/#buildingID/logs/',
```

```
method: POST,
url: '/API/admin/users/#userId/logs',
```

## Users
