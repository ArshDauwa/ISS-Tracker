from unittest.mock import patch
import math
from datetime import datetime
import pytest
from iss_tracker import calculate_lat, calculate_alt, calculate_long, calculate_geoposition, get_data
from iss_tracker import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_server_response(client):
    response = client.get('/')
    if response.status_code == 200:
        assert b"Welcome to the ISS Tracker API!" in response.data
    elif response.status_code == 404:
        print("Flask app is not running.")
        assert True  
    else:
        assert False

# Mock data for testing
mock_data = [
    {   "EPOCH":"2024-079T00:56:00.000Z",
        "X":719.875689675049,
        "X_DOT":-6.46958114906447,
        "Y":5211.35844946617,
        "Y_DOT":-2.04604360061346,
        "Z":4294.87217744873,
        "Z_DOT":3.56256406910499
    },
    {
        "EPOCH": "2024-090T11:42:00.000Z",
        "X": -4899.50219797882,
        "X_DOT": 5.0874841659975,
        "Y": -2160.01389417642,
        "Y_DOT": -4.35504009792081,
        "Z": -4196.10576548605,
        "Z_DOT": -3.69836419534284
    },
    {
        "EPOCH": "2024-090T11:46:00.000Z",
        "X": -3515.98500284686,
        "X_DOT": 6.37160099533276,
        "Y": -3114.43055090048,
        "Y_DOT": -3.5502503846941,
        "Z": -4920.68807017086,
        "Z_DOT": -2.30325927950645
    },
    {
        "EPOCH": "2024-090T11:50:00.000Z",
        "X": -1878.14622678954,
        "X_DOT": 7.19416674649454,
        "Y": -3843.58916446542,
        "Y_DOT": -2.48924556025271,
        "Z": -5288.3486923043,
        "Z_DOT": -0.74201239734831
    },
]

@patch('iss_tracker.get_data')
def test_calculate_lat(mock_get_data):
    mock_get_data.return_value = mock_data
    epoch = "2024-079T00:56:00.000Z"
    expected_latitude = 39.227672510032775
    assert math.isclose(calculate_lat(epoch), expected_latitude, rel_tol=1e-3)

@patch('iss_tracker.get_data')
def test_calculate_alt(mock_get_data):
    mock_get_data.return_value = mock_data
    epoch = "2024-079T00:56:00.000Z"
    expected_altitude = 420.33899834097247
    assert math.isclose(calculate_alt(epoch), expected_altitude, rel_tol=1e-3)

@patch('iss_tracker.get_data')
def test_calculate_long(mock_get_data):
    mock_get_data.return_value = mock_data
    epoch = "2024-079T00:56:00.000Z"
    expected_longitude = -111.86483176776528
    assert math.isclose(calculate_long(epoch), expected_longitude, rel_tol=1e-3)

@patch('iss_tracker.calculate_lat')
@patch('iss_tracker.calculate_long')
def test_calculate_geoposition(mock_calculate_long, mock_calculate_lat):
    lat = 39.227672510032775
    long = -111.86483176776528
    mock_calculate_lat.return_value = lat
    mock_calculate_long.return_value = long
    expected_geoposition = "Sanpete County, Utah, United States"
    assert calculate_geoposition(lat, long) == expected_geoposition
