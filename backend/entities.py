from datetime import date, datetime

from pydantic import BaseModel, Field

class User(BaseModel):
    """"Represents a user in the database"""
    id: str
    created_at: datetime

class Message(BaseModel):
    """"Represents a chat in the database"""
    id: str
    user_id: str
    text: str
    created_at: datetime

class Chat(BaseModel):
    """Represents a chat in the database"""
    id: str
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime
    messages: list[Message]

class Metadata(BaseModel):
    """Represents metadata for a collection."""
    count: int

class ChatCollection(BaseModel):
    """Represents a collection of Chats"""
    meta: Metadata
    chats: list[Chat]

class UserCollection(BaseModel):
    """Represents a collection of Users"""
    meta: Metadata
    users: list[User]

class MessageCollection(BaseModel):
    """Represents a collection of Messages"""
    meta: Metadata
    messages: list[Message]

class Detail(BaseModel):
    """Represents an exceptional response from the server"""
    type: str
    entity_name: str
    entity_id: str