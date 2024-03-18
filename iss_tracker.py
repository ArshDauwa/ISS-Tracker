# !/usr/bin/env python3
from flask import Flask, request, jsonify
import math
import logging
import requests
import xmltodict
import numpy as np
from datetime import datetime
from typing import Union, Dict, Tuple, List
from geopy.geocoders import Nominatim


app = Flask(__name__)


url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'




def get_data(url: str) -> List[Dict[str, float]]:
    """
    Fetches data from a given URL, parses it as XML, and extracts relevant information.

    Parameters:
        url (str): The URL from which to fetch the XML data.

    Returns:
        list: A list of dictionaries containing ISS state vector data.
              Each dictionary represents a state vector with keys 'EPOCH', 'X', 'Y', 'Z', 'X_DOT', 'Y_DOT', and 'Z_DOT'.
    """

    response = requests.get(url)
    response.raise_for_status()
    data = xmltodict.parse(response.content)
    
    iss_data = []
    for state_vector in data['ndm']['oem']['body']['segment']['data']['stateVector']:
        iss_data.append({
            'EPOCH' : state_vector['EPOCH'],
        
            'X' : float(state_vector['X']['#text']),

            'Y' : float(state_vector['Y']['#text']),
            'Z' : float(state_vector['Z']['#text']),

            'X_DOT' : float(state_vector['X_DOT']['#text']),
            'Y_DOT' : float(state_vector['Y_DOT']['#text']), 
            'Z_DOT' : float(state_vector['Z_DOT']['#text'])

	})
	
    return iss_data 	

  
def calculate_lat(epochs: str) -> float:
    """
    Calculate the latitude based on the state vector data for a given epoch.

    Parameters:
        epochs (str): The epoch for which to calculate the latitude.

    Returns:
        float: The calculated latitude.
        
    Raises:
        ValueError: If the epoch is not found in the data.
    """    
    try:
        data = get_data(url)
    
        for state_vector in data:
            if state_vector['EPOCH'] == epochs:
               x = float(state_vector['X'])
               y = float(state_vector['Y'])
               z = float(state_vector['Z'])

               latitude = math.degrees(math.atan2(z, math.sqrt(x**2 + y**2)))
               return float(latitude)
        raise ValueError(f"Epoch '{epochs}' not found in the data.")
    
    except (ValueError, KeyError) as e:
        # Handle exceptions and return None
        print(f"Error: {e}")
        return None


def calculate_alt(epochs: str) -> float:
    """
    Calculate the altitude based on the state vector data for a given epoch.

    Parameters:
        epochs (str): The epoch for which to calculate the altitude.

    Returns:
        float: The calculated altitude.
        
    Raises:
        ValueError: If the epoch is not found in the data.
    """

    MEAN_EARTH_RADIUS = 6371.0088  

    try:
        data = get_data(url)

        for state_vector in data:
            if state_vector['EPOCH'] == epochs:
               x = float(state_vector['X'])
               y = float(state_vector['Y'])
               z = float(state_vector['Z'])
  
               altitude = math.sqrt(x**2 + y**2 + z**2) - MEAN_EARTH_RADIUS 

               return float(altitude)

        raise ValueError(f"Epoch '{epochs}' not found in the data.")
    
    except (ValueError, KeyError) as e:
        # Handle exceptions and return None
        print(f"Error: {e}")
        return None


def calculate_long(epochs: str) -> float:
    """
    Calculate the longitude based on the state vector data for a given epoch.

    Parameters:
        epochs (str): The epoch for which to calculate the longitude.

    Returns:
        float: The calculated longitude.
        
    Raises:
        ValueError: If the epoch is not found in the data.
    """
    try:
        data = get_data(url)

        parsed_timestamp = datetime.strptime(epochs, '%Y-%jT%H:%M:%S.%fZ') 
        hrs = int(parsed_timestamp.strftime('%H'))
        mins = int(parsed_timestamp.strftime('%M'))

        for state_vector in data:
            if state_vector['EPOCH'] == epochs:
               x = float(state_vector['X'])
               y = float(state_vector['Y'])
               z = float(state_vector['Z'])

               longitude = math.degrees(math.atan2(y, x)) - ((hrs-12)+(mins/60))*(360/24) 

               if longitude > 180:
                  longitude = -180 + (longitude - 180)
               elif longitude < -180:
                  longitude = 180 + (longitude + 180)

               return float(longitude) 
        raise ValueError(f"Epoch '{epochs}' not found in the data.")
    
    except (ValueError, KeyError) as e:
        # Handle exceptions and return None
        print(f"Error: {e}")
        return None

