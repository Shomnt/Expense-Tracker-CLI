import argparse
import json
import os.path
import sys
import time
from datetime import datetime

print_table_form = "| {:3} | {:^10} | {:^17} | {:^5} | {:^10} |"
print_column_names = ["ID", "Date", "Description", "Amount", "Category"]

def create_json() -> None:
    with open("data.json", 'w') as f:
        data = {
            "meta": {
                "last_id": 0,
                "free_ids": []
            }
        }
        json.dump(data, f)

def add(description: str, amount: int, category: str) -> None:
    try:
        with open("data.json", 'r') as f:
            data = json.load(f)
        with open("data.json", 'w') as f:
            id_exp = data["meta"]["last_id"]
            if data["meta"]["free_ids"]:
                id_exp = data["meta"]["free_ids"].pop()
            else:
                data["meta"]["last_id"] = data["meta"]["last_id"] + 1

            data[id_exp] = {
                "id": id_exp,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "description": description,
                "amount": amount,
                "category": category,
            }
            json.dump(data, f)
            print(f"# Expense added successfully (ID: {id_exp})")
    except FileNotFoundError:
        print("File not found")

def update(id_exp: int, description: str = None, amount: int = None, category: str = None) -> None:
    try:
        with open("data.json", 'r') as f:
            data = json.load(f)
        with open("data.json", 'w') as f:
            if data.get(str(id_exp), False):
                if description:
                    data[str(id_exp)]["description"] = description
                if amount:
                    data[str(id_exp)]["amount"] = amount
                if category:
                    data[str(id_exp)]["category"] = category
                json.dump(data, f)
                print("# Expense updated successfully")
            else:
                print(f"Expense with ID={id_exp} doesn't exist")
    except FileNotFoundError:
        print("File not found")

def delete(id_exp: int) -> None:
    try:
        with open("data.json", 'r') as f:
            data = json.load(f)
        with open("data.json", 'w') as f:
            if data.get(str(id_exp), False):
                del data[str(id_exp)]
                data["meta"]["free_ids"].append(id_exp)
                json.dump(data, f)
                print("# Expense deleted successfully")
            else:
                print(f"Expense with ID={id_exp} doesn't exist")
    except FileNotFoundError:
        print("File not found")

def list_expense(id_exp: int = None, category: str = None) -> None:
    try:
        with open("data.json", 'r') as f:
            data = json.load(f)
        print(print_table_form.format(*print_column_names))
        if id_exp is not None:
            exp = data[str(id_exp)]
            print(print_table_form.format(exp["id"], exp["date"], exp["description"], exp["amount"], exp["category"]))
        else:
            for key in list(data.keys())[1:]:
                if category is None or data[key]["category"] == category:
                    exp = data[key]
                    print(print_table_form.format(exp["id"], exp["date"], exp["description"], exp["amount"], exp["category"]))

    except FileNotFoundError:
        print("File not found")

def summary(month: int = None) -> None:
    try:
        with open("data.json", 'r') as f:
            data = json.load(f)
        s = 0
        for id_exp in list(data.keys())[1:]:
            m = datetime.strptime(data[id_exp]["date"], "%Y-%m-%d").month
            if month is None or m == month:
                s += data[id_exp]["amount"]
        if month is not None:
            m = datetime.strptime(f'{month}', "%m").strftime("%B")
            print(f"# Total expenses for {m}: ${s}")
        else:
            print(f"# Total expenses: ${s}")

    except FileNotFoundError:
        print("File not found")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(prog="Expense Tracker",
                                     description="Tracker with some commands")
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # add
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("-d", "--description", help="The description of the expense", required=True)
    add_parser.add_argument("-a", "--amount", help="The amount of the expense", type=int, required=True)
    add_parser.add_argument("-c", "--category",
                            help="The category of the expense",
                            required=False,
                            default="Something")

    # update
    update_parser = subparsers.add_parser("update", help="Update an expense")
    update_parser.add_argument("-i", "--id", help="The id of the expense", type=int, required=True)
    update_parser.add_argument("-d", "--description",
                               help="The new description of the expense",
                               required=False)
    update_parser.add_argument("-a", "--amount",
                               help="The new amount of the expense",
                               type=int,
                               required=False)
    update_parser.add_argument("-c", "--category",
                               help="The new category of the expense",
                               required=False)

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("-i", "--id", help="The id of the expense", type=int, required=True)

    # list
    list_parser = subparsers.add_parser("list", help="View expenses")
    group = list_parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-i", "--id", help="The id of the expense", type=int,  required=False)
    group.add_argument("-c", "--category", help="The category of the expenses", required=False)

    # summary
    summary_parser = subparsers.add_parser("summary", help="View summary of an expenses")
    summary_parser.add_argument("-m", "--month", help="The month", type=int, required=False)

    args = parser.parse_args()

    if not os.path.isfile("data.json"):
        create_json()
        time.sleep(1)

    match args.command:
        case "add":
            if args.amount < 0:
                print(f"# Expense amount cannot be negative")
                sys.exit(1)
            add(args.description, args.amount, args.category)
        case "update":
            if args.amount and args.amount < 0:
                print(f"# Expense amount cannot be negative")
                sys.exit(1)
            update(args.id, args.description, args.amount, args.category)
        case "delete":
            delete(args.id)
        case "list":
            list_expense(args.id, args.category)
        case "summary":
            summary(args.month)
        case _:
            print("Unknown command")

if __name__ == "__main__":
    main()