from geopy.geocoders import Nominatim
import folium

geolocator = Nominatim(user_agent="http://biasc.be")
#### enter city and country
city_county = "Dilbeek, Belgium"
####
location = geolocator.geocode(city_county)
print(location.address)
devnet_lat = location.latitude
devnet_lon = location.longitude
print((devnet_lat, devnet_lon))
#
coordinats = [devnet_lat, devnet_lon]
map = folium.Map(location=coordinats, tiles='OpenStreetMap', zoom_start=13)
#map
#save method of map object will create a map
#saved in downloads
map.save("geopy_location.html")
map