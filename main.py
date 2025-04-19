from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 🎯 Модель SQLAlchemy
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# 🛠️ Створення таблиці
Base.metadata.create_all(bind=engine)

# 📦 FastAPI додаток
app = FastAPI()

# 🔁 Залежність для сесії
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🧾 Схема (можна через Pydantic, але тут просто)
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str

# 🚀 Створення користувача
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 📥 Отримати всіх користувачів
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()
