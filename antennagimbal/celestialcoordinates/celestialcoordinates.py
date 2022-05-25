from skyfield.api import N, W, wgs84, load

#time
ts = load.timescale()
t = ts.now()

#load earth data
planets = load('de421.bsp')
earth = planets['earth']

#load NOAA-19 satellite
stations_url = 'http://celestrak.com/NORAD/elements/active.txt'
satellites = load.tle_file(stations_url)
by_name = {sat.name: sat for sat in satellites}
satellite = by_name['NOAA 19']

print('NOAA-19',satellite)
print('Earth',earth)

#find current satellite position
ts = load.timescale()
t = ts.now()
geocentric = satellite.at(t)
print('Satellite current position:',geocentric.position.km)

#find alt and az from current home location
home = wgs84.latlon(40.005451 * N, -105.254093 * W)
home = earth + home
astrometric = home.at(t).observe(earth + satellite)
alt, az, d = astrometric.apparent().altaz()

print('Altitude',alt)
print('Azimuth',az)

#lat lon of satellite
lat, lon = wgs84.latlon_of(geocentric)
print('Latitude:', lat)
print('Longitude:', lon)

#range rate (doppler shift of radio)
#t = ts.utc(2014, 1, 23, 11, range(17, 23)) time at which satellite reaches minimum
#pos = (satellite - home).at(t)
#_, _, the_range, _, _, range_rate = pos.frame_latlon_and_rates(home)

#from numpy import array2string
#print(array2string(the_range.km, precision=1), 'km')
#print(array2string(range_rate.km_per_s, precision=2), 'km/s')

#when satellite is blocvked by Earth

p = (home).at(t).observe(earth + satellite).apparent()
behind_earth = p.is_behind_earth()
print('Is the satellite visible?:',not behind_earth)

while True:
    ts = load.timescale()
    t = ts.now()
    geocentric = satellite.at(t)
    print('Satellite current position:',geocentric.position.km)
    p = (home).at(t).observe(earth + satellite).apparent()
    behind_earth = p.is_behind_earth()
    #print('Is the satellite visible?:',not behind_earth)