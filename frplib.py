import json
import requests
import re

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
            
def getMessageId(msg):
    if isMessage(msg):
        return msg.get("message_id")
            
def setEssenceMsg(msgId:int, endpointAddr:str):
    """
    Set essence message.
    """

    addr = endpointAddr + "set_essence_msg"
    payload = json.dumps(
        {
            "message_id": msgId
        }
    )
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post(
        url = addr,
        data = payload,
        headers = headers
    )
    return r

def sendMessage(msgContent:object, groupId:int, endpointAddr:str):
    addr = endpointAddr + "send_group_msg"
    payload = json.dumps(
        {
            "group_id": groupId,
            "message": msgContent
        }
    )

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post(
        url = addr,
        data = payload,
        headers = headers
    )

    return r

if __name__ == "__main__":
    print("you are not supposed to run this - run main.py instead")
