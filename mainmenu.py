from __future__ import annotations
from customers import Customer
from investment import Investment
from reports import total_investment, top_investor, investment_chart
from rich.console import Console
from rich.table import Table
import csv

console = Console()

def list_customers() -> None:
    customers = Customer.get_all()
    if not customers:
        console.print("[red]No customers found.[/red]")
        return
    table = Table(title="Customers", show_lines=True)
    table.add_column("ID", justify="right")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Phone")

    for c in customers:
        table.add_row(str(c.id), c.name, c.email, c.phone)
    console.print(table)


def list_investments() -> None:
    investments = Investment.get_all()
    if not investments:
        console.print("[red]No investments found.[/red]")
        return
    table = Table(title="Investments", show_lines=True)
    table.add_column("ID", justify="right")
    table.add_column("Customer ID", justify="right")
    table.add_column("Amount", justify="right")
    table.add_column("Type")
    table.add_column("Start")
    table.add_column("End")
    table.add_column("Expected Profit", justify="right")
    for inv in investments:
        table.add_row(
            str(inv.id),
            str(inv.customer_id),
            f"{inv.amount:.2f}",
            inv.investment_type,   
            str(inv.start_date),
            str(inv.end_date or "-"),
            f"{inv.expected_profit:.2f}",
        )
    console.print(table)


def customer_summary() -> None:
    customers = Customer.get_all()
    if not customers:
        console.print("[red]No customers found.[/red]")
        return
    table = Table(title="Summary of Investments", show_lines=True)
    table.add_column("Customer ID", justify="right")
    table.add_column("Name")
    table.add_column("Total Investments", justify="right")
    table.add_column("Total Expected Profit", justify="right")

    for c in customers:
        invs = Investment.get_by_customer(c.id)
        total_amt = sum(i.amount for i in invs)
        total_profit = sum(i.expected_profit for i in invs)
        table.add_row(str(c.id), c.name, f"{total_amt:.2f}", f"{total_profit:.2f}")
    console.print(table)


def input_int(prompt: str) -> int:
    while True:
        val = input(prompt).strip()
        if val.isdigit():
            return int(val)
        console.print("[red]Please enter a valid integer.[/red]")


def input_float(prompt: str) -> float:
    while True:
        val = input(prompt).strip()
        try:
            return float(val)
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")


def menu():
    while True:
        console.rule("[bold cyan]Investment Management System[/bold cyan]")
        console.print(
            "[yellow]1[/yellow]. Add customer\n"
            "[yellow]2[/yellow]. List customers\n"
            "[yellow]3[/yellow]. Update customer\n"
            "[yellow]4[/yellow]. Delete customer\n"
            "[yellow]5[/yellow]. Add investment\n"
            "[yellow]6[/yellow]. List investments\n"
            "[yellow]7[/yellow]. Customer summary\n"
            "[yellow]8[/yellow]. Show top investor & totals\n"
            "[yellow]9[/yellow]. Plot investments chart\n"
            "[yellow]0[/yellow]. Exit"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            Customer(name, email, phone).save()
            console.print("[green]Customer added successfully![/green]")

        elif choice == "2":
            list_customers()

        elif choice == "3":
            customer_id = input_int("Customer ID to update: ")
            name = input("New name: ").strip()
            email = input("New email: ").strip()
            phone = input("New phone: ").strip()
            Customer.update(customer_id, name, email, phone)
            console.print("[green]Customer updated successfully![/green]")

        elif choice == "4":
            customer_id = input_int("Customer ID to delete: ")
            Customer.delete(customer_id)
            console.print("[green]Customer deleted successfully![/green]")

        elif choice == "5":
            customer_id = input_int("Customer ID: ")
            amount = input_float("Investment amount: ")
            investment_type = input("Investment type: ").strip()
            start_date = input("Start date (YYYY-MM-DD): ").strip()
            end_date = input("End date (YYYY-MM-DD): ").strip() or None
            expected_profit = input_float("Expected profit: ")
            Investment(customer_id, amount, investment_type, start_date, end_date, expected_profit).save()
            console.print("[green]Investment added successfully![/green]")

        elif choice == "6":
            list_investments()

        elif choice == "7":
            customer_summary()

        elif choice == "8":
            total = total_investment()
            top = top_investor()
            console.print(f"[bold]Total invested:[/bold] {total:.2f}")
            if top:
                cid, name, t = top
                console.print(f"[bold]Top investor:[/bold] {name} (ID {cid}) with {t:.2f}")
            else:
                console.print("No investments yet.")

        elif choice == "9":
            investment_chart()

        elif choice == "0":
            console.print("Goodbye 👋")
            break

        else:
            console.print("[red]Invalid option.[/red]")


if __name__ == "__main__":
    menu()
