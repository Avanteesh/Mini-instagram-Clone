from fastapi import FastAPI, Depends, HTTPException, status, Request, Form, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime, timedelta
from jose import JWTError,jwt
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import (Session, select, update, delete)
from passlib.context import CryptContext
from datetime import datetime, timedelta
from models import db_engine, User, UserInDB, Post, Comments, Follower
from models import TokenData, Token, dateDifferenceInText, Likes
from os import environ
from dotenv import load_dotenv
from datetime import date as Date
from json import loads, dumps

load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory='static'), name='static')
templates = Jinja2Templates("templates")
session = Session(db_engine)
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def getUser(username: str, email: str) -> User:
    query = session.exec(
      select(User).where(User.username == username).where(
        User.email == email
      )
    ).first()
    if query:
        return UserInDB(
          username=query.username,email=query.email,password=query.password
        )
    
def authenticate(username: str, email: str, password: str):
    user = getUser(username, email)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user

def createAccessToken(data: dict):
    encoded = data.copy()
    expire_time = datetime.now() + timedelta(minutes=int(environ.get('TOKEN_EXPIRE_TIME')))
    encoded.update({'exp': expire_time})
    encoded_jwt = jwt.encode(encoded, environ.get('SECRET_KEY'),algorithm=environ.get('ALGORITHM'))
    return encoded_jwt

def verifyJWT(request: Request):
    token = request.cookies.get("session")
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized user!")
    return token

async def getCurrentUser(token: str=Depends(verifyJWT)):
    credentialException = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials!",
      headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token, environ.get("SECRET_KEY"),algorithms=[environ.get("ALGORITHM")])  # decode jwt token
        json = loads(payload.get("sup"))
        if json is None:
            raise credentialException  
        tokendata = TokenData(username=json["username"], email=json["email"])
    except JWTError:
        raise credentialException
    user_data = getUser(username=tokendata.username, email=tokendata.email)
    if user_data is None:
        raise credentialException
    theuser = session.exec(
      select(User).where(
        User.email == user_data.email
      ).where(
        User.username == user_data.username
      ).where(User.password == user_data.password)
    ).first()
    return theuser

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(
      request, name='index.html'
    )

@app.get("/sign-in", response_class=HTMLResponse)
async def signIn(request: Request):
    return templates.TemplateResponse(
      request, name='signup.html'
    )

@app.post("/signin-user")
async def signInNewUser(request: Request,display_profile: bytes=Form(...), username: str=Form(...),
    email: str=Form(...),password: str=Form(...),userbio: str=Form(...)):
    findUser = session.exec(select(User).where(
        User.username == username
    ).where(User.email == email)).first()
    if findUser is not None:
        return RedirectResponse(url="/", status_code=303)
    hashed_pass = pwd_context.hash(password)
    if display_profile == b"":
        session.add(User(
          username=username,email=email,password=hashed_pass,
          userbio=userbio               
        ))
    else:
        session.add(User(
          username=username,email=email,password=hashed_pass,
          display_profile=display_profile,userbio=userbio
        ))
    session.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/token", response_class=HTMLResponse)
async def loginTheUser(request: Request, username: str=Form(...),email: str=Form(...),password: str=Form(...)):
    isAuthentic = authenticate(username, email, password)
    if not isAuthentic:
        return RedirectResponse(url="/", status_code=303)
    new_accesstoken = createAccessToken(
      data={"sup": dumps({"username": username, "email": email})}
    )
    template_res = templates.TemplateResponse(
      request,name='pager.html'
    )
    template_res.set_cookie(key="session", value=new_accesstoken)
    return template_res

