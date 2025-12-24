from sqlalchemy import Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String, unique=True, index=True)
    hashed_password = mapped_column(String)

class Book(Base):
    __tablename__ = "books"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String)
    author = mapped_column(String)
    genre = mapped_column(String)
    year_published = mapped_column(Integer)

    # NEW FIELD
    storage_path = mapped_column(String, nullable=False)

    reviews = relationship("Review", back_populates="book", cascade="all, delete")


class Review(Base):
    __tablename__ = "reviews"
    id = mapped_column(Integer, primary_key=True)
    book_id = mapped_column(ForeignKey("books.id"))
    user_id = mapped_column(Integer)
    review_text = mapped_column(Text)
    rating = mapped_column(Float)

    book = relationship("Book", back_populates="reviews")