def calculate_geoposition(lat: float, long: float) -> Union[str, None]:
    """
    Calculate the geoposition (address) based on the latitude and longitude.

    Parameters:
        lat (float): Latitude coordinate.
        long (float): Longitude coordinate.

    Returns:
        Union[str, None]: The geoposition (address) if available, or "Location currently unavailable" if not available.
        
    Raises:
        Exception: If there is an error retrieving the ISS location.
    """     
    try:    
       geocoder = Nominatim(user_agent='iss_tracker')
       geoloc = geocoder.reverse((f"{lat},{long}"), zoom=15, language='en')
    
       if geoloc is None:
          return "Location currently unavailable"
       else:
          return geoloc.address   
 
    except Exception as e:
        logging.error(f"Error in calculate_geoposition: {e}")
        raise Exception("Error retrieving ISS location")

    
@app.route('/epochs', methods = ['GET'])
def epochs() -> Union[List[Dict[str, float]], Tuple[Dict[str, str], int]]:
    """
    Retrieves ISS state vector data and handles optional limit and offset parameters.

    Returns:
        list: A list of dictionaries containing ISS state vector data.
              Each dictionary represents a state vector with keys 'EPOCH', 'X', 'Y', 'Z', 'X_DOT', 'Y_DOT', and 'Z_DOT'.
        tuple: A tuple containing an error message dictionary and HTTP status code if an error occurs.
    """    
    data = get_data(url)
    
    try:
        limit = request.args.get('limit', default = None, type = int) 
        offset = request.args.get('offset', default = 0, type = int)
        
        if limit is not None:
           data = data[offset:offset + limit]
        return data
       
    except Exception as e:
        logging.error(f"Error in get_epochs: {e}")
        return {"error": str(e)}, 500


@app.route('/epochs/<epoch>', methods = ['GET'])
def state_vectors(epoch: str) -> Union[Dict[str, float], Tuple[Dict[str, str], int]]:
    """
    Retrieves state vector data for a specific epoch.

    Parameters:
        epoch (str): The epoch for which to retrieve the state vector data.

    Returns:
        dict: A dictionary containing the state vector data for the specified epoch.
        tuple: A tuple containing an error message dictionary and HTTP status code if the specified epoch is not found.
    """
    data = get_data(url)
    for i in range(len(data)):
        if (data[i]['EPOCH'] == epoch):
           return data[i]


@app.route('/epochs/<epoch>/speed', methods = ['GET'])
def instantaneous_speed(epoch: str) -> Union[str, Tuple[Dict[str, str], int]]:
    """
    Calculates the instantaneous speed for a specific epoch.

    Parameters:
        epoch (str): The epoch for which to calculate the instantaneous speed.

    Returns:
        str: The calculated instantaneous speed as a string.
        tuple: A tuple containing an error message dictionary and HTTP status code if the specified epoch is not found or an error occurs during calculation.
     """
    try:
        data = get_data(url)
    
        for i in range(len(data)):
            if (data[i]['EPOCH'] == epoch):
                x_dot = float(data[i]['X_DOT'])
                y_dot = float(data[i]['Y_DOT'])
                z_dot = float(data[i]['Z_DOT'])
 
                speed =  str(math.sqrt((x_dot**2) + (y_dot**2) + (z_dot**2)))

                return jsonify(speed)
    except Exception as e:
        logging.error(f"Error in get_epochs: {e}")
        return {"error": str(e)}, 500    
	

@app.route('/now', methods = ['GET'])
def nearest_epoch() -> Union[Dict[str, Union[str, float]], Tuple[Dict[str, str], int]]:
    """
    Finds the nearest epoch to the current time and calculates its speed, latitude, longitude, altitude, and geoposition.

    Returns:
       dict: A dictionary containing information about the nearest epoch, including its epoch time, calculated speed, latitude, altitude, longitude, and geopositon.
       tuple: A tuple containing an error message dictionary and HTTP status code if an error occurs during calculation.
    """
    try:
        data = get_data(url)
        current_time = datetime.utcnow()
               
        closest_epoch = min(data, key = lambda vector: abs(datetime.strptime(vector["EPOCH"], "%Y-%jT%H:%M:%S.%fZ") - current_time))
      
        closest_speed = str(math.sqrt((closest_epoch['X_DOT']**2) + (closest_epoch['Y_DOT']**2) + (closest_epoch['Z_DOT']**2)))
        lat = calculate_lat(closest_epoch['EPOCH'])
        alt = calculate_alt(closest_epoch['EPOCH'])
        longitude = calculate_long(closest_epoch['EPOCH'])
        geoloc = calculate_geoposition(lat,longitude)
 
        if longitude > 180:
           longitude = -180 + (longitude - 180) 
        elif longitude < -180:
             longitude = 180 + (longitude + 180)
     
        closest_epoch['Speed'] = closest_speed
        closest_epoch['Latitude'] = lat
        closest_epoch['Altitude'] = alt   
        closest_epoch['Longitude'] = longitude
        closest_epoch['Geoposition'] = geoloc
        
        return jsonify(closest_epoch)

    except Exception as e:
        logging.error(f"Error in get_epochs: {e}")
        return {"error": str(e)}, 500


