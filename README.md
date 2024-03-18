# ISS Tracker

## Description
This Python Flask application serves as a RESTful API for accessing real-time and historical data related to the International Space Station (ISS). It retrieves XML data from a NASA API endpoint, parses it, and exposes endpoints for querying information such as the ISS's current location, speed, altitude, and geoposition. Error handling is implemented to provide appropriate responses in case of any issues during data retrieval or processing.

## Files 
- `Dockerfile`: Specifies the instructions for building a Docker container, including dependencies and configurations necessary to run the application.
- `README.md`: Provides guidance and instructions on how to use the ISS API, including setup, endpoints, and examples.
- `diagram.png`: Offers a visual representation of the architecture of the ISS tracking system, illustrating components and their interactions.
- `docker-compose.yml`: Defines a multi-container Docker application, automating the deployment and management of the Docker containers.
- `iss_tracker.py`: The main Python script responsible for fetching, parsing, and serving ISS trajectory data through a Flask server, handling requests from clients.
- `requirements.txt`: Lists the Python packages and versions required by the ISS tracking system, facilitating easy installation of dependencies.
- `test/test_iss_tracker.py`: Contains unit tests for the iss_tracker.py script, verifying its functionality and ensuring the reliability of the API's endpoints.

  ## Citation

  ### Data
  - The ISS data comes directly from NASA's website which is the most updated and recent data regarding the International Space Station. The data is presented as a .txt and .XML, for this script, we will be using the .XML:
[     https://spotthestation.nasa.gov/trajectory_data.cfm 
](https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml)https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml

Click the link above to download the data and save it to the same folder as your python script.

## How to Run

<details>
<summary>Containerized App</summary>
- To begin, head over to the directory that contains both the Dockerfile and the docker-compose.yml files.
- Build the Docker image using the command:
  
  `docker build -t username/flask-app:1.0 .`

  Replace username and flask-app with your own respective information.

- Then run the following Docker command which will start the container and run the Flask app inside of it.
     
  `docker-compose up`
</details>

<details>
<summary>Routes and Outputs</summary>

### Once your Flask app is running properly, you can curl several endpoints using the command:


`curl 127.0.0.1:5000/comment`
 - **Output:** This endpoint is a 'GET' method that will return the 'comment' dictionary associated with the ISS .XML file.

`curl 127.0.0.1:5000/header` 
- **Output:** This endpoint is a 'GET' method that will return the 'header' dictionary associated with the ISS .XML file.

`curl 127.0.0.1:5000/metadata` 
- **Output:** This endpoint is a 'GET' method that will return the 'metadata' dictionary associated with the ISS .XML file.

`curl 127.0.0.1:5000/epochs` 
- **Output:** This endpoint is a 'GET' method that will return the entire data set of epochs associated with the ISS in the .XML file.

`curl 127.0.0.1:5000/epochs/epochs?limit=int&offset=int` 
- **Output:** This endpoint is a 'GET' method that includes query parameters limit and offset are included in the request with their respective integer values. This endpoint is designed to retrieve a list of ISS state vectors with optional pagination using the limit and offset parameters.
- **limit**: The number of epoch records to return.
- **offset**: The starting position in the data set.

`curl 127.0.0.1:5000/epochs/<epoch>`
- **Output:** This endpoint is a 'GET' method that will return the state vectors for a specific epoch from the data set.
- The epoch should be an exact epoch from the data, such as `curl 127.0.0.1:5000/epochs/2024-075T13:56:00.000Z`

`curl 127.0.0.1:5000/epochs/<epoch>/speed`
- **Output:** This endpoint is a 'GET' method that will return the instantaneous speed for a specific epoch from the data set.
- The epoch should be an exact epoch from the data, such as `curl 127.0.0.1:5000/epochs/2024-075T13:56:00.000Z/speed`

`curl 127.0.0.1:5000/epochs/<epoch>/location`
- **Output:** This endpoint is a 'GET' method that will return the location data (latitude, longitude, altitude, and geoposition) for a specific epoch from the data set.
- The epoch should be an exact epoch from the data, such as `curl 127.0.0.1:5000/epochs/2024-075T13:56:00.000Z/location`

`curl 127.0.0.1:5000/now`
- **Output:** This endpoint is a 'GET' method that will return instantaneous speed, latitude, longitude, altitude, and geoposition for the epoch that is nearest in time to when the program is run.

</details>

<details>
<summary>Example Curl</summary>
  
`curl 127.0.0.1:5000/comment`

