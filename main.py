# Importing all modules and classes
import os
from pprint import pprint

import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
#from openai.types.graders import label_model_grader_param

#load environment variables from the variable .env file
# had to hardcode path of variable file as argument, bcos it was showing error
load_dotenv(dotenv_path=".env.homework-2")

# Define a tool for checking weather
def check_weather(location: str) -> str:
    """Return the weather of the location using the OpenweatherMap"""
    # Get the OpenWeatherMap API key from the environment variable
    api_key = os.getenv("OPENWEATHER_API_KEY")

    # OpenWeatherMap APi endpoint
    url = "https://api.openweathermap.org/data/2.5/weather"

    try:

        # Query parameters
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric",
        }

        # Send the GET http request
        response = requests.get(url, params=params, timeout=10)

        #check if the request was successful
        if response.status_code != 200:
            return f"could not get weather for {location}. Error code: {response.status_code}"

        # parse the JSON response
        data = response.json()
        city = data["name"]
        country = data["sys"]["country"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        temp = [0, 12, 27, 35]
        todo = ""
        for tem in temp:
            if temperature < 0:
                # label = "too cold"
                # return label
                todo = (f"freezing, risk of hypothermia and frostbite with prolonged exposure"
                        f"wear a very thick clothing for the day")
            elif temperature <= 12:
                # label = "cold"
                # return label
                todo = (f"chilly, requires a coat; uncomfortable for extended outdoor activity"
                        f"wear a moderately thick clothing for the day")
            elif temperature <= 27:
                # label = "warm"
                # return label
                todo = (f"the sweet spot for most people; pleasant for everyday activity."
                        f"wear a light clothing for the day")
            elif temperature <= 35:
                # label = "hot"
                # return label
                todo = (f"sweaty and uncomfortable; stay hydrated."
                        f"wear a very light clothing for the day")
            else:
                # label = "too hot"
                # return label
                todo = (f"dangerous, especially with high humidity; risk of heat exhaustion or heatstroke."
                        f"stay in door and keep cooling system on.")


        # return the weather information as a string
        return (
            f"Current weather in {city}, {country}: "
            f"{description}, temperature {temperature}°C, "
            f"feels like {feels_like}°C, humidity {humidity}%. "
            f"{todo}"
        )
    except requests.exceptions.RequestException as e:
        return f"API Request failed: {e}"


# Define tool to get country information
def get_country_information(name):
    """Return the information of the country like Capital, currency and population"""

    url= f"https://restcountries.com/v3.1/name/{name}"
    params = {
        "fields": "name,capital,currencies,population"
    }
    try:
        response = requests.get(url, params=params, timeout=10)

        # confirming if the status of https request is successful or not.
        if response.status_code != 200:
            return f"could not get country information for {name}. Error code: {response.status_code}"
        #response.raise_for_status()

        data = response.json()

        if not isinstance(data, list) or len(data) == 0:
            return f"No data found for country {name}"

        # trying to parse the structured JSON response well
        country = data[0]
        country_name = country.get('name', {}).get('common', 'N/A')
        capital = country.get('capital', ['N/A'])[0]
        currencies = country.get('currencies', {})
        currency_names = [info.get('name') for info in currencies.values()]

        return {
            f"Country: {country_name}",
            f"Capital: {capital}",
            f"Currencies: {", ".join(currency_names)}",
            f"Population: {country.get('population', 0):,}"
        }

    except requests.exceptions.RequestException as e:
        return f"API Request failed: {e}"

print("Welcome to the Weather and Country information AI agent\n"
      "My name is Agent BOB")

running = True

while running:

    location = input("Enter your destination location: \n")

    inputs = {
        "messages": [
            {"role": "user",
             "content": f"What is the weather in {location} and provide information about {location}? add information about Country like capital, currency and population."}
        ]
    }

    # Create the agent using the OpenAI API
    graph = create_agent(
        model="openai:gpt-4.1-mini",
        tools=[check_weather,get_country_information],
        system_prompt=(
            "You are an AI weather and country information assistant. "
            "When asked about a country, you MUST call BOTH the check_weather tool "
            "AND the get_country_information tool, and include ALL results "
            "(weather, capital, currency, and population) in your final answer."
            "you MUST use the TEXT OUTPUT OF THE todo String, retaining all the text but MAKING a COMPLETE SENTENCE"
        )
    )

    # inputs = {
    #     "messages": [
    #         {"role": "user",
    #          "content": "What is the weather in Tennessee, USA and provide information on country? Also, add information about Country like capital, currency and population."}
    #    ]
    # }

    # Run the agent
    # chunk = graph.invoke(inputs)


    # Streaming helps us get the output in real-time as it's generated
    for chunk in graph.stream(inputs, stream_mode="updates"):
        # 1. Model output
        if "model" in chunk:
            messages = chunk["model"]["messages"]

            for msg in messages:
                # Tool call request
                if msg.tool_calls:
                    print("\n🤖 Agent wants to use a tool:")
                    for tool_call in msg.tool_calls:
                        print(f"Tool: {tool_call['name']}")
                        print(f"Arguments: {tool_call['args']}")

                # Final AI response
                if msg.content:
                    print("\n✅ Final Answer:")
                    print(msg.content)

                # Token usage
                if hasattr(msg, "usage_metadata") and msg.usage_metadata:
                    print("\n📊 Token Usage:")
                    pprint(msg.usage_metadata)

        # 2. Tool output
        if "tools" in chunk:
            messages = chunk["tools"]["messages"]

            for msg in messages:
                print("\n🛠️ Tool Result:")
                print(f"Tool: {msg.name}")
                print(f"Output: {msg.content}")


    print("Do you want to provide another location?")
    track = input("Enter yes or no: \n")
    if track == "no":
        print("Understood. I have safely ended our session and closed the workspace. "
        "Thank you for using asking Agent BOB. If you require further assistance in the future, "
        "please don't hesitate to log back in. Goodbye")
        running = False