@app.get("/profile/main", response_class=HTMLResponse)
async def openProfilePage(request: Request, user: User=Depends(getCurrentUser)):
    publicposts = session.exec(
      select(Post.id, Post.postimage).where(Post.user_id == user.id).where(
        Post.ispublic == True
      ).order_by(Post.postDate)
    ).fetchall()
    userfollowers = session.exec(
      select(Follower.follower_id, User.username).join(
        Follower, Follower.follower_id == User.id
      ).where(Follower.user_id == user.id)
    ).fetchall()
    return templates.TemplateResponse(
      request, name="profile.html",context={
        "username": user.username, "display_profile": user.display_profile.decode("utf-8"),
        "userbio": user.userbio, "posts": publicposts, "public": True,
        "sameuser": True
      }
    )

@app.get("/profile/private", response_class=HTMLResponse)
async def openProfileWithPrivatePost(request: Request, user: User=Depends(getCurrentUser)):
    privateposts = session.exec(
      select(Post.id, Post.postimage).where(Post.user_id == user.id).where(
        Post.ispublic == False
      ).order_by(Post.postDate)
    ).fetchall()
    return templates.TemplateResponse(
      request, name="profile.html", context={
        "username": user.username, "display_profile": user.display_profile.decode("utf-8"),
        "userbio": user.userbio, "posts": privateposts, "public": False,
        "sameuser": True
      }
    )

@app.get("/new-post", response_class=HTMLResponse)
async def openProfilePage(request: Request, user: User=Depends(getCurrentUser)):
    userposts = session.exec(
      select(Post.id,Post.postDate).where(Post.user_id == user.id).order_by(Post.postDate)
    ).fetchall()
    message = None
    if len(userposts) == 0:
        message = "Let your first post be the best!"
    elif (datetime.now() - userposts[0].postDate).days >= 30:
        message = "Its Good to see you post after a long time!"
    return templates.TemplateResponse(
      request, name="newPost.html", context={"message":message}
    )

@app.post("/update-profile")
async def updateProfileDetails(request: Request,username: str=Form(...), userbio: str=Form(...),
    updatedProfile: bytes=Form(...),user: User=Depends(getCurrentUser)):
    searchquery = session.exec(select(User).where(User.username == username)).fetchall()
    if len(searchquery) != 0:
        return RedirectResponse(url="/profile/main", status_code=303)
    session.exec(update(User).where(User.id == user.id).values(
      display_profile = updatedProfile
    ).values(userbio = userbio).values(
      username = username
    ))
    new_cookie = createAccessToken(data={"sup": dumps({
     "username": username,"email": user.email 
    })})
    session.commit()
    template_res = templates.TemplateResponse(
     request, name="pager.html"
    )
    template_res.set_cookie(key="session",value=new_cookie)
    return template_res

@app.get("/profile/{username}", response_class=HTMLResponse)
async def showOtherUsersProfile(username: str,request: Request,user: User=Depends(getCurrentUser)):
    if username == user.username:   # if query user is same as logged in user go to profile page!
        return RedirectResponse(url="/profile/main", status_code=303)  
    targetuser = session.exec(select(User).where(User.username == username)).first()
    if targetuser is None:
        raise credential_exception
    posts = session.exec(
      select(Post).where(Post.user_id == targetuser.id).where(
        Post.ispublic == True
      )
    ).fetchall()
    return templates.TemplateResponse(
      request, name='profile.html', context={
        "public": True, "posts": posts, "display_profile": targetuser.display_profile.decode(),
        "userbio": targetuser.userbio, "username": username, "sameuser": False
      }
    )

