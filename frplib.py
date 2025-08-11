import websockets
import json

def getGid(message:object) -> int | None:
    if "group_id" in message:
        return message.get("group_id")
    else:
        return None
    
def isMetaEvent(message:object) -> bool:
    if (
        "post_type" in message
        and message.get("post_type") == "meta_event"
    ):
        return True
    else:
        return False

def isHeartbeat(message:object) -> bool:
    if (
        isMetaEvent(message) == True
        and "meta_event_type" in message
        and message.get("meta_event_type") == "heartbeat"
    ):
        return True
    else:
        return False
    
def isLifecycle(message:object) -> bool:
    if (
        isMetaEvent(message) == True
        and "meta_event_type" in message
        and message.get("meta_event_type") == "lifecycle"
    ):
        return True
    else:
        return False
    
def isConnect(message:object) -> bool:
    if (
        isMetaEvent(message) == True
        and isLifecycle(message) == True
        and "sub_type" in message
        and message.get("sub_type") == "connect"
    ):
        return True
    else:
        return False
    
def isMessage(message:object) -> bool:
    if "message" in message:
        return "True"
    else:
        return False
    
def getTextInMsg(message:object) -> str:
    if isMessage(message):
        msgDictList = message.get("message")

        for component in msgDictList:
            msgType = component.get("type")
            if msgType == "text":
                return str(component.get("data").get("text"))
            
def isReply(message:object) -> bool:
    if isMessage(message):
        msgDictList = message.get("message")
        for a in msgDictList:
            msgType = a.get("type")
            if msgType == "reply":
                return True
            else:
                return False

def getReplyId(message:object) -> int:
    if isMessage(message):
        msgDictList = message.get("message")

        for component in msgDictList:
            msgType = component.get("type")
            if msgType == "reply":
                return component.get("data").get("id")
            
def getMessageId(message:object) -> int:
    if isMessage(message):
        return message.get("message_id")
    
def setEssenceMsg(connection:websockets.ClientConnection, msgId:int):
    payload = {
        "action": "set_essence_msg",
        "params": {
            "message_id": msgId
        }
    }
    return connection.send(json.dumps(payload))

def sendGroupMessage(connection:websockets.ClientConnection, msgContent:object, groupId:int):
    payload = {
        "action": "send_group_msg",
        "params": {
            "group_id": groupId,
            "message": msgContent
        }
    }
    return connection.send(json.dumps(payload))

def qSendGroupReply(connection:websockets.ClientConnection, msgContent:str, replyId:int, groupId:int):
    payload = [
        {
            "type": "reply",
            "data": {
                "id": replyId
            }
        },
        {
            "type": "text",
            "data": {
                "text": str(msgContent)
            }
        }
    ]
    return sendGroupMessage(connection, payload, groupId)
