import argparse as ap
import satpos
import sat_orbital_plane as sop
import pickle, os

parser = ap.ArgumentParser()
parser.add_argument("satellite_id", type=int, help="Pass the satellite unique ID.", nargs='?')
parser.add_argument("-o", "--orbital_plane", dest='o', action="store_true", help="Trace satellite orbital plane around earth.")
parser.add_argument("-t", "--tracker", dest='t', action="store_true", help="Track the satellite.")
parser.add_argument("--reset", dest='r', action="store_true", help="Reset the api-key.")
args = parser.parse_args()

# first check if the api key is provided or not.
f = open("creds.dat", "rb")
try:
    while True:
        apikey = pickle.load(f)
except:
    f.close()

def set_api_key(apikey):
    f = open("temp.dat", "wb")
    pickle.dump(apikey.encode("base64"), f)
    f.close()

    os.remove("creds.dat")
    os.rename("temp.dat", "creds.dat")

if apikey == '':
    print "Since, there is no api-key, you cannot use the services. Please provide a valid api-key to move further."
    print "If you don't have an api-key, please visit https://www.n2yo.com/login/ and register with a valid email id to get an api-key."
    print """If you will not provide a valid api-key, the program will not run correctly. If you think that by mistake,
the api-key entered by you is wrong and you want to re-enter the key, then do the following.

Issue this command 'python satellite_id.py --reset'. Enter the correct key at the prompt and rectify the issue."""
    print
    print "If you have an api-key press 'c' and then press ENTER.\nPress ENTER to exit.\n"
    choice = raw_input("> ").lower()

    if choice == 'c':
        print "\nGlad to know that you have an api-key. Please enter it."
        apiKey = raw_input("Enter the api-key here exactly as given to you: ")
        
        set_api_key(apiKey)

        print "\nYour api-key has been saved. Please run the program again to enjoy the services.\nThank You!"
    else:
        print "Please get yourself an api-key by registering at https://www.n2yo.com/login/."
else:

    if args.satellite_id and not args.r:
        if args.o:
            flag = raw_input("Plot 2D or 3D orbital plane? (enter 2 or 3 respectively): ")
            if flag == '3':
                sop.sat_orbital_plane.trace_orbit(args.satellite_id)
            else:
                sop.sat_orbital_plane.trace_orbit(args.satellite_id, False)

        elif args.t:
            print "Enter 1 to get current position of satellite."
            print "Enter 2 to live track the satellite."
            print "Enter 3 to get information about satellite."
            x = input("Enter the choice: ")

            if x == 1:
                sec = input("Enter the no. of seconds to track satellite: ")
                response = satpos.satpos.current_position(args.satellite_id, seconds=sec)
            elif x == 2:
                update_interval = input("Enter the refresh interval for position update in seconds: ")
                satpos.satpos.live_track(args.satellite_id, refresh_interval=update_interval)
            elif x == 3:
                satpos.satpos.satellite_info(args.satellite_id)

    elif args.r and not args.satellite_id:
        new_key = raw_input("Enter a valid API Key: ")
        set_api_key(new_key)

        print "\nThe api-key has been reset. Run the program again to enjoy the services."

    else:
        print "Either choose to reset the api-key or enter the satellite ID."
