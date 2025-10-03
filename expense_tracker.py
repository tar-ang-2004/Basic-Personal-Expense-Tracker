import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple

class ExpenseTracker:
    def __init__(self, data_file='expenses.json'):
        self.data_file = data_file
        self.expenses = self.load_expenses()
        self.categories = [
            'Food & Dining',
            'Rent & Housing',
            'Transportation',
            'Entertainment',
            'Shopping',
            'Healthcare',
            'Utilities',
            'Education',
            'Insurance',
            'Savings & Investments',
            'Other'
        ]
    
    def load_expenses(self) -> List[Dict]:

        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_expenses(self):

        with open(self.data_file, 'w') as f:
            json.dump(self.expenses, f, indent=2)
    
    def add_expense(self, amount: float, category: str, description: str = "", date: str = None) -> bool:

        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        if amount <= 0:
            return False
        
        if category not in self.categories:
            category = 'Other'
        
        expense = {
            'id': len(self.expenses) + 1,
            'amount': amount,
            'category': category,
            'description': description,
            'date': date,
            'timestamp': datetime.now().isoformat()
        }
        
        self.expenses.append(expense)
        self.save_expenses()
        return True
    
    def get_expenses_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:

        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        filtered_expenses = []
        for expense in self.expenses:
            expense_date = datetime.strptime(expense['date'], '%Y-%m-%d')
            if start <= expense_date <= end:
                filtered_expenses.append(expense)
        
        return filtered_expenses
    
    def get_weekly_summary(self) -> Dict:

        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        weekly_expenses = self.get_expenses_by_date_range(
            week_start.strftime('%Y-%m-%d'),
            week_end.strftime('%Y-%m-%d')
        )
        
        return self._generate_summary(weekly_expenses, 'Weekly', week_start, week_end)
    
    def get_monthly_summary(self) -> Dict:

        today = datetime.now()
        month_start = today.replace(day=1)
        
        # Get last day of current month
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1) - timedelta(days=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1) - timedelta(days=1)
        
        monthly_expenses = self.get_expenses_by_date_range(
            month_start.strftime('%Y-%m-%d'),
            month_end.strftime('%Y-%m-%d')
        )
        
        return self._generate_summary(monthly_expenses, 'Monthly', month_start, month_end)
    
    def _generate_summary(self, expenses: List[Dict], period: str, start_date: datetime, end_date: datetime) -> Dict:

        if not expenses:
            return {
                'period': period,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'total_amount': 0,
                'total_transactions': 0,
                'category_breakdown': {},
                'daily_breakdown': {},
                'average_per_day': 0,
                'highest_expense': None,
                'expenses': []
            }
        
        total_amount = sum(expense['amount'] for expense in expenses)
        category_breakdown = defaultdict(float)
        daily_breakdown = defaultdict(float)
        
        for expense in expenses:
            category_breakdown[expense['category']] += expense['amount']
            daily_breakdown[expense['date']] += expense['amount']
        
        # Find highest expense
        highest_expense = max(expenses, key=lambda x: x['amount'])
        
        # Calculate average per day
        days_in_period = (end_date - start_date).days + 1
        average_per_day = total_amount / days_in_period if days_in_period > 0 else 0
        
        # Sort category breakdown by amount (descending) for consistent ordering
        sorted_category_breakdown = dict(sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True))
        
        return {
            'period': period,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'total_amount': round(total_amount, 2),
            'total_transactions': len(expenses),
            'category_breakdown': sorted_category_breakdown,
            'daily_breakdown': dict(daily_breakdown),
            'average_per_day': round(average_per_day, 2),
            'highest_expense': highest_expense,
            'expenses': sorted(expenses, key=lambda x: x['date'], reverse=True)
        }
    
    def get_all_expenses(self) -> List[Dict]:

        return sorted(self.expenses, key=lambda x: x['date'], reverse=True)
    
    def delete_expense(self, expense_id: int) -> bool:

        for i, expense in enumerate(self.expenses):
            if expense['id'] == expense_id:
                del self.expenses[i]
                self.save_expenses()
                return True
        return False
    
    def get_category_totals(self) -> Dict[str, float]:

        category_totals = defaultdict(float)
        for expense in self.expenses:
            category_totals[expense['category']] += expense['amount']
        return dict(category_totals)


