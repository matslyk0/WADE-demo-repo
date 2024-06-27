import os, requests, random
from openai import OpenAI
from PIL import Image
from pyowm.owm import OWM

#API Keys
owm = OWM(os.environ.get("OWM_API_KEY")) # grabbing the key from the environment variable on my system 
client = OpenAI() # the api_key argument is automatically obtained from the OPENAI_API_KEY environment variable

wthr_manager = owm.weather_manager()
geo_manager = owm.geocoding_manager()

def get_image(user_prompt):
    """
    Prompts DALL-E 3 with the user's prompt (str).
    """
    response = client.images.generate(model='dall-e-3', prompt=user_prompt, size='1024x1024', quality="standard", n=1)

    image_url = response.data[0].url

    my_img = Image.open(requests.get(image_url, stream=True).raw)

    my_img.show()

city_array = []
while len(city_array) == 0:

    cityInput = input('Please enter a city: ')
    while len(cityInput) == 0:
        cityInput = input('Nothing entered, please try again: ')
    if cityInput == "BREAK":
        break

    countryCode = input('Please enter the associated country ISO code: ')
    if countryCode.lower() == 'us':
        stateCode = input('Please enter the state code associated with the location: ')
        city_array = geo_manager.geocode(cityInput,countryCode,stateCode)

    while len(countryCode) != 2:
        countryCode = input('Please enter the associated country ISO code: ')
        
    city_array = geo_manager.geocode(cityInput,countryCode)
    if len(city_array) == 0:
        print('Sorry, no results came up. Please enter the information again.')

city = city_array[0]

one_call = wthr_manager.one_call(city.lat,city.lon)
temperature_info = one_call.current.temperature('celsius')
temperature = temperature_info['temp']
humidity = one_call.current.humidity

print("Loading...")

get_image(f"{city} with a temperature of {temperature} degrees celsius and a humidity of {humidity}")
