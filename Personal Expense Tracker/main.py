import csv
import os
import matplotlib.pyplot as plt

expenses = []
income_list = []

DATA_DIR = "data" #creates a variable holding the name of the folder ("data") where we want to organize and store our financial files.
FILE_NAME = os.path.join(DATA_DIR, "expenses.csv")
INCOME_FILE = os.path.join(DATA_DIR, "income.csv")
BUDGET_FILE = os.path.join(DATA_DIR, "budget.txt")

# ---------------- SETUP ----------------
def setup_folders():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

# ---------------- LOAD DATA ----------------
def load_expenses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["Amount"] = float(row["Amount"])
                expenses.append(row)

# ---------------- SAVE DATA ----------------
def save_expenses():
    with open(FILE_NAME, "w", newline="") as file:
        fieldnames = ["Date", "Category", "Description", "Amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for exp in expenses:
            writer.writerow(exp)

# ---------------- ADD EXPENSE ----------------
def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category: ")
    description = input("Enter description: ")

    try:
        amount = float(input("Enter amount: "))
    except:
        print("Invalid amount!")
        return

    expense = {
        "Date": date,
        "Category": category,
        "Description": description,
        "Amount": amount
    }

    expenses.append(expense)
    save_expenses()
    print("Expense added successfully!")

# ---------------- EDIT EXPENSE (NEW) ----------------
def edit_expense():
    view_expenses()

    if len(expenses) == 0:
        return

    try:
        num = int(input("Enter expense number to edit: "))
    except:
        print("Invalid input!")
        return

    if num < 1 or num > len(expenses):
        print("Invalid number.")
        return

    exp = expenses[num - 1]

    print("\nLeave field blank to keep the current value.")

    new_date = input("New Date (" + exp["Date"] + "): ")
    new_category = input("New Category (" + exp["Category"] + "): ")
    new_description = input("New Description (" + exp["Description"] + "): ")
    new_amount = input("New Amount (" + str(exp["Amount"]) + "): ")

    if new_date.strip() != "":
        exp["Date"] = new_date
    if new_category.strip() != "":
        exp["Category"] = new_category
    if new_description.strip() != "":
        exp["Description"] = new_description
    if new_amount.strip() != "":
        try:
            exp["Amount"] = float(new_amount)
        except:
            print("Invalid amount, keeping old value.")

    save_expenses()
    print("Expense updated successfully!")

# ---------------- VIEW EXPENSES ----------------
def view_expenses():
    if len(expenses) == 0:
        print("No expenses found.")
        return

    count = 1
    for exp in expenses:
        print("\nExpense", count)
        print("Date:", exp["Date"])
        print("Category:", exp["Category"])
        print("Description:", exp["Description"])
        print("Amount:", exp["Amount"])
        count = count + 1

# ---------------- INCOME TRACKING (NEW) ----------------
def load_income():
    if os.path.exists(INCOME_FILE):
        with open(INCOME_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["Amount"] = float(row["Amount"])
                income_list.append(row)

def save_income():
    with open(INCOME_FILE, "w", newline="") as file:
        fieldnames = ["Date", "Source", "Amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for inc in income_list:
            writer.writerow(inc)

def add_income():
    date = input("Enter date (YYYY-MM-DD): ")
    source = input("Enter income source (Salary/Business/Other): ")

    try:
        amount = float(input("Enter amount: "))
    except:
        print("Invalid amount!")
        return

    income = {
        "Date": date,
        "Source": source,
        "Amount": amount
    }

    income_list.append(income)
    save_income()
    print("Income added successfully!")

def view_income():
    if len(income_list) == 0:
        print("No income records found.")
        return

    count = 1
    for inc in income_list:
        print("\nIncome", count)
        print("Date:", inc["Date"])
        print("Source:", inc["Source"])
        print("Amount:", inc["Amount"])
        count = count + 1

def total_income():
    total = 0
    for inc in income_list:
        total = total + inc["Amount"]
    return total

# ---------------- TOTAL + BUDGET ----------------
def total_expense():
    total = 0

    for exp in expenses:
        total = total + exp["Amount"]

    print("Total Expense:", total)

    budget = get_budget()
    if total > budget:
        print("⚠ Budget exceeded! Your budget is", budget)

# ---------------- USER-DEFINED BUDGET (NEW) ----------------
def get_budget():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as file:
            content = file.read().strip()
            if content != "":
                return float(content)
    return 5000  # default budget if user hasn't set one

def set_budget():
    try:
        budget = float(input("Enter your monthly budget: "))
    except:
        print("Invalid amount!")
        return

    with open(BUDGET_FILE, "w") as file:
        file.write(str(budget))

    print("Budget set successfully to", budget)

# ---------------- REMAINING BALANCE (NEW) ----------------
def remaining_balance():
    income_total = total_income()

    expense_total = 0
    for exp in expenses:
        expense_total = expense_total + exp["Amount"]

    balance = income_total - expense_total

    print("Total Income:", income_total)
    print("Total Expense:", expense_total)
    print("Remaining Balance:", balance)

    if balance < 0:
        print("⚠ You have spent more than your income!")

# ---------------- CATEGORY ANALYSIS ----------------
def category_analysis():
    data = get_category_totals()

    if len(data) == 0:
        print("No expenses found.")
        return

    for cat in data:
        print(cat, ":", data[cat])

    # Pie Chart
    labels = []
    values = []

    for cat in data:
        labels.append(cat)
        values.append(data[cat])

    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Expense Distribution")
    plt.show()

# ---------------- HELPER: CATEGORY TOTALS (NEW) ----------------
def get_category_totals():
    data = {}

    for exp in expenses:
        cat = exp["Category"]

        if cat in data:
            data[cat] = data[cat] + exp["Amount"]
        else:
            data[cat] = exp["Amount"]

    return data

# ---------------- BAR CHART (NEW) ----------------
def category_bar_chart():
    data = get_category_totals()

    if len(data) == 0:
        print("No expenses found.")
        return

    labels = []
    values = []

    for cat in data:
        labels.append(cat)
        values.append(data[cat])

    plt.bar(labels, values, color="skyblue")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.title("Expenses by Category")
    plt.show()

# ---------------- TOP SPENDING CATEGORY (NEW) ----------------
def top_spending_category():
    data = get_category_totals()

    if len(data) == 0:
        print("No expenses found.")
        return

    top_cat = None
    top_amount = 0

    for cat in data:
        if data[cat] > top_amount:
            top_amount = data[cat]
            top_cat = cat

    print("Top Spending Category:", top_cat, "-", top_amount)

# ---------------- LARGEST EXPENSE (NEW) ----------------
def largest_expense():
    if len(expenses) == 0:
        print("No expenses found.")
        return

    largest = expenses[0]

    for exp in expenses:
        if exp["Amount"] > largest["Amount"]:
            largest = exp

    print("Largest Expense:")
    print("Date:", largest["Date"])
    print("Category:", largest["Category"])
    print("Description:", largest["Description"])
    print("Amount:", largest["Amount"])

# ---------------- MONTHLY REPORT ----------------
def monthly_report():
    month = input("Enter month (MM): ")
    total = 0

    for exp in expenses:
        parts = exp["Date"].split("-")

        if len(parts) >= 2:
            if parts[1] == month:
                total = total + exp["Amount"]

    print("Total expense for month", month, ":", total)

# ---------------- SEARCH ----------------
def search_expense():
    keyword = input("Enter keyword to search: ").lower()
    found = False

    for exp in expenses:
        desc = exp["Description"].lower()

        if keyword in desc:
            print("\nMatch Found:")
            print("Date:", exp["Date"])
            print("Category:", exp["Category"])
            print("Description:", exp["Description"])
            print("Amount:", exp["Amount"])
            found = True

    if found == False:
        print("No matching expense found.")

# ---------------- SEARCH BY CATEGORY (NEW) ----------------
def search_by_category():
    keyword = input("Enter category to search: ").lower()
    found = False

    for exp in expenses:
        cat = exp["Category"].lower()

        if keyword in cat:
            print("\nMatch Found:")
            print("Date:", exp["Date"])
            print("Category:", exp["Category"])
            print("Description:", exp["Description"])
            print("Amount:", exp["Amount"])
            found = True

    if found == False:
        print("No matching expense found for this category.")

# ---------------- SEARCH BY DATE (NEW) ----------------
def search_by_date():
    date = input("Enter date to search (YYYY-MM-DD): ")
    found = False

    for exp in expenses:
        if exp["Date"] == date:
            print("\nMatch Found:")
            print("Date:", exp["Date"])
            print("Category:", exp["Category"])
            print("Description:", exp["Description"])
            print("Amount:", exp["Amount"])
            found = True

    if found == False:
        print("No matching expense found for this date.")

# ---------------- SORT EXPENSES (NEW) ----------------
def sort_expenses():
    if len(expenses) == 0:
        print("No expenses found.")
        return

    print("Sort by:")
    print("1. Date")
    print("2. Amount")
    print("3. Category")

    choice = input("Enter choice: ")

    if choice == "1":
        sorted_list = sorted(expenses, key=lambda exp: exp["Date"])
    elif choice == "2":
        sorted_list = sorted(expenses, key=lambda exp: exp["Amount"])
    elif choice == "3":
        sorted_list = sorted(expenses, key=lambda exp: exp["Category"])
    else:
        print("Invalid choice!")
        return

    count = 1
    for exp in sorted_list:
        print("\nExpense", count)
        print("Date:", exp["Date"])
        print("Category:", exp["Category"])
        print("Description:", exp["Description"])
        print("Amount:", exp["Amount"])
        count = count + 1

# ---------------- DELETE ----------------
def delete_expense():
    view_expenses()

    try:
        num = int(input("Enter expense number to delete: "))
    except:
        print("Invalid input!")
        return

    if num > 0 and num <= len(expenses):
        expenses.pop(num - 1)
        save_expenses()
        print("Deleted successfully!")
    else:
        print("Invalid number.")

# ---------------- MAIN ----------------
def main():
    setup_folders()
    load_expenses()
    load_income()

    while True:
        print("\n------ MENU ------")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Total Expense")
        print("6. Category Analysis (Pie Chart)")
        print("7. Category Bar Chart")
        print("8. Monthly Report")
        print("9. Search by Description")
        print("10. Search by Category")
        print("11. Search by Date")
        print("12. Sort Expenses")
        print("13. Top Spending Category")
        print("14. Largest Expense")
        print("15. Add Income")
        print("16. View Income")
        print("17. Remaining Balance")
        print("18. Set Monthly Budget")
        print("19. Exit")

        try:
            choice = int(input("Enter choice: "))
        except:
            print("Invalid input!")
            continue

        if choice == 1:
            add_expense()
        elif choice == 2:
            view_expenses()
        elif choice == 3:
            edit_expense()
        elif choice == 4:
            delete_expense()
        elif choice == 5:
            total_expense()
        elif choice == 6:
            category_analysis()
        elif choice == 7:
            category_bar_chart()
        elif choice == 8:
            monthly_report()
        elif choice == 9:
            search_expense()
        elif choice == 10:
            search_by_category()
        elif choice == 11:
            search_by_date()
        elif choice == 12:
            sort_expenses()
        elif choice == 13:
            top_spending_category()
        elif choice == 14:
            largest_expense()
        elif choice == 15:
            add_income()
        elif choice == 16:
            view_income()
        elif choice == 17:
            remaining_balance()
        elif choice == 18:
            set_budget()
        elif choice == 19:
            print("Thank you!")
            break
        else:
            print("Invalid choice!")

# Run program
if __name__ == "__main__":
    main()
