                    #Personal Expense Tracker
expenses=[] #List of expenses
print("Welcome to expense tracker")

while True:
    print("-----Menu-----")
    print("1. Add expense")
    print("2. View your expenses")
    print("3. View all expenses")
    print("4. Exit ")
    choice = int(input("Enter Your choice:"))
    if choice==1:
        date=input("Enter date of expense: ")
        category=input("Enter category of expense: ")
        description=input("Enter description of expense: ")
        amount=float(input("Enter amount of expense: "))
        expense={"Date":date, "Category": category,
               "Description": description, "Amount": amount }
        expenses.append(expense)
    elif choice==2:
        if len(expenses)!=0:
            count=1
            for each_expense in expenses:
                print(f"Expense no.{count},-> Date :{each_expense['Date']}, Category: {each_expense['Category']}, Description: {each_expense['Description']}, Amount: {each_expense['Amount']}")
                count+=1
        else:
            print("There are no expenses ")
    elif choice==3:
        total=0
        for each_expense in expenses:
            total = total+ each_expense ["Amount"]
        print(f"Total expense amount is { total} ")
    elif choice==4:
        print("\nThank You")
        break
    else:
        print("\nInvalid Choice. Try Again")

