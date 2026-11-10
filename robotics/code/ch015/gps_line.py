# gps_line.py - read one line of text from a GPS receiver (an NMEA "GGA" sentence)
line = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47\n"

fields = line.strip().split(",")   # cut at every comma; fields[0] is the first piece

time_text = fields[1]              # "123519" means 12:35:19
clock = f"{time_text[:2]}:{time_text[2:4]}:{time_text[4:]}"

lat_text = fields[2]               # "4807.038" means 48 degrees and 7.038 minutes
lat_deg = int(lat_text[:2]) + float(lat_text[2:]) / 60   # 60 minutes = 1 degree

lon_text = fields[4]               # "01131.000" means 11 degrees and 31.000 minutes
lon_deg = int(lon_text[:3]) + float(lon_text[3:]) / 60   # longitude has 3 degree digits

satellites = int(fields[7])        # "08" becomes the whole number 8
altitude_m = float(fields[9])      # height above sea level, in metres

print("time (UTC):", clock)
print(f"latitude:   {lat_deg:.5f} degrees {fields[3]}")
print(f"longitude:  {lon_deg:.5f} degrees {fields[5]}")
print(f"satellites: {satellites}")
print(f"altitude:   {altitude_m:.1f} m")
