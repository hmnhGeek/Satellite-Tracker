import json, requests, os, pickle
from selenium import webdriver
import folium
import time
import webbrowser

FILE_LOC = os.path.abspath(os.path.dirname(__file__))
base_url = "https://www.n2yo.com/rest/v1/satellite/positions/"

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
    
def get_satellite_position(ID, obs_lat, obs_lng, obs_alt, seconds):

    # build the url for getting the position of the satellite.
    url = base_url+"{}/{}/{}/{}/{}&apiKey={}".format(ID, obs_lat, obs_lng, obs_alt, seconds, load_api_key())

    # POST a request by sending this url to n2yo.
    r = requests.get(url)

    # retrieve the JSON data.
    data = r.json()
    return data

def plot_coords_on_map(locations, saveloc):
    mapit = folium.Map(prefer_canvas=True)
    
    for coords in locations:
        latitude, longitude, popup = coords[0], coords[1], coords[2]
        folium.CircleMarker(location=[latitude, longitude], popup=popup\
                            , radius=2).add_to(mapit)

    mapit.save(saveloc)

def track_satellite(ID, obs_alt=0, seconds=1000):
    # find observer's location first.
    r = requests.get('http://freegeoip.net/json')
    obs_lat, obs_lng = json.loads(r.text)['latitude'], json.loads(r.text)['longitude']
    
    satellite_data = get_satellite_position(ID, obs_lat, obs_lng, obs_alt, seconds)
    locations = [(obs_lat, obs_lng, "Observer")]

    # find the name of the satellite.
    satname = satellite_data['info']['satname']

    # retrieve each second, a point that tells the location of satellite on map.
    satpos_data = satellite_data['positions']

    # now iterate in each second and find the latitude and longitude of the satellite.
    for second in satpos_data:
        locations.append((second['satlatitude'], second['satlongitude'], "Satellite: "+satname))

    # generate satpos.html in the satpos module only and not where the command line tool is present.
    plot_coords_on_map(locations, os.path.join(os.path.dirname(__file__), "satpos.html"))
    return os.path.join(os.path.dirname(__file__), "satpos.html")

def current_position(ID, obs_alt=0, seconds=1000):
    updated_satpos = track_satellite(ID, obs_alt, seconds)
    return webbrowser.open("file://"+updated_satpos)
    
def live_track(ID, refresh_interval=1, obs_alt=0):
    # load the chrome-driver first
    chromedriver = os.path.join(os.path.join(FILE_LOC, ".."), "chromedriver")
    driver = webdriver.Chrome(chromedriver)
    driver.get("file://"+track_satellite(ID, obs_alt, 1))
    try:
        while 1:
            time.sleep(refresh_interval)
            track_satellite(ID, obs_alt, 1)
            driver.refresh()
    except:
        return "Abort!"
    
