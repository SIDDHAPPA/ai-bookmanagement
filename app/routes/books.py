from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Book, Review
from app.schemas import BookCreate, BookUpdate, ReviewCreate
from app.auth import get_current_user
from app.services.llm_client import generate_summary
from fastapi import UploadFile, File, Form
from app.services.storage import upload_file
from app.services.storage import get_file_content

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/")
async def add_book(
    title: str = Form(...),
    author: str = Form(...),
    genre: str = Form(...),
    year_published: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    key = f"books/{file.filename}"

    upload_file(
        file.file,
        key,
        file.content_type
    )

    book = Book(
        title=title,
        author=author,
        genre=genre,
        year_published=year_published,
        storage_path=key
    )

    db.add(book)
    await db.commit()
    await db.refresh(book)

    return book


@router.get("/")
async def get_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    return result.scalars().all()

@router.get("/{book_id}")
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    return book

@router.put("/{book_id}")
async def update_book(book_id: int, data: BookUpdate,
                      db: AsyncSession = Depends(get_db),
                      user=Depends(get_current_user)):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(404, "Book not found")

    for k, v in data.dict().items():
        setattr(book, k, v)

    await db.commit()
    await db.refresh(book)
    return book

@router.delete("/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db),
                      user=Depends(get_current_user)):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(404, "Book not found")

    await db.delete(book)
    await db.commit()
    return {"message": "Book deleted"}

@router.post("/{book_id}/reviews")
async def add_review(book_id: int, review: ReviewCreate,
                     db: AsyncSession = Depends(get_db),
                     user=Depends(get_current_user)):
    if not await db.get(Book, book_id):
        raise HTTPException(404, "Book not found")

    db.add(Review(
        book_id=book_id,
        user_id=user["user_id"],
        review_text=review.review_text,
        rating=review.rating
    ))
    await db.commit()
    return {"message": "Review added"}

@router.get("/{book_id}/reviews")
async def get_reviews(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).where(Review.book_id == book_id))
    return result.scalars().all()

@router.get("/{book_id}/summary")
async def book_summary(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(404, "Book not found")

    book_text = get_file_content(book.storage_path)

    reviews_result = await db.execute(
        select(Review).where(Review.book_id == book_id)
    )
    reviews = reviews_result.scalars().all()

    review_text = " ".join(r.review_text for r in reviews)
    avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else None

    return {
        "book_summary": await generate_summary(book_text),
        "review_summary": await generate_summary(review_text),
        "average_rating": avg_rating
    }