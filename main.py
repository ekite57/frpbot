import asyncio
import websockets
import json
import frplib as lib

# websocket / http server configuration
WEBSOCKET_URI = "ws://127.0.0.1:5001/"
HTTP_URI = "http://127.0.0.1:5002/"

# target chat for the bot to work on
TARGET = 0

# command to pin a message
PIN_COMMANDS = ["!pin", "！pin"]

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

            if gid == TARGET:
                print("message received from target:" + str(gid))
                if lib.isMessage(deserialisedMsg):
                    if (
                        lib.isReply(deserialisedMsg)
                        and str(lib.getTextInMsg(deserialisedMsg)) in PIN_COMMANDS
                    ):
                        replyID = lib.getReplyID(deserialisedMsg)
                        lib.setEssenceMsg(replyID, HTTP_URI)
            else:
                print("not from target, skipping")

if __name__ == "main":
    asyncio.run(main())
