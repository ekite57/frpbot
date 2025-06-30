import asyncio
import websockets
import json
import time
import datetime
import re

import frplib as lib

# websocket / http server configuration
WEBSOCKET_URI = "ws://127.0.0.1:5001/"
HTTP_URI = "http://127.0.0.1:5002/"

# target chat for the bot to work on
TARGETS = [0]

# command syntaxes
PIN_SYNTAX = re.compile("(!|！)pin$")
UPTIME_SYNTAX = re.compile("^(!|！)uptime$")
HELP_SYNTAX = re.compile("^(!|！)help$")

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
                    if (lib.isReply(deserialisedMsg) and PIN_SYNTAX.search(str(lib.getTextInMsg(deserialisedMsg)))):
                        replyID = lib.getReplyID(deserialisedMsg)
                        lib.setEssenceMsg(replyID, HTTP_URI)

                    elif (UPTIME_SYNTAX.search(str(lib.getTextInMsg(deserialisedMsg)))):
                        timeCurrent = time.time()
                        uptime = datetime.timedelta(
                            seconds = round(timeCurrent - timeStart, None)
                        )
                        msgId = lib.getMessageId(deserialisedMsg)
                        lib.sendMessage(
                            msgContent = [
                                {
                                    "type": "reply",
                                    "data":
                                    {
                                        "id": msgId
                                    }
                                },
                                {
                                    "type": "text",
                                    "data":
                                    {
                                        "text": f"Running for {uptime}"
                                    }
                                }
                            ],
                            groupId = gid,
                            endpointAddr = HTTP_URI
                        )
                    
                    elif (HELP_SYNTAX.search(str(lib.getTextInMsg(deserialisedMsg)))):
                        msgId = lib.getMessageId(deserialisedMsg)
                        lib.sendMessage(
                            msgContent = [
                                {
                                    "type": "reply",
                                    "data":
                                    {
                                        "id": msgId
                                    }
                                },
                                {
                                    "type": "text",
                                    "data":
                                    {
                                        "text": f"FRPBot\n!uptime - 查看在线时间\n!pin - 设置精华消息"
                                    }
                                }
                            ],
                            groupId = gid,
                            endpointAddr = HTTP_URI
                        )

if __name__ == "__main__":
    timeStart = time.time()
    asyncio.run(main())
