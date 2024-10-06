from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Book(BaseModel):
  title: str
  author: str
  description: Optional[str] = None
  price: float

@app.get("/")
def read_root():
  return {"message": "Welcome to the Book Library API"}

books = []

@app.post("/books/", response_model=Book)
def create_book(book: Book):
  books.append(book)
  return book

@app.post("/books/bulk/", response_model=List[Book])
def create_books_bulk(new_books: List[Book]):
  books.extend(new_books)
  return new_books

@app.get("/books/", response_model=List[Book])
def read_books():
  return books

@app.get("/books/{title}", response_model=Book)
def read_book(title: str):
  for book in books:
    if book.title.lower() == title.lower():
      return book
  raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{title}", response_model=Book)
def update_book(title: str, updated_book: Book):
  for index, book in enumerate(books):
    if book.title.lower() == title.lower():
      books[index] = updated_book
      return updated_book
    raise HTTPException(status_code=404, detail="Book not found")
  
@app.delete("/books/{title}")
def delete_book(title: str):
  for index, book in enumerate(books):
    if book.title.lower() == title.lower():
      books.pop(index)
      return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")