import asyncio
import websockets
import json
import time
import datetime
import re

import frplib as lib
import configlib as conf

c = conf.readConfig()

wsUri = conf.getConfig(c, "websocket_uri")
httpUri = conf.getConfig(c, "http_uri")

targets = conf.getConfig(c, "targets")

pinSyntax = re.compile(conf.getConfig(c, "pin_syntax"))
uptimeSyntax = re.compile(conf.getConfig(c, "uptime_syntax"))
helpSyntax = re.compile(conf.getConfig(c, "help_syntax"))

async def main():
    async with websockets.connect(wsUri) as ws:
        while True:
            msg = await ws.recv()
            deserialisedMsg = json.loads(msg)

            # print(deserialisedMsg)

            if lib.isConnect(deserialisedMsg) == True:
                print("connected to server")

            if lib.isHeartbeat(deserialisedMsg) == True:
                print("<3beat received")

            gid = lib.getGid(deserialisedMsg)

            if gid in targets:
                print("message received from target:" + str(gid))
                if lib.isMessage(deserialisedMsg):
                    if (lib.isReply(deserialisedMsg) and pinSyntax.search(str(lib.getTextInMsg(deserialisedMsg)))):
                        replyID = lib.getReplyID(deserialisedMsg)
                        lib.setEssenceMsg(replyID, httpUri)

                    elif (uptimeSyntax.search(str(lib.getTextInMsg(deserialisedMsg)))):
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
                            endpointAddr = httpUri
                        )
                    
                    elif (helpSyntax.search(str(lib.getTextInMsg(deserialisedMsg)))):
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
                            endpointAddr = httpUri
                        )

if __name__ == "__main__":
    timeStart = time.time()
    asyncio.run(main())
