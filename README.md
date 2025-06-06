# FRPBot
a bot I wrote so everyone can pin messages in a QQ group.  
(shitcode warning)

## Usage
to pin a message, reply to it and type `!pin` or `！pin`

## Deploy
WARNING: NOT RESPONSIBLE FOR ANY BANNED ACCOUNT  

for more information about configuring napcat, go [here](https://napneko.github.io/) for a detailed documentation  

0. clone repo
1. `pip install -r requirements.txt`
2. create a websocket and a http server within napcat or whatever framework that you use
3. open `main.py` with your preferred text editor
4. set `WEBSOCKET_URI` and `HTTP_URI` to the server that you created before
5. set `TARGET_GROUP` to the group you want
6. `python main.py`
7. enjoy