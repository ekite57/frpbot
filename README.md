# FRPBot
a bot I wrote so everyone can pin messages in a QQ group.  
shitcode warning: if your IQ is larger than 0.1, then please don't view any code within this repo

## Usage
to pin a message, reply to it and type `!pin` or `！pin`

## Deploy
WARNING: NOT RESPONSIBLE FOR ANY BANNED ACCOUNT  

0. clone repo
1. `pip install -r requirements.txt`
2. create a websocket and a http server within napcat or whatever framework that you use
3. open `main.py` with any editor that you want
4. set `WEBSOCKET_URI` and `HTTP_URI` to the server that you created before
5. set `TARGET_GROUP` to the group you want
6. `python main.py`
7. enjoy