from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from db.models.blog import Blog
from schemas.blog import CreateBlog
from schemas.blog import UpdateBlog
from sqlalchemy.orm import Session


def create_new_blog(blog: CreateBlog, db: Session, author_id: int = 1) -> Blog:
    """
    Create a new blog in the database.
    Args:
        blog (CreateBlog): The blog object containing the details of the new blog.
        db (Session): The database session.
        author_id (int, optional): The ID of the author. Defaults to 1.
    Returns:
        Blog: The newly created blog object.
    """
    blog = Blog(**blog.model_dump(), author_id=author_id)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


def update_blog(id: int, blog: UpdateBlog, author_id: int, db: Session) -> Blog:
    """
    Update a blog in the database.
    Args:
        id (int): The ID of the blog to update.
        blog (UpdateBlog): The updated blog data.
        author_id (int): The ID of the author.
        db (Session): The database session.
    Returns:
        Blog: The updated blog.
    """
    blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    if not blog_in_db:
        return
    blog_in_db.title = blog.title
    blog_in_db.content = blog.content
    db.add(blog_in_db)
    db.commit()
    return blog_in_db


def retrieve_blog(id: int, db: Session) -> Optional[Blog]:
    """
    Retrieve a blog from the database.
    Args:
        id (int): The ID of the blog.
        db (Session): The database session.
    Returns:
        Optional[Blog]: The retrieved blog, or None if not found.
    """
    blog = db.query(Blog).filter(Blog.id == id).first()
    return blog


def delete_blog(id: int, author_id: int, db: Session) -> Dict[str, Union[str, int]]:
    """
    Delete a blog from the database.
    Args:
        id (int): The ID of the blog to be deleted.
        author_id (int): The ID of the author of the blog.
        db (Session): The database session object.
    Returns:
        Dict[str, Union[str, int]]: A dictionary containing the result of the deletion operation.
            If the blog is not found, the dictionary will contain an "error" key with an error message.
            Otherwise, the dictionary will contain a "msg" key with a success message and the ID of the deleted blog.
    """
    blog_in_db = db.query(Blog).filter(Blog.id == id)
    if not blog_in_db.first():
        return {"error": f"Could not find blog with id {id}"}
    blog_in_db.delete()
    db.commit()
    return {"msg": f"deleted blog with id {id}"}


def list_blogs(db: Session) -> List[Blog]:
    """
    Retrieves a list of active blogs from the database.
    Args:
        db (Session): The database session.
    Returns:
        List[Blog]: A list of active blogs.
    """
    blogs: List[Blog] = db.query(Blog).filter(Blog.is_active == True).all()
    return blogs
