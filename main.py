import asyncio
import websockets
import json
import time
import datetime
import frplib as lib

# websocket / http server configuration
WEBSOCKET_URI = "ws://127.0.0.1:5001/"
HTTP_URI = "http://127.0.0.1:5002/"

# target chat for the bot to work on
TARGETS = ["0"]

# command to pin a message
PIN_COMMANDS = ["!pin", "！pin"]
UPTIME_COMMANDS = ["!uptime", "！uptime"]
HELP_COMMANDS = ["!help", "！help"]

timeStart = 0

async def main():
    async with websockets.connect(WEBSOCKET_URI) as ws:
        while True:
            msg = await ws.recv()
            deserialisedMsg = json.loads(msg)

            # print(deserialisedMsg)

            if lib.isConnect(deserialisedMsg) == True:
                print("connected to server")

            if lib.isHeartbeat(deserialisedMsg) == True:
                print("<3beat received")

            gid = lib.getGid(deserialisedMsg)

            if gid in TARGETS:
                print("message received from target:" + str(gid))
                if lib.isMessage(deserialisedMsg):
                    if (lib.isReply(deserialisedMsg) and str(lib.getTextInMsg(deserialisedMsg)) in PIN_COMMANDS):
                        replyID = lib.getReplyID(deserialisedMsg)
                        lib.setEssenceMsg(replyID, HTTP_URI)

                    elif (str(lib.getTextInMsg(deserialisedMsg)) in UPTIME_COMMANDS):
                        timeCurrent = time.time()
                        uptime = datetime.timedelta(
                            seconds = round(timeCurrent - timeStart, None)
                        )
                        id = lib.getMessageId(deserialisedMsg)
                        lib.sendReply(f"Running for {uptime}", id, gid, HTTP_URI)
                    
                    elif (str(lib.getTextInMsg(deserialisedMsg)) in HELP_COMMANDS):
                        id = lib.getMessageId(deserialisedMsg)
                        lib.sendReply(f"FRPBot\n!uptime - 查看在线时间\n!pin - 设置精华消息", id, gid, HTTP_URI)

            else:
                print("not from target, skipping")

if __name__ == "__main__":
    timeStart = time.time()
    asyncio.run(main())
