from typing import Optional

from fastapi import FastAPI, HTTPException, status,Response, Depends, APIRouter
from fastapi.params import Body
from model.schemas import PostCreate, PostResponse, PostResponseWithVotes
from sqlalchemy.orm import Session
from model import model
from model.database import get_db
import oauth2
from sqlalchemy import func

from sqlalchemy.orm import joinedload

post_router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



# @post_router.get("/posts", response_model=list[PostResponse])
@post_router.get("/posts", response_model=list[PostResponseWithVotes])
# @post_router.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     print(posts)
#     return {"data": posts}
def get_posts(db: Session = Depends(get_db),  current_user: int =Depends(oauth2.get_current_user), limit: int= 10, skip: int=0, search: Optional[str]=""):
    # posts = db.query(model.Post).limit(limit).all()
    # posts = db.query(model.Post).filter(
    #     model.Post.title.contains(search)
    # ).limit(limit).offset(skip).all()

    # results = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(model.Vote, model.Vote.post_id==model.Post.id, isouter=True).group_by(model.Post.id).all()
    results = db.query(
        model.Post,
        func.count(model.Vote.post_id).label("votes")
    ).join(
        model.Vote,
        model.Vote.post_id == model.Post.id,
        isouter=True
    ).group_by(model.Post.id).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()


    return results


    # posts = db.query(model.Post).options(joinedload(model.Post.owner)).all()
    # posts = db.query(model.Post).filter(model.Post.owner_id == current_user.id).all()
    # return results

@post_router.get("/posts/{id}", response_model=PostResponseWithVotes)
# def get_post(id: int):
#     if id < 0:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#     return {"message": f"Post with id {id} retrieved", "data": post}
def get_post(id: int, db: Session = Depends(get_db),  current_user: int =Depends(oauth2.get_current_user)):
    if id < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # post = db.query(model.Post).filter(model.Post.id == id).first()
    post = db.query(
        model.Post,
        func.count(model.Vote.post_id).label("votes")
    ).join(
        model.Vote,
        model.Vote.post_id == model.Post.id,
        isouter=True
    ).group_by(model.Post.id).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return  post


@post_router.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(payload: PostCreate):
#     payload = payload.model_dump()

#     print(payload)
#     cursor.execute(
#         """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
#         (payload["title"], payload["content"], payload["published"])
#     )
#     new_post = cursor.fetchone()


#     conn.commit()
#     return {"message": "Post created successfully", "data": new_post}
def create_posts(payload: PostCreate, db: Session = Depends(get_db), response_model=PostResponse, current_user: int =Depends(oauth2.get_current_user)):
    payload = payload.model_dump()
    current_user
    new_post = model.Post(owner_id=current_user.id,**payload)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




@post_router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     if id < 0:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found" )

#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found" )

#     return Response(status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    if id < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found" )

    delete_post_query = db.query(model.Post).filter(model.Post.id == id)

    delete_post = delete_post_query.first()
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found" )

    if delete_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    # db.delete(delete_post)
    delete_post_query.delete(synchronize_session=False)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)

@post_router.put("/posts/{id}", response_model=PostResponse)
# def update_post(id: int, payload: PostCreate):

#     if id == None or id <  0:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
#     payload = payload.model_dump()
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (payload["title"], payload["content"], payload["published"], str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
#     print(payload)
#     return {"message": f"Post with id {id} updated successfully", "data": updated_post}
def update_post(id: int, payload: PostCreate, db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):

    if id == None or id <  0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    payload = payload.model_dump()
    post_query = db.query(model.Post).filter(model.Post.id == id)
    update_post = post_query.first()

    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")


    if update_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.update(payload, synchronize_session=False)
    # updated_post.title = payload["title"]
    # updated_post.content = payload["content"]
    # updated_post.published = payload["published"]
    # if "rating" in payload:
    #     updated_post.rating = payload["rating"]
    db.commit()
    # db.refresh(updated_post)
    print(payload)
    return  post_query.first()



# @post_router.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     return db.query(model.Post).all()

