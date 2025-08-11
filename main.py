import asyncio
import websockets
import json
import re
import time
import datetime

import config as conf
import frplib as frplib

async def main():
    async with websockets.connect(conf.websocketUri) as ws:
        while True:
            msgJson = await ws.recv()
            msg = json.loads(msgJson)

            if frplib.isConnect(msg):
                print("✅ WebSocket connected")

            gid = frplib.getGid(msg)
            msgId = frplib.getMessageId(msg)

            if gid in conf.targets:
                print(f"♿ received message from {gid}")
            
                if frplib.isMessage(msg):
                    text = frplib.getTextInMsg(msg)

                    try:
                        if (
                            re.search("(!|！)([Pp]|[Pp][Ii][Nn])$", text)
                            and frplib.isReply(msg)
                        ):
                            replyId = frplib.getReplyId(msg)
                            await frplib.setEssenceMsg(ws, replyId)

                        elif (
                            re.search("^(!|！)([Uu][Pp]|[Uu][Pp][Tt][Ii][Mm][Ee])$", text)
                        ):
                            timeCurrent = time.time()
                            uptime = datetime.timedelta(
                                seconds = round(timeCurrent - timeStart, None)
                            )
                            await frplib.qSendGroupReply(ws, f"Running for {uptime}", msgId, gid)

                        elif (
                            re.search("^(!|！)[Hh][Ee][Ll][Pp]$", text)
                        ):
                            await frplib.qSendGroupReply(
                                connection = ws,
                                msgContent = f"FRPBot\n\n!uptime\n查看在线时间\n!pin\n设置精华消息",
                                replyId = msgId,
                                groupId = gid
                            )
                    
                    except Exception as e:
                        print(f"🆖 Error: {e}")

if __name__ == "__main__":
    timeStart = time.time()
    asyncio.run(main())
