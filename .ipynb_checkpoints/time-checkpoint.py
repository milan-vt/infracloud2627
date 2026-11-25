import datetime
now = datetime.datetime.now()
print(now)

from geopy.geocoders import Nominatin
import folium

geolocator = Nominatim(user_agent="http://biasc.be")
#### enter city and country
city_county = "Leuven, Belgium"
####
location = geolocator.geocode(city_county)
print(location.address)
devnet_lat = location.latitude
devnet_lon = location.longitude
print((devnet_lat, devnet_lon))
#
coordinats = [devnet_lat, devnet_lon]
map = folium.Map(location=coordinats, tiles='OpenStreetMap', zoom_start=12)
#map
#save method of map object will create a map
#saved in downloads
map.save("geopy_location.html")
map



if_dict = {}
print(type(if_dict))
print(id_dict)
if_json = json.dumps(if_dict, indent=2)
print(if_json)
print(type(if_dict))