@app.get("/post/{username}/{post_id}", response_class=HTMLResponse)
async def viewPost(username: str, post_id: str, request: Request, user: User=Depends(getCurrentUser)):
    query = session.exec(
      select(Post.postDate,Post.postTitle,Post.postimage,Post.postdescription,
        User.display_profile,User.username,User.id,Post.ispublic).join(User,Post.user_id == User.id
      ).where(Post.id == post_id).where(User.username == username)
    ).first()
    if query is None:
        return RedirectResponse(url="/profile/main", status_code=303)
    # if post is private Only User can access it!
    if query[-1] == False:
        if user.username == username:
            return templates.TemplateResponse(
              request, name='viewpost.html', context={
                "postUploaded": dateDifferenceInText(query[0]), "private": True,
                "post_image": query[2].decode(), "post_title": query[1],
                "post_description": query[3], "display_profile": query[4].decode(),
                "username": query[5], "isCurrentUser": True
              }
            )
        else:
            raise credential_exception 
    usercomments = session.exec(
      select(Comments.comment_id,Comments.comment,Comments.commentDate,
        User.username,User.id,User.display_profile).join(User,Comments.user_id == User.id).where(
        Comments.post_id == post_id
      )
    ).fetchall()
    postlikes = session.exec(select(Likes).where(Likes.post_id == post_id)).fetchall()
    isLikedByUser = session.exec(select(Likes).where(
      Likes.post_id == post_id
    ).where(
      Likes.user_id == user.id    
    )).first()
    return templates.TemplateResponse(
      request, name='viewpost.html', context={
        "postUploaded": dateDifferenceInText(query[0]),"username": query[5],
        "display_profile": query[4].decode(),"post_title": query[1],
        "post_description": query[3],"post_image": query[2].decode(),
        "isCurrentUser": (query[5] == user.username), "postcomments": usercomments,
        "likes": postlikes, "islikedbyuser": (isLikedByUser != None),
        "active_users_id": user.id, "private": False
      }
    )

@app.put("/like-post", response_class=HTMLResponse)
async def likePost(post_id: str, user: User=Depends(getCurrentUser)):
    alreadyliked = session.exec(select(Likes).where(
      Likes.user_id == user.id
    ).where(Likes.post_id == post_id)).first()
    if alreadyliked is None:
        # if user has not liked the post yet, let it be liked and save it!
        session.add(Likes(post_id=post_id, user_id=user.id))
    else:
        # if user has already liked it remove the like from the post!
        session.exec(delete(Likes).where(
          Likes.user_id == user.id                 
        ).where(Likes.post_id == post_id))
    session.commit()
    getpostowner = session.exec(
      select(User.username, Post.id).join(User, Post.user_id == User.id).where(
        Post.id == post_id
      )
    ).first()
    return RedirectResponse(url=f"/post/{getpostowner[0]}/{post_id}", status_code=303)

@app.post("/create-newpost", response_class=HTMLResponse)
async def createNewPost(postTitle: str=Form(...), postImage: bytes=Form(...),
    postVisibility: str=Form(...),description:str=Form(...), user: User=Depends(getCurrentUser)):
    session.add(Post(
      postTitle=postTitle,user_id=user.id,postimage=postImage,
      ispublic=(True if postVisibility == "public" else False),
      postdescription=description
    ))
    session.commit()
    if postVisibility == "public":
        return RedirectResponse(url="/profile/main", status_code=303)
    return RedirectResponse(url="/profile/private", status_code=303)

@app.put("/new-comment")
async def addNewComment(post_id: str, comment: str, user: User=Depends(getCurrentUser)):
    print(comment)
    session.add(Comments(comment=comment,post_id=post_id,user_id=user.id))
    session.commit()
    getpostowner = session.exec(
      select(User.username, Post.id).where(User, Post.user_id == User.id).where(
        Post.id == post_id
      )
    ).first()
    return RedirectResponse(url=f"/post/{getpostowner[0]}/{post_id}", status_code=303)

@app.put("/edit-comment")
async def editComment(comment_id: str, comment: str, user: User=Depends(getCurrentUser)):
    print(comment)
    
    
@app.delete("/delete-post/{post_id}")
async def deletePost(post_id: str, user: User=Depends(getCurrentUser)):
    session.exec(delete(Post).where(Post.id == post_id))  # delete the post!
    session.commit()
    return

@app.delete("/delete-comment/{post_id}/{comment_id}")
async def deleteComment(post_id: str, comment_id: str, user: User=Depends(getCurrentUser)):
    session.exec(delete(Comments).where(
      Comments.post_id == post_id             
    ).where(Comments.comment_id == comment_id))
    session.commit()
    return

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, user: User=Depends(getCurrentUser)):
    return templates.TemplateResponse(
      request, name="home.html"
    )


