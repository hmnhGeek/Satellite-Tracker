import json, requests, os, pickle
from orbital import KeplerianElements, earth, plot, plot3d
from matplotlib import pyplot as plt
from numpy import radians
from orbital import earth_sidereal_day

FILE_LOC = os.path.abspath(os.path.dirname(__file__))
base_url = "https://www.n2yo.com/rest/v1/satellite/tle/"

def load_api_key():
    """
        Returns the api-key by decoding from base64 stored key.
    """
    
    # get the api-key file address encoded in base64.
    key_file = os.path.join(os.path.join(FILE_LOC, ".."), "creds.dat")

    # load the base64 key.
    f = open(key_file, "rb")
    try:
        while True:
            base64Key = pickle.load(f)
    except:
        pass
    f.close()

    # return the decoded key.
    return base64Key.decode("base64")
    
def get_satellite_TLE(ID):
    """
        Returns the two-line-element of a satellite.
    """

    # build the url for getting the position of the satellite.
    url = base_url+"{}&apiKey={}".format(ID, load_api_key())

    # POST a request by sending this url to n2yo.
    r = requests.get(url)

    # retrieve the JSON data.
    data = r.json()
    return data

def rectify_tle(geometry_data):
    """
        Returns rectified geometry list, deletes the empty elements.
    """
    correct_data = []

    for data in geometry_data:
        if data != '':
            correct_data.append(data)

    return correct_data

def extract_geometry(tle_data):
    """
        The line 2 contains inclination, eccentricity, satellite no. and perigee.
    """
    tle = tle_data['tle']
    second_line = tle.split('\n')

    data = second_line[1].split(' ')
    data = rectify_tle(data)

    directory = {
            'satellite_number':data[1],
            'inclination':data[2],
            'eccentricity':data[4],
            'perigee':data[5]
        }
    return directory

def trace_orbit(satellite_ID, plt3d=True):
    TLE_DATA = get_satellite_TLE(satellite_ID)
    geometry = extract_geometry(TLE_DATA)

    satellite_name = TLE_DATA['info']['satname']

    e = float("0."+geometry['eccentricity'])
    i = radians(float(geometry['inclination']))
    arg_pe = radians(float(geometry['perigee']))

    # define an orbit using orbital module.
    orbit = KeplerianElements.with_period(earth_sidereal_day/2, e=e, i=i, arg_pe=arg_pe, body=earth)
    
    if plt3d:
        p=plot3d(orbit, title="Orbit of {}".format(satellite_name), animate=True)
    else:
        p=plot(orbit, title="Orbit of {}".format(satellite_name), animate=True)

    try:
        plt.show()
    except:
        return "Abort!"
    
