from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from expense_tracker import ExpenseTracker
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure key in production

# Initialize the expense tracker
tracker = ExpenseTracker()

@app.route('/')
def index():

    weekly_summary = tracker.get_weekly_summary()
    monthly_summary = tracker.get_monthly_summary()
    recent_expenses = tracker.get_all_expenses()[:5]  # Last 5 expenses
    category_totals = tracker.get_category_totals()
    
    return render_template('index.html', 
                         weekly_summary=weekly_summary,
                         monthly_summary=monthly_summary,
                         recent_expenses=recent_expenses,
                         category_totals=category_totals)

@app.route('/add_expense', methods=['GET', 'POST'])

def add_expense():

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            category = request.form['category']
            description = request.form.get('description', '')
            date = request.form.get('date', '')
            
            if not date:
                date = None
            
            if tracker.add_expense(amount, category, description, date):
                flash('Expense added successfully!', 'success')
            else:
                flash('Failed to add expense. Please check your input.', 'error')
                
        except ValueError:
            flash('Invalid amount entered!', 'error')
        
        return redirect(url_for('add_expense'))
    
    return render_template('add_expense.html', categories=tracker.categories)

@app.route('/expenses')

def view_expenses():

    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    all_expenses = tracker.get_all_expenses()
    total = len(all_expenses)
    
    start = (page - 1) * per_page
    end = start + per_page
    expenses = all_expenses[start:end]
    
    has_prev = page > 1
    has_next = end < total
    
    return render_template('expenses.html', 
                         expenses=expenses,
                         page=page,
                         has_prev=has_prev,
                         has_next=has_next,
                         total=total)

@app.route('/reports')

def reports():

    weekly_summary = tracker.get_weekly_summary()
    monthly_summary = tracker.get_monthly_summary()
    category_totals = tracker.get_category_totals()
    
    return render_template('reports.html',
                         weekly_summary=weekly_summary,
                         monthly_summary=monthly_summary,
                         category_totals=category_totals)

@app.route('/api/delete_expense/<int:expense_id>', methods=['POST'])

def delete_expense(expense_id):

    if tracker.delete_expense(expense_id):
        return jsonify({'success': True, 'message': 'Expense deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Expense not found'}), 404

@app.route('/api/category_data')

def category_data():

    category_totals = tracker.get_category_totals()
    
    # Prepare data for chart
    labels = list(category_totals.keys())
    data = list(category_totals.values())
    
    return jsonify({
        'labels': labels,
        'data': data
    })

@app.route('/api/monthly_trend')

def monthly_trend():

    # Get last 6 months of data
    import calendar
    from datetime import date, timedelta
    
    trend_data = []
    today = date.today()
    
    for i in range(5, -1, -1):  # Last 6 months
        if today.month - i > 0:
            month = today.month - i
            year = today.year
        else:
            month = today.month - i + 12
            year = today.year - 1
        
        # Get first and last day of month
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)
        
        # Get expenses for this month
        month_expenses = tracker.get_expenses_by_date_range(
            first_day.strftime('%Y-%m-%d'),
            last_day.strftime('%Y-%m-%d')
        )
        
        total = sum(expense['amount'] for expense in month_expenses)
        month_name = calendar.month_name[month]
        
        trend_data.append({
            'month': f"{month_name} {year}",
            'total': total
        })
    
    return jsonify(trend_data)

if __name__ == '__main__':
    app.run(debug=True)