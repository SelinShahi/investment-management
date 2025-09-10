from __future__ import annotations
from typing import List, Optional, Tuple
from database import get_cursor


class Investment:
    def __init__(
        self,
        customer_id: int,
        amount: float,
        investment_type: str,
        start_date: str,
        end_date: Optional[str],
        expected_profit: float,
        investment_id: Optional[int] = None
    ):
        self.id = investment_id
        self.customer_id = customer_id
        self.amount = amount
        self.investment_type = investment_type
        self.start_date = start_date
        self.end_date = end_date
        self.expected_profit = expected_profit

    def save(self) -> None:
        """
        Insert investment into database.
        """
        query = """
            INSERT INTO investments (customer_id, amount, investment_type, start_date, end_date, expected_profit)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            self.customer_id,
            self.amount,
            self.investment_type,
            self.start_date,
            self.end_date,
            self.expected_profit,
        )
        with get_cursor() as (conn, cursor):
            cursor.execute(query, values)
            self.id = cursor.lastrowid
            print("Investment added.")

    @staticmethod
    def get_all() -> List["Investment"]:
        query = """
            SELECT id, customer_id, amount, investment_type, start_date, end_date, expected_profit
            FROM investments
            ORDER BY id
        """
        with get_cursor() as (conn, cursor):
            cursor.execute(query)
            rows: List[Tuple] = cursor.fetchall()
        return [
            Investment(
                investment_id=r[0],
                customer_id=r[1],
                amount=float(r[2]),
                investment_type=r[3],
                start_date=str(r[4]),
                end_date=str(r[5]) if r[5] is not None else None,
                expected_profit=float(r[6]),
            )
            for r in rows
        ]

    @staticmethod
    def get_by_customer(customer_id: int) -> List["Investment"]:
        query = """
            SELECT id, customer_id, amount, investment_type, start_date, end_date, expected_profit
            FROM investments
            WHERE customer_id = %s
            ORDER BY id
        """
        with get_cursor() as (conn, cursor):
            cursor.execute(query, (customer_id,))
            rows: List[Tuple] = cursor.fetchall()
        return [
            Investment(
                investment_id=r[0],
                customer_id=r[1],
                amount=float(r[2]),
                investment_type=r[3],
                start_date=str(r[4]),
                end_date=str(r[5]) if r[5] is not None else None,
                expected_profit=float(r[6]),
            )
            for r in rows
        ]

    def __repr__(self) -> str:
        return (
            f"Investment(id={self.id}, customer_id={self.customer_id}, amount={self.amount}, "
            f"investment_type='{self.investment_type}', start='{self.start_date}', "
            f"end='{self.end_date}', expected_profit={self.expected_profit})"
        )