@app.route('/epochs/<epoch>/location', methods=['GET'])
def location(epoch: str) -> dict:
    """
    Retrieve the location information for a given epoch.

    Parameters:
        epoch (str): The epoch for which to retrieve the location information.

    Returns:
        dict: A dictionary containing the location information.
              The dictionary includes the following keys:
              - 'EPOCH': The provided epoch.
              - 'Latitude': The latitude of the International Space Station (ISS).
              - 'Longitude': The longitude of the ISS.
              - 'Altitude': The altitude of the ISS.
              - 'Geoposition': The geoposition (address) of the ISS.

    Raises:
        Exception: If there is an error retrieving location information.
    """
    try:
        data = get_data(url)
        iss_data_location = {}

        for state_vector in data:
            if state_vector['EPOCH'] == epoch:
                x = float(state_vector['X'])
                y = float(state_vector['Y'])
                z = float(state_vector['Z'])
        
        lat = calculate_lat(epoch)
        long = calculate_long(epoch)
        alt = calculate_alt(epoch)
        geoLoc = calculate_geoposition(lat, long)

        iss_data_location['EPOCH'] = epoch
        iss_data_location['Latitude'] = lat
        iss_data_location['Longitude'] = long
        iss_data_location['Altitude'] = alt
        iss_data_location['Geoposition'] = geoLoc

        return jsonify(iss_data_location)
    
    except Exception as e:
        logging.error(f"Error in location route: {e}")
        raise Exception("Error retrieving location information")


@app.route('/comment', methods=['GET'])
def return_comment() -> Union[dict, str]:
    """
    Retrieve the comment from the ISS data.

    Returns:
        Union[dict, str]: If successful, returns a dictionary containing the comment from the ISS data.
                          If an error occurs, returns an error message as a string.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = xmltodict.parse(response.content)
        
        # Extract comment from the ISS data
        iss_data = {'COMMENT': data['ndm']['oem']['body']['segment']['data']['COMMENT']}
        
        return jsonify(iss_data['COMMENT'])
    
    except Exception as e:
        logging.error(f"Error in return_comment route: {e}")
        return "Error retrieving comment from ISS data"


@app.route('/header', methods=['GET'])
def return_header() -> Union[dict, str]:
    """
    Retrieve the header information from the ISS data.

    Returns:
        Union[dict, str]: If successful, returns a dictionary containing the header information from the ISS data.
                          If an error occurs, returns an error message as a string.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = xmltodict.parse(response.content)
        
        # Extract header information from the ISS data
        iss_data = {
            'CREATION_DATE': data['ndm']['oem']['header']['CREATION_DATE'],
            'ORIGINATOR': data['ndm']['oem']['header']['ORIGINATOR']
        }
        
        return jsonify(iss_data)
    
    except Exception as e:
        logging.error(f"Error in return_header route: {e}")
        return "Error retrieving header information from ISS data"


@app.route('/metadata', methods=['GET'])
def return_metadata() -> Union[dict, str]:
    """
    Retrieve the metadata information from the ISS data.

    Returns:
        Union[dict, str]: If successful, returns a dictionary containing the metadata information from the ISS data.
                          If an error occurs, returns an error message as a string.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = xmltodict.parse(response.content)
        
        # Extract metadata information from the ISS data
        iss_data = {
            'OBJECT_NAME': data['ndm']['oem']['body']['segment']['metadata']['OBJECT_NAME'],
            'OBJECT_ID': data['ndm']['oem']['body']['segment']['metadata']['OBJECT_ID'],
            'CENTER_NAME': data['ndm']['oem']['body']['segment']['metadata']['CENTER_NAME'],
            'REF_FRAME': data['ndm']['oem']['body']['segment']['metadata']['REF_FRAME'],
            'TIME_SYSTEM': data['ndm']['oem']['body']['segment']['metadata']['TIME_SYSTEM'],
            'START_TIME': data['ndm']['oem']['body']['segment']['metadata']['START_TIME'],
            'STOP_TIME': data['ndm']['oem']['body']['segment']['metadata']['STOP_TIME']
        }
        
        return jsonify(iss_data)
    
    except Exception as e:
        logging.error(f"Error in return_metadata route: {e}")
        return "Error retrieving metadata information from ISS data"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
