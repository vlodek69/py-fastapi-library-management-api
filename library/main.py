from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from library import models, schemas, crud
from library.database import engine, SessionLocal


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db=db)


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_author_by_id(db=db, author_id=author_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_user


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(db: Session = Depends(get_db)):
    return crud.get_books(db=db)


@app.post("/books/", response_model=schemas.Book)
def create_books(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
