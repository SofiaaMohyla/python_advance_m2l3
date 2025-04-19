from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# 💾 Налаштування бази даних
DATABASE_URL = "sqlite:///./test1.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


# 👤 Модель користувача
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


# 🧱 Створення таблиць
def init_db():
    Base.metadata.create_all(bind=engine)


# 🔄 Отримання сесії (ручна альтернатива get_db)
def get_session() -> Session:
    return SessionLocal()


# ➕ Створити користувача
def create_user(name: str):
    db = get_session()
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    #print(f"[+] Створено користувача:  - {user.name}")


# 📋 Отримати всіх користувачів
def list_users():
    db = get_session()
    users = db.query(User).all()
    db.close()
    print("[📋] Всі користувачі:")
    for user in users:
        print(f"{user.id}: {user.name}")


# 🔍 Знайти користувача за ім'ям
def find_user(name: str):
    db = get_session()
    user = db.query(User).filter(User.name == name).first()
    db.close()
    if user:
        print(f"[🔍] Знайдено: {user.id} - {user.name}")
    else:
        print("[❌] Користувача не знайдено")


# ✏️ Оновити ім'я користувача
def update_user(user_id: int, new_name: str):
    db = get_session()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.name = new_name
        db.commit()
        print(f"[✏️] Оновлено: ID {user_id} → {new_name}")
    else:
        print("[❌] Користувача не знайдено")
    db.close()


# ❌ Видалити користувача
def delete_user(user_id: int):
    db = get_session()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        print(f"[🗑️] Видалено користувача з ID {user_id}")
    else:
        print("[❌] Користувача не знайдено")
    db.close()


# 🧪 Демонстрація роботи
if __name__ == "__main__":
    #Base.metadata.create_all(bind=engine)

    #create_user("Alice2")
     create_user("Bob")

    # list_users()

    # find_user("Alice")

    # update_user(1, "Alicia")

    # delete_user(2)

    # list_users()
