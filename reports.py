from __future__ import annotations
from typing import List, Tuple, Optional
from database import get_cursor
import matplotlib.pyplot as plt


def total_investment() -> float:
    """
    Returns total amount of all investments (0 if none exist).
    """
    query = "SELECT COALESCE(SUM(amount), 0) FROM investments"
    with get_cursor() as (conn, cursor):
        cursor.execute(query)
        total = cursor.fetchone()[0]
    return float(total or 0)


def top_investor() -> Optional[Tuple[int, str, float]]:
    """
    Returns the top investor as (customer_id, customer_name, total_amount),
    or None if there are no investments.
    """
    query = """
        SELECT c.id, c.name, SUM(i.amount) AS total
        FROM customers c
        JOIN investments i ON i.customer_id = c.id
        GROUP BY c.id, c.name
        ORDER BY total DESC
        LIMIT 1
    """
    with get_cursor() as (conn, cursor):
        cursor.execute(query)
        row = cursor.fetchone()
    if row is None:
        return None
    return int(row[0]), str(row[1]), float(row[2])


def investments_by_customer() -> List[Tuple[int, float]]:
    """
    Returns list of tuples (customer_id, total_amount) for all customers.
    """
    query = """
        SELECT customer_id, SUM(amount) AS total
        FROM investments
        GROUP BY customer_id
        ORDER BY customer_id
    """
    with get_cursor() as (conn, cursor):
        cursor.execute(query)
        rows = cursor.fetchall()
    return [(int(r[0]), float(r[1])) for r in rows]


def investment_chart() -> None:
    """
    Draws a bar chart of total investments per customer.
    """
    data = investments_by_customer()
    if not data:
        print("No investment data to plot.")
        return

    ids = [str(cid) for cid, _ in data]
    amounts = [amt for _, amt in data]

    plt.figure(figsize=(8, 5))
    plt.bar(ids, amounts, color="skyblue", edgecolor="black")
    plt.xlabel("Customer ID")
    plt.ylabel("Total Investment")
    plt.title("Investments by Customer")
    plt.tight_layout()
    plt.show()
    plt.close()
