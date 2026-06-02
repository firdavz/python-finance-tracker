import json
from datetime import date
print("== == == == == == == == == == == == == == == ==")
print("Personal finance tracker ")
print("== == == == == == == == == == == == == == == ==")

records = []

savings = 0
expenses = 0
net_profit = 0

try:
   with open("fina.json", "r") as f:
      records = json.load(f)
except : records = []

def save_records():
    with open("fina.json", "w") as f:
        json.dump(records, f)

money = {}

def get_amount(prompt):
  while True:
    try:
        amount = float(input(prompt))
        if amount <= 0 :
            print("Please enter a positive number")
            continue
        return amount
    except ValueError:
        print("Please enter a valid number! ")


savings_category = ["salary","gift","cashback","sold item","other"]

def m_savings():
    while True:
        try:
            category = int(input(" Categories : \n 1- salary\n 2- gift \n 3- cashback \n 4-sold item \n 5- other \n Please choose a category (only numbers) : "))
            if category <=0 or category > len(savings_category):
                print("Please enter a valid number! ")
                continue
            amount = get_amount("Please enter your saving : ")
            note = input("You can leave a note: ")
            choice = category - 1
            selected_category = savings_category[choice]
            return selected_category, amount,note
        except ValueError:
            print("Please enter a valid number! ")


expense_category =["food","rent","transport","shopping","other"]

def m_expense():
    while True:
        try:
            category = int(input(" Categories : \n 1- food\n 2- rent \n 3- transport \n 4-shopping \n 5- other \n Please choose a category (only numbers) : "))
            if category <= 0 or category >len(expense_category):
                print("Please enter a valid number! ")
                continue
            amount = get_amount("Please enter your expense : ")
            note1 = input("You can leave a note: ")
            choice = category - 1
            selected_category = expense_category[choice]
            return selected_category, amount,note1
        except ValueError:
            print("Please enter a valid number! ")

def get_today():
    return str(date.today())


def view_summary():
    savings = 0
    expenses = 0
    net_profit = 0
    for entry in records:
        if entry["type"] == "saving":
            savings += entry["amount"]
    for entry in records:
        if entry["type"] == "expense":
            expenses += entry["amount"]
    net_profit = savings - expenses
    print(f"Your total savings are {savings:.2f} UZS ")
    print(f"Your total expenses are {expenses:.2f} UZS ")
    print(f"Your total net balance is {net_profit:.2f} UZS ")


def view_entries():
    is_running = True
    while is_running:
        user =  input("What are you looking for ? (saving or expense) or (exit): ").lower().strip()
        if user == "saving":
            for entry in records:
                if entry["type"] == user:
                   print(entry)

        elif user == "expense":
            for entry in records:
                if entry["type"] == user:
                    print(entry)

        elif user == "exit":
            is_running = False
        else:
            print("Please enter a valid choice! ")


def exit_app():
    save_records()
    print("Thank you for using Finance App")
    exit()




def  main():
    is_working = True
    while is_working:

        print("1.Add Savings")
        print("2.Add Expense")
        print("3.View summary")
        print("4.View Entries (date/category)")
        print("5.Exit")
        user = input("Please choose a number (1-5): ").strip()
        if user == "1":


            selected_category, amount, note = m_savings()
            money = {"type": "saving",
                     "category": selected_category,
                     "amount" : amount,
                     "note" : note,
                     "day": get_today()}

            records.append(money)
            save_records()

        elif user == "2":
            selected_category , amount, note2  = m_expense()
            money = {"type": "expense",
                     "category": selected_category,
                     "amount" : amount,
                     "note" : note2,
                     "day": get_today()}

            records.append(money)
            save_records()

        elif user == "3":
            view_summary()


        elif user == "4":
            view_entries()


        elif user == "5":
            exit_app()
            is_working = False

        else:
            print("Wrong input ! ")
            print("Please choose a number (1-5)")


main()


