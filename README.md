# Moji

<div align="center">

![moji-01](https://user-images.githubusercontent.com/47546985/89359073-d029ab00-d679-11ea-833b-f00106046a2d.png)

[![made-with-discord.py](https://img.shields.io/badge/Made%20with-Discord.py-orange)](https://discordpy.readthedocs.io/en/latest/)
[![GitHub](https://img.shields.io/github/license/RyanLuong1/Moji)](https://github.com/RyanLuong1/Moji/blob/master/LICENSE)

</div>
</br>

## Table of Contents
1. [Description](https://github.com/RyanLuong1/Moji#description)
2. [Commands](https://github.com/RyanLuong1/Moji#commands)
3. [Commands Usage](https://github.com/RyanLuong1/Moji#commands-usage)
4. [Setup](https://github.com/RyanLuong1/Moji#setup)
   1. [Prerequistes for Linux](https://github.com/RyanLuong1/Moji#prerequistes-for-linux)
      1. [Installing Prerequistes](https://github.com/RyanLuong1/Moji#installing-prerequistes)
   2. [Prerequistes for Windows 10](https://github.com/RyanLuong1/Moji#prerequistes-for-windows-10)
      1. [Installing Prerequistes](https://github.com/RyanLuong1/Moji#installing-prerequistes-1)
   3. [MongoDB Setup](https://github.com/RyanLuong1/Moji#mongodb-setup)
   4. [Discord Bot Setup](https://github.com/RyanLuong1/Moji#discord-bot-setup)
   5. [Moji Setup (Linux)](https://github.com/RyanLuong1/Moji#moji-setup-linux)
      1. [Running Moji](https://github.com/RyanLuong1/Moji#running-moji)
   6. [Moji Setup (Windows 10)](https://github.com/RyanLuong1/Moji#moji-setup-windows-10)
      1. [Running Moji](https://github.com/RyanLuong1/Moji#running-moji-1)
5. [Troubleshooting (Linux)](https://github.com/RyanLuong1/Moji#troubleshooting-linux)
6. [Troubleshooting (Windows 10)](https://github.com/RyanLuong1/Moji#troubleshooting-windows-10)

## Description

Moji is a Discord bot which tracks custom emojis usage. It can track both non-animated and animated emojis from messages and reaction messages. 
<div align="center">

![moji_gif](https://user-images.githubusercontent.com/47546985/89852438-ae319c00-db43-11ea-989a-1a84f81fe15e.gif)
</div>
</br>

## Commands
Prefix: !

</br>

## Commands Usage
*   !emotes
     
     Displays all of the server emojis name and its count sorted in descending order. If there are emojis with duplicate counts, then the emojis name is used to sort it.

</br>

## Setup
Setting up the bot requires yourself to host it.

### Prerequistes for Linux
* Python 3.6 or higher
* [discord.py](https://github.com/Rapptz/discord.py)
* [pymongo](https://api.mongodb.com/python/current/installation.html)

#### Installing Prerequistes

##### Terminal
```
sudo apt-get update
sudo apt-get install python3.6
python3 -m pip install -U discord.py
python3 -m pip install pymongo
```

>First two steps are only required if you do not have python 3.6 installed

>You don't have to get python 3.6, but any version you install must be 3.6 or higher. If you get python 3.7, then it would be ```sudo apt-get install python3.7``` 

>Press enter for each command you type

### Prerequistes for Windows 10
* [Python 3.6 or higher](https://www.python.org/downloads/windows/)
* [discord.py](https://github.com/Rapptz/discord.py)
* [pymongo](https://api.mongodb.com/python/current/installation.html)
* [Git](https://git-scm.com/downloads)

#### Installing Prerequistes for Windows 10

1. Download the executable on [Python.org](https://www.python.org/downloads/)
2. Download Git on the [Git page](https://git-scm.com/downloads)

>Mark sure to tick the ```Add Python # to PATH``` box for the Python installer

>Leave everything default for the Git installer

##### Command Prompt
```
py -3 -m pip install -U discord.py
python -m pip install pymongo
```

>Press enter for each command you type

### MongoDB Setup

1. Go to [MongoDB](https://www.mongodb.com/)
2. Make an account by clicking either the ```Start Free``` or ```Try Free``` button
3. Name your organization and your project as well as selecting your preferred language **(Optional)**
4. Select shared clusters (free version).
5. Pick a cloud provider and a region closest to you. This may take a few minutes.
6. Click the ```CONNECT``` button
7. Click the ```Add Your Current IP Address``` button and click the ```Add IP Address```
8. Go to ```Create a Database User``` and create your username and your password. Remember your username and your password as you will need it for step 8.
9. Click ```Choose a connection method``` button and choose ```Connect using MongoDB Compass``` button
10. Pick your operating system and download Mongodb Compass.
11. Copy your connection string and replace ```password``` with the password you created from step 8.
12. Open Mongodb Compass and paste your connection string and connect.
13. Click the ```CREATE DATABASE``` button and name your database and collection **(Optional)**

### Discord Bot Setup
1. Go to [Discord Developer Portal](https://discord.com/developers). 
2. Login using your existing Discord account or create one if you don't have one.
3. Click the ```New Application``` button.
4. Name your ```Application``` and click ```Create```
5. On the left panel, click ```Bot``` and click the ```Add Bot``` button
6. On the left panel, click ```OAuth2```
7. Check ```bot``` under ```scopes```.
8. Under ```Bot Permissions```, check ```Manage Emojis```, ```Send Messages```, ```Manage Messages```, ```Use External Emojis```, and ```Add Reactions```.
9. Copy and paste the URL generated under ```scopes```, select your guild and click ```Authorize```. Check that your bot is in your guild. It should be offline.
10. Click ```Bot``` on the left panel and click either the ```Copy``` button or ```Click to Reveal Token``` to get your bot token.

### Moji Setup (Linux)
1. Open terminal and type ```git clone https://github.com/RyanLuong1/Moji.git```
2. Change your directory to the bot directory ```cd /Moji``` and type ```pip3 install -r requirements.txt```.
3. In the same directory, create a new file ```.env``` by typing ```touch .env``` and opening it through the terminal or through your preferred text editor. It should contain the following:
   ```
     DISCORD_TOKEN= "YOUR_DISCORD_TOKEN"
     CONNECTION_URL= "YOUR_CONNECTION_STRING"
   ```
4. Replace ```"YOUR_DISCORD_TOKEN"``` and ```"YOUR_CONNECTION_STRING"``` with their respective token and connection string
5. Open ```CommandEvents.py``` and ```EmoteCommand.py``` and replace ```emotes_db``` and ```emotes_collection``` with your respective database and collection name. **(Only do this if you gave your database and collection a name. Otherwise, a database named "emotes_db" and a collection named "emotes_collection" will be created and shown in MongoDB Compass)**

>```DISCORD_TOKEN``` is from step 10 of ```Discord Bot Setup```

>```CONNECTION_URL``` is from step 12 of ```MongoDB Setup```

>Your respective database name is from step 13 of ```MongoDB Setup```

>Your respective collection name is from step 13 of ```MongoDB Setup```

#### Running Moji
1. Go to the bot directory and type ```python3 emojibot.py```. Now your emojis are loaded to the database and ready for its count to be collected by Moji as long as it is online.


### Moji Setup (Windows 10)
1. Open command prompt and type ```cd Downloads```
2. Type ```git clone https://github.com/RyanLuong1/Moji.git``` 
3. Type ```cd Moji``` and type ```pip install -r requirements.txt```
4. In the same directory, create a new file ```.env``` by typing ```type nul > .env``` and opening through the command prompt or through your preferred text editor. It should contain the following:
    ```
      DISCORD_TOKEN = "YOUR_DISCORD_TOKEN"
      CONNECTION_URL = "YOUR_CONNECTION_STRING"
    ```
5. Replace your ```"YOUR_DISCORD_TOKEN"``` and ```"YOUR_CONNECTION_STRING"``` with their respective token and connection string.
6. Open ```CommandEvents.py``` and ```EmoteCommand.py``` and replace ```emotes_db``` and ```emotes_collection``` with your respective database and collection name. **(Only do this if you gave your database and collection a name. Otherwise, a database named "emotes_db" and a collection named "emotes_collection" will be created and shown in MongoDB Compass)**
</br>

>```DISCORD_TOKEN``` is from step 10 of ```Discord Bot Setup```

>```CONNECTION_URL``` is from step 12 of ```MongoDB Setup```

>Your respective database name is from step 13 of ```MongoDB Setup```

>Your respective collection name is from step 13 of ```MongoDB Setup```

#### Running Moji
1. Go to the bot directory and type ```python emojibot.py```. Now your emojis are loaded to the database and ready for its count to be collected by Moji as long as it is online.

## Troubleshooting (Linux)

```TypeError: __new__() got an unexpected keyword argument 'deny_new'```

[Solution](https://stackoverflow.com/questions/63027848/discord-py-glitch-or-random-error-typeerror-new-got-an-unexpected-keywor). Discord most likely have updated discord.py. Type ```python3 -m pip install -U discord.py```

```TypeError: __init__() got an unexpected keyword argument 'requote'```

[Solution](https://github.com/Rapptz/discord.py/issues/5162). Read Rapptz's response. Type ```pip3 install -U yarl==1.4.2```

## Troubleshooting (Windows 10)

```the dns response does not contain an answer to the question```

[Solution](https://stackoverflow.com/questions/52930341/pymongo-mongodbsrv-dnspython-must-be-installed-error). Type ```pip install pymongo[srv]```
