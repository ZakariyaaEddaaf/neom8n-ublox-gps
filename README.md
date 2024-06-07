# neom8n-ublox-gps
```
$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47
```
## GPGGA Sentence
+ $GPGGA: Indicates that this is a GPS fix data sentence.
+ 123519: Time of the fix, 12:35:19 UTC.
+ 4807.038, N: Latitude 48 degrees 7.038 minutes North.
+ 01131.000, E: Longitude 11 degrees 31.000 minutes East.
+ 1: Fix quality (0 = invalid, 1 = GPS fix, 2 = DGPS fix).
+ 08: Number of satellites being tracked.
+ 0.9: Horizontal dilution of precision.
+ 545.4, M: Altitude, 545.4 meters above mean sea level.
+ 46.9, M: Height of geoid (mean sea level) above WGS84 ellipsoid.
+ (empty field): Time in seconds since last DGPS update.
+ (empty field): DGPS station ID number.
+ *47: Checksum for error checking.
## Data Field
+ Time Stamp: Provided in UTC (Coordinated Universal Time).
+ Latitude and Longitude: Given in degrees and minutes (sometimes also in decimal degrees).
+ Fix Quality: Indicates the type of fix, which could be none, GPS, DGPS (Differential GPS), etc.
+ Number of Satellites: Shows how many satellites the device is communicating with, which affects the accuracy.
+ HDOP (Horizontal Dilution of Precision): A measure of the geometrical quality of satellite configuration during the fix.
+ Altitude: Height of the device above sea level.
+ Geoidal Separation: The difference between the earth ellipsoid model used by GPS and the mean sea level.