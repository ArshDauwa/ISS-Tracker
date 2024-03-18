# ISS Tracker

## Description
This Python Flask application serves as a RESTful API for accessing real-time and historical data related to the International Space Station (ISS). It retrieves XML data from a NASA API endpoint, parses it, and exposes endpoints for querying information such as the ISS's current location, speed, altitude, and geoposition. Error handling is implemented to provide appropriate responses in case of any issues during data retrieval or processing.

## Files 
- `Dockerfile`: Specifies the instructions for building a Docker container, including dependencies and configurations necessary to run the application.
- `README.md`: Provides guidance and instructions on how to use the ISS API, including setup, endpoints, and examples.
- `diagram.png`: Offers a visual representation of the architecture of the ISS tracking system, illustrating components and their interactions.
- `docker-compose.yml`: Defines a multi-container Docker application, automating the deployment and management of the Docker containers.
- `iss_tracker.py`: The main Python script responsible for fetching, parsing, and serving ISS trajectory data through a Flask server, handling requests from clients.
-`requirements.txt`: Lists the Python packages and versions required by the ISS tracking system, facilitating easy installation of dependencies.
- `test/test_iss_tracker.py`: Contains unit tests for the iss_tracker.py script, verifying its functionality and ensuring the reliability of the API's endpoints.












