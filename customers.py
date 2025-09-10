from __future__ import annotations
from typing import List, Optional, Tuple
from database import get_cursor


class Customer:
    def __init__(self, name: str, email: str, phone: str, customer_id: Optional[int] = None) -> None:
        self.id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    def save(self) -> None:
        """
        Insert customer if self.id is None, otherwise update.
        """
        if self.id is None:
            query = "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)"
            values = (self.name, self.email, self.phone)
            with get_cursor() as (conn, cursor):
                cursor.execute(query, values)
                self.id = cursor.lastrowid
                print("New customer added.")
        else:
            Customer.update(self.id, self.name, self.email, self.phone)

    @staticmethod
    def get_all() -> List["Customer"]:
        query = "SELECT id, name, email, phone FROM customers ORDER BY id"
        with get_cursor() as (conn, cursor):
            cursor.execute(query)
            rows: List[Tuple[int, str, str, str]] = cursor.fetchall()
            return [Customer(name=r[1], email=r[2], phone=r[3], customer_id=r[0]) for r in rows]

    @staticmethod
    def get_by_id(customer_id: int) -> Optional["Customer"]:
        query = "SELECT id, name, email, phone FROM customers WHERE id=%s"
        with get_cursor() as (conn, cursor):
            cursor.execute(query, (customer_id,))
            row = cursor.fetchone()
        if row is None:
            return None
        return Customer(name=row[1], email=row[2], phone=row[3], customer_id=row[0])

    @staticmethod
    def update(customer_id: int, name: str, email: str, phone: str) -> None:
        query = "UPDATE customers SET name=%s, email=%s, phone=%s WHERE id=%s"
        values = (name, email, phone, customer_id)
        with get_cursor() as (conn, cursor):
            cursor.execute(query, values)
            print(f"Customer {customer_id} updated.")

    @staticmethod
    def delete(customer_id: int) -> None:
        query = "DELETE FROM customers WHERE id=%s"
        with get_cursor() as (conn, cursor):
            cursor.execute(query, (customer_id,))
            print(f"Customer {customer_id} deleted.")

    def __repr__(self) -> str:
        return f"Customer(id={self.id}, name='{self.name}', email='{self.email}', phone='{self.phone}')"
