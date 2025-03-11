from sqlmodel import SQLModel, Field, String, LargeBinary
from sqlmodel import create_engine, CheckConstraint, Column, ForeignKey
from uuid import uuid4
from base64 import b64encode
from datetime import date, datetime
from typing import Optional, List

db_engine = create_engine("sqlite:///media.db")

def loadDefaultProfile() -> bytes:
    result: bytes = None
    with open('static/images.jpeg', 'rb') as f2:
        result = f2.read()
    return b64encode(result)

def dateDifferenceInText(date_inp: datetime) -> str:
    difference = datetime.now() - date_inp
    if difference.seconds < 60:
        return f"{int(difference.seconds)} seconds ago"
    elif difference.seconds >= 60 and difference.seconds < 3600:
        if difference.seconds/60 < 2:
            return f"{int(difference.seconds/60)} minute ago"
        return f"{int(difference.seconds/60)} minutes ago"
    elif difference.seconds >= 3600 and difference.seconds < 86400:
        if difference.seconds/3600 < 2:
            return f"{int(difference.seconds/3600)} hour ago"
        return f"{int(difference.seconds/3600)} hours ago"
    elif difference.days == 1:
        return f"{difference.days} day ago"
    elif difference.days >= 30:
        if int(difference.days/30.3) == 1:
            return f"{int(difference.days/30.3)} month ago"
        return f"{int(difference.days/30.3)} months ago"
    elif difference.days >= 365.325:
        if int(difference.days/365.325) == 1:
            return f"{int(difference.days/365.325)} year ago"
    return f"{int(difference.days/365)} years ago"
    
# database schema
class User(SQLModel, table=True):
    id: str = Field(default=str(uuid4()), primary_key=True)   # user id
    username: str = Field(String,unique=True)
    account_birthday: date = Field(default=date.today())
    email: str = Field(String, unique=True)
    password: str = Field(String)
    display_profile: bytes = Field(default=loadDefaultProfile())
    userbio: str = Field(String)

class Post(SQLModel, table=True):
    id: str = Field(default=str(uuid4()), primary_key=True)
    postDate: datetime = Field(default=datetime.now())
    user_id: str = Field(String, foreign_key="user.id")  # reference to user id in User
    postTitle: str = Field(String)
    postimage: bytes
    postdescription: str = Field(String)
    ispublic: bool = Field(default=True)
    
class Follower(SQLModel, table=True):
    f_id: str = Field(default=str(uuid4()), primary_key=True)
    user_id: str = Field(sa_column=Column(String,ForeignKey("user.id")))   # reference to user id in User
    follower_id: str = Field(sa_column=Column(String, ForeignKey("user.id")))  # references user id as well
    # Obviously user id and follower id must not be the same
    # as a user can only follow other users, But not the user itself!
    __table_args__ = (
      CheckConstraint(user_id.sa_column != follower_id.sa_column),
    )
   
class Likes(SQLModel, table=True):
    l_id: str = Field(default=str(uuid4()), primary_key=True)
    post_id: str = Field(String, foreign_key="post.id")
    user_id: str = Field(String, foreign_key="user.id")

class Comments(SQLModel, table=True):
    comment_id: str = Field(default=str(uuid4()),primary_key=True)
    comment: str = Field(String)
    post_id: str = Field(String, foreign_key="post.id")
    user_id: str = Field(String, foreign_key="user.id")
    commentDate: datetime = Field(default=datetime.now())
    
# models
class UserInDB(SQLModel):
    username: str
    email: str
    password: str

class TokenData(SQLModel):
    username: str
    email: str

class Token(SQLModel):
    access_type: str
    token_type: str


SQLModel.metadata.create_all(db_engine)

