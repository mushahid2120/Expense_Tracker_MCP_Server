from datetime import date as date_type
import os
from typing import Literal
from unicodedata import category
import json
from fastmcp import FastMCP
from sqlalchemy import Date, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH")

mcp = FastMCP("Expense_Tracker")
engine = create_engine(f"sqlite:///{DATABASE_PATH}/mydatabase.db")


class Base(DeclarativeBase):
    pass


class Expense(Base):
    __tablename__ = "expense"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    note: Mapped[str] = mapped_column(String, nullable=True)


Base.metadata.create_all(engine)


def date_encoder(obj):
    if isinstance(obj, date_type):
        return obj.isoformat()

    raise TypeError(f"{type(obj)} is not JSON serializable")


@mcp.tool()
async def add_expense(
    date: date_type,
    amount: int,
    category: Literal[
        "Education",
        "Clothes",
        "Shoes",
        "Accesories",
        "Ration",
        "Bills",
    ],
    note: str,
):
    "Add a new expense entry to the dataset by providing date:(eg: 2020-20-10),amount:integer,category:string,notes:string"
    try:
        with Session(engine) as session:
            expense = Expense(date=date, amount=amount, category=category, note=note)
            session.add(expense)
            await session.commit()
        return {"status": "Data has been added to the database"}
    except Exception as error:
        print(error)
        return error


@mcp.tool()
def list_expenses(
    start_date: date_type | None = None, end_date: date_type = date_type.today()
):
    """Get all the Expense list (start_date=None) or you can get Expense list in between specific date (end_date=today's date)"""
    try:
        expense_list = (
            (
                select(
                    Expense.date, Expense.amount, Expense.category, Expense.note
                ).order_by(Expense.date.asc())
            )
            if start_date is None
            else (
                select(Expense.date, Expense.amount, Expense.category, Expense.note)
                .where(Expense.date >= start_date)
                .where(Expense.date <= end_date)
                .order_by(Expense.date.asc())  # Optional: Sort from oldest to newest
            )
        )
        with Session(engine) as session:
            result = session.execute(expense_list).mappings().all()
        converted_result = [dict(row) for row in result]
        return json.dumps(converted_result, default=date_encoder, indent=4)

    except Exception as error:
        return {
            "status": "error",
            "message": str(error),
        }


@mcp.resource("expense://category")
def categories() -> str:
    """Returns the list of valid expense categories as a JSON string."""
    try:
        category_list = [
            "Education",
            "Clothes",
            "Shoes",
            "Accesories",
            "Ration",
            "Bills",
        ]

        # MCP resources must return text or bytes, so convert your list to a JSON string!
        return json.dumps(category_list)
    except Exception as error:
        return {
            "status": "error",
            "message": str(error),
        }


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
