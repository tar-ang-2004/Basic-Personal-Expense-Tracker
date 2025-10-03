# Personal Expense Tracker 

A basic personal expense tracking application built with Python and Flask. Track your daily expenses, categorize spending, and get detailed insights with beautiful charts and analytics.

## Features 

### Core Features
- **Easy Expense Entry**: Add expenses with amount, category, description, and date
- **Smart Categorization**: 11 predefined categories (Food & Dining, Rent & Housing, Transportation, etc.)
- **Real-time Analytics**: Weekly and monthly summaries with detailed breakdowns
- **Interactive Charts**: Beautiful visualizations using Chart.js
- **Search & Filter**: Find expenses by description, category, or date
- **Data Persistence**: JSON-based storage that saves all your data locally

### Web Interface
- **Modern UI**: Clean, responsive design with Bootstrap 5
- **Dashboard Overview**: Quick summary cards with key metrics
- **Detailed Reports**: Comprehensive analytics with spending trends
- **Mobile Friendly**: Works perfectly on phones and tablets
- **Quick Actions**: Fast expense entry with predefined common expenses

### Analytics & Insights
- **Weekly Summary**: Current week spending analysis
- **Monthly Reports**: Detailed monthly breakdowns with percentages
- **Category Analysis**: See where your money goes with pie charts
- **Spending Trends**: 6-month trend analysis
- **Smart Recommendations**: AI-powered insights based on your spending patterns

## Installation & Setup 

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Start

1. **Clone or download the project**
   ```bash
   cd expense-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the command-line version**
   ```bash
   python expense_tracker.py
   ```

4. **Run the web application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Go to `http://localhost:5000` to access the web interface

## Usage Guide 

### Command Line Interface

The command-line version offers a simple menu-driven interface:

```
🏦 Welcome to Personal Expense Tracker!
==================================================

What would you like to do?
1. Add new expense
2. View weekly summary
3. View monthly summary
4. View all expenses
5. View category totals
6. Delete expense
7. Exit
```

### Web Interface

#### Dashboard
- View weekly and monthly summaries at a glance
- See recent expenses and quick statistics
- Interactive category breakdown chart
- Quick action buttons for common tasks

#### Adding Expenses
- Simple form with amount, category, description, and date
- Quick-add buttons for common expenses (lunch, gas, groceries, etc.)
- Smart date defaulting to today
- Input validation to ensure data quality

#### Viewing Expenses
- Paginated list of all expenses
- Search by description
- Filter by category or date
- Sort by any column
- Delete expenses with confirmation

#### Reports & Analytics
- **Weekly Report**: Detailed weekly analysis with daily breakdown chart
- **Monthly Report**: Comprehensive monthly view with category percentages
- **Analytics**: 6-month spending trends and overall insights
- **Smart Insights**: Automated recommendations based on spending patterns

## Categories 

The app comes with 11 predefined spending categories:

1. **Food & Dining** - Restaurants, groceries, coffee, etc.
2. **Rent & Housing** - Rent, mortgage, utilities, home maintenance
3. **Transportation** - Gas, public transport, car maintenance, Uber
4. **Entertainment** - Movies, concerts, streaming services, games
5. **Shopping** - Clothes, electronics, personal items
6. **Healthcare** - Doctor visits, medications, insurance
7. **Utilities** - Electricity, water, internet, phone
8. **Education** - Books, courses, tuition, supplies
9. **Insurance** - Auto, health, life, property insurance
10. **Savings & Investments** - 401k, stocks, savings accounts
11. **Other** - Miscellaneous expenses that don't fit elsewhere

## Data Storage 

- All data is stored locally in `expenses.json`
- JSON format makes it easy to backup and transfer
- No external database required
- Automatic backup creation on each save

## Technical Details 🔧

### Backend (Flask)
- **Framework**: Flask 2.3.3
- **Storage**: JSON file-based storage
- **API Endpoints**: RESTful APIs for expense management
- **Data Processing**: Real-time analytics calculation

### Frontend
- **Framework**: Bootstrap 5.1.3
- **Charts**: Chart.js for interactive visualizations
- **Icons**: Font Awesome 6.0
- **Responsive**: Mobile-first design approach

### File Structure
```
expense-tracker/
├── app.py                 # Flask web application
├── expense_tracker.py     # Core logic and CLI interface
├── requirements.txt       # Python dependencies
├── expenses.json         # Data storage (created automatically)
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Dashboard page
│   ├── add_expense.html  # Add expense form
│   ├── expenses.html     # View all expenses
│   └── reports.html      # Analytics and reports
└── README.md            # This file
```

## Example Data Flow 

1. **Add Expense**: User enters $12.50 for "Lunch" in "Food & Dining" category
2. **Data Storage**: Expense saved to JSON with unique ID and timestamp
3. **Analytics Update**: Weekly/monthly summaries recalculated automatically
4. **Dashboard Update**: New expense appears in recent expenses list
5. **Reports Update**: Category breakdown and trends charts updated

## Tips for Better Tracking 

1. **Daily Entry**: Add expenses immediately after making them
2. **Detailed Descriptions**: Use specific descriptions for better insights
3. **Correct Categories**: Choose the most appropriate category
4. **Regular Review**: Check weekly and monthly reports regularly
5. **Set Goals**: Use insights to identify areas for spending reduction

## Future Enhancements 

- Budget setting and tracking
- Expense goals and alerts
- Data export to CSV/Excel
- Multi-currency support
- Receipt photo attachments
- Recurring expense templates
- Advanced filtering and search
- Spending predictions using machine learning

## Troubleshooting 

### Common Issues

**"Module not found" errors**
```bash
pip install -r requirements.txt
```

**Permission errors on Windows**
```bash
python -m pip install -r requirements.txt
```

**Port already in use**
```bash
# The Flask app runs on port 5000 by default
# Change the port in app.py if needed:
app.run(debug=True, port=5001)
```

**Data not persisting**
- Check if the script has write permissions in the directory
- Ensure the `expenses.json` file is not read-only

### Data Backup

To backup your expenses:
1. Copy the `expenses.json` file to a safe location
2. The file contains all your expense data in JSON format

To restore expenses:
1. Replace the `expenses.json` file with your backup
2. Restart the application

## Contributing 

This is a personal project, but suggestions and improvements are welcome! 

## Support 

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the code comments for technical details
3. Test with the command-line interface first to isolate issues