def main():

    tracker = ExpenseTracker()
    
    print("🏦 Welcome to Personal Expense Tracker!")
    print("=" * 50)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Add new expense")
        print("2. View weekly summary")
        print("3. View monthly summary")
        print("4. View all expenses")
        print("5. View category totals")
        print("6. Delete expense")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            print("\n📝 Adding New Expense")
            print("-" * 30)
            
            try:
                amount = float(input("Enter amount: $"))
                if amount <= 0:
                    print("❌ Amount must be positive!")
                    continue
                
                print("\nSelect category:")
                for i, category in enumerate(tracker.categories, 1):
                    print(f"{i}. {category}")
                
                cat_choice = input(f"\nEnter category number (1-{len(tracker.categories)}): ").strip()
                try:
                    cat_index = int(cat_choice) - 1
                    if 0 <= cat_index < len(tracker.categories):
                        category = tracker.categories[cat_index]
                    else:
                        category = 'Other'
                        print("⚠️ Invalid category, using 'Other'")
                except ValueError:
                    category = 'Other'
                    print("⚠️ Invalid input, using 'Other'")
                
                description = input("Enter description (optional): ").strip()
                date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
                
                date = date_input if date_input else None
                
                if tracker.add_expense(amount, category, description, date):
                    print("✅ Expense added successfully!")
                else:
                    print("❌ Failed to add expense!")
                    
            except ValueError:
                print("❌ Invalid amount entered!")
        
        elif choice == '2':
            print("\n📊 Weekly Summary")
            print("-" * 30)
            summary = tracker.get_weekly_summary()
            print_summary(summary)
        
        elif choice == '3':
            print("\n📊 Monthly Summary")
            print("-" * 30)
            summary = tracker.get_monthly_summary()
            print_summary(summary)
        
        elif choice == '4':
            print("\n📋 All Expenses")
            print("-" * 30)
            expenses = tracker.get_all_expenses()
            if expenses:
                for expense in expenses[:20]:  # Show last 20 expenses
                    print(f"ID: {expense['id']} | ${expense['amount']:.2f} | {expense['category']} | {expense['date']} | {expense['description']}")
                if len(expenses) > 20:
                    print(f"\n... and {len(expenses) - 20} more expenses")
            else:
                print("No expenses found.")
        
        elif choice == '5':
            print("\n📊 Category Totals")
            print("-" * 30)
            totals = tracker.get_category_totals()
            if totals:
                for category, total in sorted(totals.items(), key=lambda x: x[1], reverse=True):
                    print(f"{category}: ${total:.2f}")
            else:
                print("No expenses found.")
        
        elif choice == '6':
            print("\n🗑️ Delete Expense")
            print("-" * 30)
            try:
                expense_id = int(input("Enter expense ID to delete: "))
                if tracker.delete_expense(expense_id):
                    print("✅ Expense deleted successfully!")
                else:
                    print("❌ Expense not found!")
            except ValueError:
                print("❌ Invalid ID entered!")
        
        elif choice == '7':
            print("\n👋 Thanks for using Personal Expense Tracker!")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")


def print_summary(summary: Dict):

    print(f"Period: {summary['period']} ({summary['start_date']} to {summary['end_date']})")
    print(f"Total Amount: ${summary['total_amount']:.2f}")
    print(f"Total Transactions: {summary['total_transactions']}")
    print(f"Average per Day: ${summary['average_per_day']:.2f}")
    
    if summary['highest_expense']:
        highest = summary['highest_expense']
        print(f"Highest Expense: ${highest['amount']:.2f} ({highest['category']}) - {highest['description']}")
    
    print("\n📊 Category Breakdown:")
    if summary['category_breakdown']:
        for category, amount in sorted(summary['category_breakdown'].items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / summary['total_amount']) * 100 if summary['total_amount'] > 0 else 0
            print(f"  {category}: ${amount:.2f} ({percentage:.1f}%)")
    else:
        print("  No expenses in this period")


if __name__ == "__main__":
    main()