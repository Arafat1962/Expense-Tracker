from expense import Expense
from typing import List
import calendar
import datetime

def main():
    print(f"running Expense Tracker File")
    expenseFilePath = 'expense.csv'
    budget = 2000

    # Get user to input expenses
    expense = get_user_expense()

    # Write their expense to a file
    if expense is not None:
        save_user_expense(expense, expenseFilePath)
    else:
        print(red(f'Not Saving as there were no expenses recorded'))



    # Read file and summarize expenses
    summarize_user_expense(expenseFilePath, budget)

    pass

def get_user_expense():
    print(f"Getting user expenses")
    expenseName = input('Enter your expense name: ')
    
    if expenseName.strip() == "":
        return None

    expenseAmount = float(input("Enter Expense quantity: "))
    # print(f"You entered {expenseName}, {expenseAmount}")

    maximumInvalidAttempts = 3
    invalidAttempts = 0

    expense_categories = [ 
        'Food', 'Home', 'Work', 'Fun', 'Misc'
    ]

    while True:
        print('Select a categoory : ')
        for i, category_name in enumerate(expense_categories):
            print(f'  {i+1}. {category_name}')

        value_range = f'[1 - {len(expense_categories)}]'
        try:

            categoryValue = int(input(f'Select a category ranging from {value_range}: '))

    
            if categoryValue in range(len(expense_categories)+1):
                categoryName = expense_categories[categoryValue - 1]
                newExpense = Expense(name=expenseName, category= categoryName, amount= expenseAmount)
                return newExpense
                
            else:
                print('Invalid Category. Please try again!')
                invalidAttempts += 1

            if invalidAttempts >= maximumInvalidAttempts:
                print('Maximum Invalid attempt reached')
                return None

        except:
            print('Invalid input. Please Enter a valid category')
            invalidAttempts += 1


def save_user_expense(expense: Expense, path):
    print(f'save {expense} to {path}')
    with open(path, 'a') as f:
        f.write(f'{expense.name}, {expense.category}, {expense.amount}\n')

def summarize_user_expense(path, budget):
    print(f"Summarizing Expenses")
    expenses = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            expenseName, expenseCategory, expenseAmount = line.strip().split(',')
            line_expenses = Expense(
                name = expenseName,
                category = expenseCategory,
                amount = float(expenseAmount)
            )
            # print(line_expenses)
            expenses.append(line_expenses)
    
    amount_by_category = {}

    for expense in expenses:
        key = expense.category
        
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        
        else:
            amount_by_category[key] = expense.amount

    for key, amount in amount_by_category.items():
        print(f'{blue(key)}: ${amount:.2f}')
        
    total_spent = sum([ex.amount for ex in expenses])
    print(f'The expense of this month is ${total_spent:.2f}')

    remainingBudget = budget - total_spent
    
    now = datetime.datetime.now()

    daysInMonth = calendar.monthrange(now.year, now.month)[1]

    remainingDays = daysInMonth - now.day


    print(green(f'Remaining budget is ${remainingBudget:.2f} for {remainingDays} days.'))
    

def green(text):
    return f"\033[92m{text}\033[0m"

def red(text):
    return f"\033[91m{text}\033[0m"

def blue(text):
    return f"\033[94m{text}\033[0m"





if __name__ == "__main__":
    main()
