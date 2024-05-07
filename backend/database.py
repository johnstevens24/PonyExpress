import json
from datetime import date
from uuid import uuid4
from fastapi import FastAPI, Request, APIRouter, HTTPException, Depends
from backend.entities import (
    User,
    Chat,
    Message,
    UserCollection,
    ChatCollection,
    Detail
)

from sqlmodel import Session, SQLModel, create_engine, select

#1
from backend.schema import *

#2
engine = create_engine(
    "sqlite:///backend/pony_express.db",
    echo=True,
    connect_args={"check_same_thread": False},
)

#3
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#4
def get_session():
    with Session(engine) as session:
        yield session








# old stuff
# with open("backend/fake_db.json", "r") as f:
#     DB = json.load(f)

class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

# ----- users ----- #

#Updated
def get_all_users(session: Session) -> list[User]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """
    rawUsers = session.exec(select(UserInDB)).all()
    cleanedUsers = []
    for user in rawUsers:
        cleanedUsers.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at
        })
    return cleanedUsers

#Updated
def get_user_by_id(session: Session, user_id: int) -> User:
    """
    Retrieve a user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user or none if not found
    """
    user = session.exec(select(UserInDB).where(UserInDB.id == user_id)).first()
    if(user != None):
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at
        }
    return None


# ----- chats ----- #
#Updated
def get_all_chats(session: Session) -> list[Chat]:
    """
    Retrieve all chats from the database.

    :return: list of chats
    """
    chats = session.exec(select(ChatInDB)).all()
    updatedChats = []
    for chat in chats:
        owner = session.exec(select(UserInDB).where(UserInDB.id == chat.owner_id)).first()
        updatedChats.append({
            "id": chat.id,
            "name": chat.name,
            "owner": {
                "id": owner.id,
                "username": owner.username,
                "email": owner.email,
                "created_at": owner.created_at
            },
            "created_at": chat.created_at
        })
    return updatedChats

#Updated
def get_users_chats(session: Session, user_id: int) -> list[Chat]:
    """
    Retrieve all of one user's chats from the database.

    :return: list of chats sans messages
    """
    #check to see if the user exists/retrieve the user object
    user = session.exec(select(UserInDB).where(UserInDB.id == user_id)).first()
    if(user == None):
        return None
    
    chats = session.exec(select(ChatInDB).join(UserChatLinkInDB).filter(UserChatLinkInDB.user_id == user.id)).all()
    updatedChats = []
    for chat in chats:
        updatedChats.append({
            "id": chat.id,
            "name": chat.name,
            "owner": {
                "id": chat.owner.id,
                "username": chat.owner.username,
                "email": chat.owner.email,
                "created_at": chat.owner.created_at
            },
            "created_at": chat.created_at
        })
    return updatedChats

#Updated
def get_users_in_chat(session: Session, chat_id) -> list[User]:
    """
    Retrieve all of the users from a particular chat in the database.

    :return: list of users
    """
    users = session.exec(select(UserInDB).join(UserChatLinkInDB).filter(UserChatLinkInDB.chat_id == chat_id)).all()
    cleanedUsers = []
    for user in users:
        cleanedUsers.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at
        })
    return cleanedUsers

#Updated
def get_messages_in_chat(session: Session, chat_id):
    """
    Retrieve all of the messages from a particular chat in the database.

    :return: list of messages
    """
    messages = session.exec(select(MessageInDB).where(MessageInDB.chat_id == chat_id)).all()
    updatedMessages = []
    for message in messages:
        owner = session.exec(select(UserInDB).where(UserInDB.id == message.user_id)).first()
        updatedMessages.append({
            "id": message.id,
            "text": message.text,
            "chat_id": int(chat_id),
            "user": {
                "id": owner.id,
                "username": owner.username,
                "email": owner.email,
                "created_at": owner.created_at
            },
            "created_at": message.created_at
        })
    return updatedMessages
    
#Updated
def get_chat_via_id(session: Session, chat_id, params) -> Chat:
    """
    Retrieve chat from database via its chat id

    :return: chat info, messages, and users
    """
    chat = session.exec(select(ChatInDB).where(ChatInDB.id == chat_id)).first()
    owner = chat.owner

    if("users" not in params and "messages" not in params):
        return {
        "meta": {
            "message_count": len(chat.messages),
            "user_count": len(chat.users)
        },
        "chat": {
            "id": chat.id,
            "name": chat.name,
            "owner": {
                "id": owner.id,
                "username": owner.username,
                "email": owner.email,
                "created_at": owner.created_at
            },
            "created_at": chat.created_at
        }
    }

    # cleanedMessages = []
    # for message in chat.messages:
    #     # return(message.user.id)
    #     cleanedMessages.append({
    #        "id": message.id,
    #        "text": message.text,
    #        "chat_id": chat.id,
    #        "user": {
    #            "id": message.user.id,
    #            "username": message.user.username,
    #            "email": message.user.email,
    #            "created_at": message.user.created_at
    #        },
    #        "created_at": message.created_at
    #     })
    
    cleanedMessages = []
    for message in chat.messages:
        try:
            cleanedMessages.append({
                "id": message.id,
                "text": message.text,
                "chat_id": chat.id,
                "user": {
                    "id": message.user.id,
                    "username": message.user.username,
                    "email": message.user.email,
                    "created_at": message.user.created_at
                },
                "created_at": message.created_at
            })
        except AttributeError as e:
            print(e)
    #it makes no sense why this needs to be in a try catch, but this is the only way it works

    cleanedUsers = []
    for user in chat.users:
        cleanedUsers.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at
        })

    if("users" not in params and "messages" in params):
        return {
        "meta": {
            "message_count": len(chat.messages),
            "user_count": len(chat.users)
        },
        "chat": {
            "id": chat.id,
            "name": chat.name,
            "owner": {
                "id": owner.id,
                "username": owner.username,
                "email": owner.email,
                "created_at": owner.created_at
            },
            "created_at": chat.created_at
        },
        "messages": cleanedMessages
    }
    
    if("users" in params and "messages" not in params):
        return {
        "meta": {
            "message_count": len(chat.messages),
            "user_count": len(chat.users)
        },
        "chat": {
            "id": chat.id,
            "name": chat.name,
            "owner": {
                "id": owner.id,
                "username": owner.username,
                "email": owner.email,
                "created_at": owner.created_at
            },
            "created_at": chat.created_at
        },
        "users": cleanedUsers
    }

    return {
        "meta": {
            "message_count": len(chat.messages),
            "user_count": len(chat.users)
        },
        "chat": {
            "id": chat.id,
            "name": chat.name,
            "owner": {
                "id": owner.id,
                "username": owner.username,
                "email": owner.email,
                "created_at": owner.created_at
            },
            "created_at": chat.created_at
        },
        "messages": cleanedMessages,
        "users": cleanedUsers
    }

    
#Updated
def contains_chat(session: Session, chat_id) -> bool:
    """
    Checks if the chat exists in the database

    :return: True or False
    """
    if(session.exec(select(ChatInDB).where(ChatInDB.id == chat_id)).first() == None):
        return False
    return True

#Updated
def update_chat(session: Session, new_chat_name, chat_id) -> Chat:
    """
    Changes the name of a chat in the database

    :return: Chat + owner details
    """
    chat = session.exec(select(ChatInDB).where(ChatInDB.id == chat_id)).first()
    chat.name = new_chat_name
    session.commit()
    owner = session.exec(select(UserInDB).where(UserInDB.id == chat.owner_id)).first()
    return {
        "chat": {
                "id": chat.id,
                "name": chat.name,
                "owner": {
                    "id": owner.id,
                    "username": owner.username,
                    "email": owner.email,
                    "created_at": owner.created_at
                },
                "created_at": chat.created_at
            }
    }



#Updated
def add_message(session: Session, chat_id, user: UserInDB, text):
    """
    Adds a message to a chat in the database

    :return: message + stuff
    """
    chat = session.exec(select(ChatInDB).where(ChatInDB.id == chat_id)).first()
    
    if(chat == None):
        raise HTTPException(status_code=404, detail={
                "type": "entity_not_found",
                "entity_name": "Chat",
                "entity_id": chat_id
            })
    else:
        message = MessageInDB(text=text, user_id=user.id, chat_id=chat_id)
        session.add(message)
        session.commit()
        session.refresh(message)
        return {
            "message": {
                "id": message.id,
                "text": message.text,
                "chat_id": int(chat_id),
                "user":{
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "created_at": user.created_at
                },
                "created_at": message.created_at
            }
        }
    


def update_user_info(session: Session, user: UserInDB, request_body: dict):
    if(request_body.get('email') != None):
        user.email = request_body.get('email')
    if(request_body.get('username') != None):
        user.username = request_body.get('username')
    session.commit()
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at
        }
    }

#assignment 5 stuff

def edit_message(session: Session, user: UserInDB, chat_id, message_id, text):
    message = session.exec(select(MessageInDB).where(MessageInDB.id == message_id)).first()
    if(message == None):
        raise HTTPException(status_code=404, detail={
                "type": "entity_not_found",
                "entity_name": "Message",
                "entity_id": message_id
            })
    else:
        if(message.user_id != user.id):
            raise HTTPException(status_code=403, detail={
                "error": "no_permission",
                "error_description": "requires permission to edit message"
            })
        
        message.text = text
        session.commit()
        return {
            "message": {
                "id": message.id,
                "text": message.text,
                "chat_id": int(chat_id),
                "user":{
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "created_at": user.created_at
                },
                "created_at": message.created_at
            }
        }
    
def delete_message(session: Session, user: UserInDB, chat_id, message_id):
    chat = session.exec(select(ChatInDB).where(ChatInDB.id == chat_id)).first()
    if(chat == None):
        raise HTTPException(status_code=404, detail={
                "type": "entity_not_found",
                "entity_name": "Chat",
                "entity_id": chat_id
            })
    
    message = session.exec(select(MessageInDB).where(MessageInDB.id == message_id)).first()
    if(message == None):
        raise HTTPException(status_code=404, detail={
                "type": "entity_not_found",
                "entity_name": "Message",
                "entity_id": message_id
            })
   
    if(message.user_id != user.id):
        raise HTTPException(status_code=403, detail={
            "error": "no_permission",
            "error_description": "requires permission to edit message"
        })
    
    session.delete(message)
    session.commit()
    
    return 
        
def get_users_chats(session:Session, user: UserInDB):
    chats = session.exec(select(ChatInDB).join(UserChatLinkInDB).filter(UserChatLinkInDB.user_id == user.id)).all()
    refinedChats = []

    for chat in chats:
        owner = session.exec(select(UserInDB).where(UserInDB.id == chat.owner_id)).first()
        refinedChats.append({ 
                "created_at": chat.created_at,
                "id": chat.id,
                "name": chat.name,
                "owner": {
                    "created_at": owner.created_at,
                    "email": owner.email,
                    "id": owner.id,
                    "username": owner.username,
                }
            })

    return refinedChats

def user_in_chat(session:Session, user: UserInDB, chat_id):
    chat = session.exec(
        select(ChatInDB)
        .join(UserChatLinkInDB)
        .filter(UserChatLinkInDB.user_id == user.id)
        .filter(ChatInDB.id == chat_id)
    ).first()
    
    if chat:
        return True
    else:
        raise HTTPException(status_code=403, detail={
                "error": "no_permission",
                "error_description": "requires permission to view chat"
            })