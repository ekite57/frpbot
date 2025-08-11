# FRPBot
a bot I wrote so everyone can pin messages in a QQ group.  
(shitcode warning)

## Usage
`!help` to show usage  
`!uptime` to show uptime  
`!pin` to pin message

## Deploy
WARNING: NOT RESPONSIBLE FOR ANY BANNED ACCOUNT  

for more information about configuring napcat, go [here](https://napneko.github.io/) for a detailed documentation  

0. clone repo
1. `pip install -r requirements.txt`
2. create a websocket server within napcat or whatever framework that you use
3. open `config.py` with your preferred text editor
4. set `websocketUri` to the server that you created before
5. set `targets` to the group(s) you want the bot to work on
6. `python main.py`
7. enjoy