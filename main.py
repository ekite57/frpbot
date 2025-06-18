import asyncio
import websockets
import json
import requests

# websocket / http server configuration
WEBSOCKET_URI = "ws://127.0.0.1:5001/"
HTTP_URI = "http://127.0.0.1:5002/"

# target chat for the bot to work on
TARGET = 0


def getGid(msg):
    if "group_id" in msg:
        return msg.get("group_id")


def isMetaEvent(msg):
    if "post_type" in msg and msg.get("post_type") == "meta_event":
        return True
    else:
        return False


def isHeartbeat(msg):
    if (
        isMetaEvent(msg) == True
        and "meta_event_type" in msg
        and msg.get("meta_event_type") == "heartbeat"
    ):
        return True
    else:
        return False


def isLifecycle(msg):
    if (
        isMetaEvent(msg) == True
        and "meta_event_type" in msg
        and msg.get("meta_event_type") == "lifecycle"
    ):
        return True
    else:
        return False


def isConnect(msg):
    if (
        isMetaEvent(msg) == True
        and isLifecycle(msg) == True
        and "sub_type" in msg
        and msg.get("sub_type") == "connect"
    ):
        return True
    else:
        return False


def isMessage(msg):
    if "message" in msg:
        return True
    else:
        return False


def getTextInMsg(msg):
    if isMessage(msg):
        msgDictList = msg.get("message")
        for a in msgDictList:
            msgType = a.get("type")
            if msgType == "text":
                return a.get("data").get("text")


def isReply(msg):
    if isMessage(msg):
        msgDictList = msg.get("message")
        for a in msgDictList:
            msgType = a.get("type")
            if msgType == "reply":
                return True


def getReplyID(msg):
    if isMessage(msg) and isReply(msg):
        msgDictList = msg.get("message")
        for a in msgDictList:
            msgType = a.get("type")
            if msgType == "reply":
                return a.get("data").get("id")


async def main():
    async with websockets.connect(WEBSOCKET_URI) as ws:
        while True:
            msg = await ws.recv()
            deserialisedMsg = json.loads(msg)

            # print(deserialisedMsg)

            if isConnect(deserialisedMsg) == True:
                print("connected to server")

            if isHeartbeat(deserialisedMsg) == True:
                print("<3beat received")

            gid = getGid(deserialisedMsg)

            if gid == TARGET:
                print("message received from target:" + str(gid))
                if isMessage(deserialisedMsg):
                    if (
                        isReply(deserialisedMsg)
                        and getTextInMsg(deserialisedMsg) == "!pin"
                        or getTextInMsg(deserialisedMsg) == "！pin"
                    ):
                        replyID = getReplyID(deserialisedMsg)
                        endpointAddr = HTTP_URI + "set_essence_msg"

                        payload = json.dumps({"message_id": replyID})
                        headers = {"Content-Type": "application/json"}
                        requests.post(url=endpointAddr, data=payload, headers=headers)

            else:
                print("not from target, skipping")


asyncio.run(main())