```
["Units are in kg and m^2",
"MASS=459154.20",
"DRAG_AREA=1487.80",
"DRAG_COEFF=2.00",
"SOLAR_RAD_AREA=0.00",
"SOLAR_RAD_COEFF=0.00",
"Orbits start at the ascending node epoch",
"ISS first asc. node: EPOCH = 2024-03-15T13:05:34.170 $ ORBIT = 402 $ LAN(DEG) = 49.49781",
"ISS last asc. node : EPOCH = 2024-03-30T10:42:10.141 $ ORBIT = 633 $ LAN(DEG) = -3.07552",
"Begin sequence of events","TRAJECTORY EVENT SUMMARY:",null,
"|       EVENT        |       TIG        | ORB |   DV    |   HA    |   HP  |",
"|                    |       GMT        |     |   M/S   |   KM    |   KM    |",
"|                    |                  |     |  (F/S)  |  (NM)   |  (NM)   |",
"=============================================================================",
"71S Launch            081:13:21:19.000             0.0     425.0     412.5",
"(0.0)   (229.5)   (222.8)",null,"71S Docking           081:16:39:42.000             0.0     425.0     412.5",
"(0.0)   (229.5)   (222.7)",
null,"SpX-30 Launch         081:20:55:09.000             0.0     425.0     412.6","(0.0)   (229.5)   (222.8)",
null,"SpX-30 Docking        083:11:30:00.000             0.0     425.3     412.0","(0.0)   (229.6)   (222.4)",
null,"============================================================================="
,"End sequence of events"]
```

`curl 127.0.0.1:5000/header`

```
{"CREATION_DATE":"2024-075T20:59:30.931Z",
"ORIGINATOR":"JSC"}
```

`curl 127.0.0.1:5000/metadata`

```
{
  "CENTER_NAME":"EARTH",
  "OBJECT_ID":"1998-067-A",
  "OBJECT_NAME":"ISS",
  "REF_FRAME":"EME2000",
  "START_TIME":"2024-075T12:00:00.000Z",
  "STOP_TIME":"2024-090T12:00:00.000Z",
  "TIME_SYSTEM":"UTC"
}
```

`curl 127.0.0.1:5000/epochs`

```
....
{
    "EPOCH": "2024-090T10:50:00.000Z",
    "X": 6211.00796878096,
    "X_DOT": -2.71881392442844,
    "Y": 593.261757779672,
    "Y_DOT": 4.94514472792443,
    "Z": 2679.1792595489,
    "Z_DOT": 5.19004672600028
  },
  {
    "EPOCH": "2024-090T10:54:00.000Z",
    "X": 5340.04172598131,
    "X_DOT": -4.49467498035985,
    "Y": 1744.01482432719,
    "Y_DOT": 4.58581135053425,
    "Z": 3811.63886071994,
    "Z_DOT": 4.18928581945629
  },
  {
    "EPOCH": "2024-090T10:58:00.000Z",
    "X": 4079.90977424504,
    "X_DOT": -5.94202859515296,
    "Y": 2767.67650101493,
    "Y_DOT": 3.89261089629353,
    "Z": 4665.53989721581,
    "Z_DOT": 2.88305607823398
  }...
```

`curl 127.0.0.1:5000/epochs/2024-090T10:58:00.000Z`

```
  {
    "EPOCH": "2024-090T10:58:00.000Z",
    "X": 4079.90977424504,
    "X_DOT": -5.94202859515296,
    "Y": 2767.67650101493,
    "Y_DOT": 3.89261089629353,
    "Z": 4665.53989721581,
    "Z_DOT": 2.88305607823398
  }
```

`curl 127.0.0.1:5000/epochs/2024-090T10:58:00.000Z/speed`

```
"7.666298700533425"
```

`curl 127.0.0.1:5000/epochs/2024-090T10:58:00.000Z/location`

```
{
  "Altitude":416.6976987197977,
  "EPOCH":"2024-090T10:58:00.000Z",
  "Geoposition":"Location currently unavailable",
  "Latitude":43.42081705210838,
  "Longitude":49.65167711498843
}
```
- If Geopositon shows "Location currently unavailable" this means the epoch  Latitude and Longitude are over a body of water.


`curl 127.0.0.1:5000/now`

```
{
  "Altitude":428.22771790667775,
  "EPOCH":"2024-078T19:48:00.000Z",
  "Geoposition":"Location currently unavailable",
  "Latitude":-42.81339797977896,
  "Longitude":-120.94411834789345,
  "Speed":"7.654282674187185",
  "X":4975.90962226887,
  "X_DOT":3.22096430613272,
  "Y":-343.072998653738,
  "Y_DOT":6.25756433003512,
  "Z":-4620.84857737651,
  "Z_DOT":3.00937216881748
}
```
- If Geopositon shows "Location currently unavailable" this means the current Latitude and Longitude of the ISS are over a body of water.

  
</details>











