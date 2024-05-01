from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from library import models, schemas, crud
from library.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

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


@app.get("/books/", response_model=list[schemas.Book])
def read_authors(db: Session = Depends(get_db)):
    return crud.get_books(db=db)
