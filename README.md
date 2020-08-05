# Moji

<div align="center">

![moji-01](https://user-images.githubusercontent.com/47546985/89359073-d029ab00-d679-11ea-833b-f00106046a2d.png)
</div>

## Description
---
Moji is a Discord bot which tracks custom emojis usage. It can track both non-animated and animated emojis from messages and reaction messages. 
<div align="center">

![moji_gif](https://user-images.githubusercontent.com/47546985/89358895-5db8cb00-d679-11ea-9524-77b558852a5a.gif)
</div>
<br/>

## To-do List
- [ ] Load in the server emojis to the database when it loads instead of calling !emotes for the first time
- [ ] Update the database whenever an emoji is added or remove
- [ ] Change the emoji name in the database when the name change as long as the emoji id is the same  

## Commands
Prefix: !


## Commands Usage
*   !emotes
     
     Displays all of the server emojis name and its count sorted in descending order. If there are emojis with duplicate counts, then the emojis name is used to sort it.
---
## Setup
Setting up the bot requires yourself to host it.

### Prerequistes
* Python 3.6 or higher
* [discord.py](https://github.com/Rapptz/discord.py)
* [pymongo](https://api.mongodb.com/python/current/installation.html)

For pymongo, use ```python3 -m pip install pymongo``` or ```pip3 install pymongo```

### MongoDB Setup

1. Go to [MongoDB](https://www.mongodb.com/)
2. Make an account by clicking either the ```Start Free``` or ```Try Free``` button
3. Name your organization and your project as well as selecting your preferred language **(Optional)**
4. Select shared clusters (free version).
5. Pick a cloud provider and a region closest to you. This may take a few minutes.
6. Click the ```CONNECT``` button
7. Click the ```Add Your Current IP Address``` button and click the ```Add IP Address```
8. Go to ```Create a Database User``` and create your username and your password. Remember your username and your password as you will need it for later steps.
9. Click ```Choose a connection method``` button and choose ```Connect using MongoDB Compass``` button
10. Pick your operating system and download Mongodb Compass.
11. Copy your connection string and replace <password> with the password you created from step 8.
12. Open Mongodb Compass and paste your connection string and connect.
13. Click the ```CREATE DATABASE``` button and name your database and collection. Remember the database and collection name as you will need it for later steps.

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
     CONNECTION_URL= "YOUR_CONNECTION_STRING
   ```
4. Replace ```"YOUR_DISCORD_TOKEN"``` and ```"YOUR_CONNECTION_STRING"``` with their respective token and connection string
5. Open ```CommandEvents.py``` and ```EmoteCommand.py``` and replace ```YOUR_DATABASE_NAME``` and ```YOUR_COLLECTION_NAME``` with your respective database and collection name.

>```DISCORD_TOKEN``` is from step 10 of ```Discord Bot Setup```

>```CONNECTION_URL``` is from step 12 of ```MongoDB Setup```

>```YOUR_DATABASE_NAME``` is from step 13 of ```MongoDB Setup```

>```YOUR_COLLECTION_NAME``` is from step 13 of ```MongoDB Setup```

#### Running Moji
1. Go to the bot directory and type ```python3 emojibot.py```

## Troubleshooting

```TypeError: __new__() got an unexpected keyword argument 'deny_new'```

[Solution](https://stackoverflow.com/questions/63027848/discord-py-glitch-or-random-error-typeerror-new-got-an-unexpected-keywor). Discord most likely have updated discord.py. Type ```python3 -m pip install -U discord.py```

```TypeError: __init__() got an unexpected keyword argument 'requote'```

[Solution](https://github.com/Rapptz/discord.py/issues/5162). Read Rapptz's response. Type ```pip3 install -U yarl==1.4.2```
