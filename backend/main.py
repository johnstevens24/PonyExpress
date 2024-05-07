import datetime
import json
from fastapi import FastAPI, Request, APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.database import create_db_and_tables
from sqlmodel import Session

# from backend.routers.animals import animals_router
# from backend.routers.users import users_router
# from backend.database import EntityNotFoundException
from backend import database as DB
from backend.auth import auth_router, get_current_user
from backend.entities import (
    User,
    Chat,
    UserCollection,
    ChatCollection,
    MessageCollection,
    Detail
)
from backend.schema import *
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Pony Express API",
    description="API for messaging people.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # change this as appropriate for your setup
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#### Users ####


# DONE
@app.get('/users', tags=["Users"], status_code=200, description="This route gets all users from the database")
def get_users(session: Session = Depends(DB.get_session)):
    users = DB.get_all_users(session)
    return {
        "meta":{"count": len(users)},
        "users":users
    }

# DONE
@app.get('/users/me', tags=["Users"], status_code=200, description="This route gets the current user from the database")
def get_users(user: UserInDB = Depends(get_current_user), session: Session = Depends(DB.get_session)):
    if(user != None):
        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at
            }
        }
    else:
        raise HTTPException(status_code=404, detail={
                "type": "entity_not_found",
                "entity_name": "User",
                "entity_id": "unknown"
            })

# DONE
@app.put('/users/me', tags=["Users"], status_code=200, description="This route updates user info in the database")
def put_user_info(request_body: dict, user: UserInDB = Depends(get_current_user), session: Session = Depends(DB.get_session)):
    return DB.update_user_info(session, user, request_body)

# DONE
@app.get('/users/{user_id}', tags=["Users"], description="This route gets a user from the database")
def get_user(user_id: int, session: Session = Depends(DB.get_session)):
    user = DB.get_user_by_id(session, user_id)
    if(user != None):
        return {
            "user": user
        }
    else:
        raise HTTPException(status_code=404, detail={
                "type": "entity_not_found",
                "entity_name": "User",
                "entity_id": user_id
            })

# DONE
@app.get('/users/{user_id}/chats', tags=["Users"], description="This route gets a user's chats from the database")
def get_users_chats(user_id: int, session: Session = Depends(DB.get_session)):
    
    chats = DB.get_users_chats(session, user_id)
    
    if(chats != None):
        chats =  DB.get_users_chats(session, user_id)
        return {
            "meta": {
                "count": len(chats)
            },
            "chats": chats,
        }
    else:
        raise HTTPException(status_code=404, detail={
                "type": "entity_not_found",
                "entity_name": "User",
                "entity_id": user_id
            })



#### Chats ####

# DONE
@app.get('/chats', tags=["Chats"], description="This route gets all chats from the database")
def get_chats(user: UserInDB = Depends(get_current_user), session: Session = Depends(DB.get_session)):
    chats = DB.get_users_chats(session, user)
    return {
        "meta":{
            "count": len(chats)
        },
        "chats": chats
    }

# DONE
@app.get('/chats/{chat_id}', tags=["Chats"], description="This route gets a specific chat from the database")
def get_chat(chat_id: str, request: Request, user: UserInDB = Depends(get_current_user), session: Session = Depends(DB.get_session)):
    params = request.query_params.getlist("include")
    if(DB.contains_chat(session, chat_id) == True):
        DB.user_in_chat(session, user, chat_id)
        return DB.get_chat_via_id(session, chat_id, params)
    else:
        raise HTTPException(status_code=404, detail={
                "type": "entity_not_found",
                "entity_name": "Chat",
                "entity_id": chat_id
            })

# DONE
@app.put('/chats/{chat_id}', tags=["Chats"], description="This route updates a chat in the database")
def put_chat(chat_id: str, request_body: dict, session: Session = Depends(DB.get_session)):
    new_chat_name = request_body.get('name')

    if(DB.contains_chat(session, chat_id)):
        response = DB.update_chat(session, new_chat_name, chat_id)
        return response
    else:
        raise HTTPException(status_code=404, detail={
                "type": "entity_not_found",
                "entity_name": "Chat",
                "entity_id": chat_id
            })

 
# DONE
@app.get('/chats/{chat_id}/messages', tags=["Chats"], status_code=200, description="This route gets chat's messages from the database")
def get_chat_messages(request: Request, chat_id: str, user: UserInDB = Depends(get_current_user), session: Session = Depends(DB.get_session)):
    DB.user_in_chat(session, user, chat_id)

    if(DB.contains_chat(session, chat_id)):
        #DB.user_in_chat(session, user, chat_id)
        messages = DB.get_messages_in_chat(session, chat_id)
        return {
            "meta": {"count": len(messages)},
            "messages": messages
        }
    else:
        raise HTTPException(status_code=404, detail={
                "type": "entity_not_found",
                "entity_name": "Chat",
                "entity_id": chat_id
            })


# DONE
@app.get('/chats/{chat_id}/users', tags=["Chats"], status_code=200, description="This route gets a list of users in a chat from the database")
def get_chat_users(chat_id: str, user: UserInDB = Depends(get_current_user), session: Session = Depends(DB.get_session)):
    DB.user_in_chat(session, user, chat_id)
    if(DB.contains_chat(session, chat_id)):
        users = DB.get_users_in_chat(session, chat_id)
        return {
            "meta":{
                "count": len(users)
            },
            "users": users
        }
    else:
        raise HTTPException(status_code=404, detail={
                "type": "entity_not_found",
                "entity_name": "Chat",
                "entity_id": chat_id
            })


# DONE
@app.post('/chats/{chat_id}/messages', tags=["Chats"], status_code=201, description="This route puts a message in the database")
def get_chat_messages(chat_id: str, request_body: dict, user: UserInDB = Depends(get_current_user), session: Session = Depends(DB.get_session)):
    DB.user_in_chat(session, user, chat_id)
    text = request_body.get('text')
    response = DB.add_message(session, chat_id, user, text)
    
    return response


#assignment 5 stuff

@app.put('/chats/{chat_id}/messages/{message_id}', tags=["Chats"], status_code=200, description="This route updates a message in the database")
def update_message(chat_id: str, message_id: str, request_body: dict, user: UserInDB = Depends(get_current_user), session: Session = Depends(DB.get_session)):
    DB.user_in_chat(session, user, chat_id)
    text = request_body.get('text')
    response = DB.edit_message(session, user, chat_id, message_id, text)
    return response
    

# DONE
@app.delete('/chats/{chat_id}/messages/{message_id}', tags=["Chats"], status_code=204, description="This route updates a message in the database")
def delete_message(chat_id: str, message_id: str, user: UserInDB = Depends(get_current_user), session: Session = Depends(DB.get_session)):
    DB.user_in_chat(session, user, chat_id)
    DB.delete_message(session, user, chat_id, message_id)
    return