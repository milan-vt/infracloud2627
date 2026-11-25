from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="http://biasc.be")
#### enter city and country
city_county = "Brussel, Belgium"

location = geolocator.geocode(city_county)
print(location.address)
devnet_lat = location.latitude
devnet_lon = location.longitude
print((devnet_lat, devnet_lon))
