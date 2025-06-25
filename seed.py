from sqlalchemy.orm import Session, sessionmaker
from models.account import AccountModel
from models.user import UserModel
from models.transaction import TransactionModel
from models.base import Base
from data.user_data import user_list
from data.account_data import accounts_list
from data.transaction_data import transaction_list
from config.environment import db_URI
from sqlalchemy import create_engine

engine = create_engine(db_URI)
SessionLocal = sessionmaker(bind=engine)

try:
    print("Recreating database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("Seeding database...")
    db = SessionLocal()

    db.add_all(user_list)
    db.commit()

    db.add_all(accounts_list)
    db.commit()



    db.add_all(transaction_list)
    db.commit()


    db.close()

    print("Database seeding complete! 👋")
except Exception as e:
    print("An error occurred:", e)