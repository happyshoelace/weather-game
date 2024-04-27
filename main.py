import requests
import pprint
import os
from dotenv import load_dotenv
import random
import json

load_dotenv()
TOKEN = os.getenv('WEATHER_TOKEN')

play = True
playablePlaces = {}
f = open("capitalList.txt","r",encoding="utf-8")
for line in f:
    line = line.strip()
    currentCity = line.split(",")
    playablePlaces[currentCity[1]] = currentCity[0]
capitals = list(playablePlaces.keys())

def initalisePlayers():
    player = input("Enter the first player: ")
    playerList = {}
    while player:
        playerList[player] = random.randint(0,25)
        player = input("Enter the next player: ")
    return playerList

def getLocation(chosencity):
    payload = {"q":chosenCity, "limit":1, "appid":TOKEN}
    r = requests.get("http://api.openweathermap.org/geo/1.0/direct", params=payload)
    response = r.json()
    locationValues= []
    locationValues.append(response[0]['lat'])
    locationValues.append(response[0]['lon'])
    return locationValues

def getWeather(locationValues):
    lat = locationValues[0]
    lon = locationValues[1]
    payload = {"lat":lat, "lon":lon, "appid":TOKEN, "units":"metric"}
    r = requests.get("https://api.openweathermap.org/data/2.5/weather",params=payload)
    response = r.json()
    temp = response['main']['temp']
    return temp

playerList = initalisePlayers()
chosenCity = capitals[random.randint(0,len(capitals)-1)]
print(f"CHOSEN CITY: {chosenCity}, {playablePlaces[chosenCity]}")

playerGuesses = {}
previousGuesses = []
guessedPlayers = list(playerList.keys())
i = 0
while i < len(playerList):
    playerNumber = random.randint(0, (len(guessedPlayers)-1))
    guess = float(input(f"{guessedPlayers[playerNumber]}, you're up! What do you think the current temperature is in {chosenCity}, {playablePlaces[chosenCity]}? "))
    validGuess = True
    if guess in previousGuesses:
        validGuess = False
    while validGuess == False:
        print(f"Oops, {playerGuesses[guess]} already guessed {guess}. Let's try a different guess!")
        guess = float(input(f"What do you think the current temperature is in {chosenCity}, {playablePlaces[chosenCity]}? "))
        if guess not in previousGuesses:
            validGuess = True
    playerGuesses[guessedPlayers[playerNumber]] = guess
    guessedPlayers.pop(playerNumber)
    i += 1

print("Everyone has guessed! Here's a rundown of what everyone guessed!")
for player in playerGuesses:
    print(f"{player}: {playerGuesses[player]}")

locationValues = getLocation(chosenCity)

temp = float(getWeather(locationValues))
temp = round(temp)
print(f"It's {temp}° (celcius) in {chosenCity}, {playablePlaces[chosenCity]}!")
for player in playerList:
    playerGuess = playerGuesses[player]
    distanceFromCorrectAnswer = abs(temp - playerGuess)
    if distanceFromCorrectAnswer == 0:
        playerList[player] = playerList[playerList] + 10
    elif distanceFromCorrectAnswer < 5:
        playerList[player] = playerList[playerList] + 5
    elif distanceFromCorrectAnswer < 10:
        playerList[player] = playerList[playerList] + 2


# TO DO: Find a way to sort a dictionary
# placedPlayers = []
# i = 0
# for player in playerList:
#     topPlayer = 
#     i = 1
#     while i < len(playerList)-1:
#         currentTopValue = playerList[topPlayer]
#         if currentTopValue > playerList[i] and i not in placedPlayers:
#             print(f"new top: {i}")
#         i+= 1
#     placedPlayers.append(i)
        