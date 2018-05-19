# Satellite Tracker 

This project aims on tracking any satellite live with an additional feature of displaying its orbital plane around the earth. The app uses n2yo.com APIs to trace the current location of the satellite and its orbital plane.

## Satellite Tracker

There are mainly two features in this domain. You can get the current location of the satellite and you can also track the satellite live with your location marked on the map in both the features.

### Current Location
To get the current location of any satellite, you just need to issue the following command.
`python satellite_tool.py [NORAD_ID] --tracker`
The next thing you will see is a prompt asking to find the current location or to live track the satellite. Enter 1 to find the current location of the satellite. Next, enter the number of seconds (which are basically the number of future positions of the satellite you want in the JSON response). As soon as you will do this, a new window in your default web browser will open, displaying the current location of the satellite and your current location as well.

### Live Tracking
Issue the same command as before but this time press 2 on the prompt. After that, another prompt will ask you to enter the refresh interval for the web page to update the satellite location. This interval, measured in seconds, is the web page refresh rate to update you with the position of the satellite. Obviously, a large number of seconds for the refresh interval will require **less** expenditure of your internet bandwidth. My experience with the program reveals that a refresh interval of 10 seconds is quite enough for a fair degree of transition in satellite position to be observed by human eye on the map. On the other hand, for 1 second of refresh time, you won't see any appreciable change for the satellite position unless you zoom in to the map.

### Few nomenclatures
Before we move on to the orbital planes, it would be a good idea to spend some time on some scientific terms involved with this program.

#### NORAD ID
Also called the satellite catalog number, the NORAD is a 5 digit number identifying any object (here satellite) orbiting the Earth. You can use n2yo.com or simply Google search for NORAD ID of any satellite.

#### Azimuth
The azimuth is the angle formed between a reference direction (in this example north) and a line from the observer to a point of interest projected on the same plane as the reference direction orthogonal to the zenith. (Source: WIKIPEDIA)

#### Elevation
The elevation of a geographic location is its height above or below a fixed reference point, most commonly a reference geoid, a mathematical model of the Earth's sea level as an equipotential gravitational surface. (Source: WIKIPEDIA)

#### Timestamp
Encoded string, specifying the time at which a certain event occured. 

### Satellite Information
To extract the above mentioned scientific terms with respect to a particular satellite, issue the same command as above and press 3 at the next prompt.

## Orbital Plane
An orbital plane is the plane of an ellipse around the Earth (or any parent body) whose boundary is traced by the satellite. This program uses the **Two Line Element** or TLE to plot the satellite orbital plane. The TLE contains the information about the azimuth, inclination of the plane and other Keplerian Elements about the satellite. To know more about Keplerian elements, a simple Google search would suffice. Wikipedia defines and explains TLE quite effectively. Knowledge of TLE and Keplerian elements is not required to run the program. However, you need to be familiar with simple terms like inclination, eccentricity, azimuth, etc to understand the orbital plane produced by the program.

### Displaying the Orbital Plane
Issue the following command to view the orbit of the satellite.
`python satellite_tool.py [NORAD_ID] -o`
On pressing enter, a prompt will ask you to display 2D or 3D orbital plane. Press 2 for 2D and 3 for 3D. The next thing that you will see would be a matplotlib window showing an animation in which a satellite will be orbiting the central body (of course, Earth). You will be able to easily observe the orientation of the orbit around the earth, the speed of the satellite while it is orbiting and the eccentricity of the ellipse.

## NOTE
This program is currently available for Linux only.

# Author
Himanshu Sharma