# Finance Tracker

A web-based expense tracker built with **Python and Flask**. Users can log expenses, filter them by date range and category, see spending in charts, and export the filtered data to CSV.

The goal of this project was to learn server-side web development: routing, handling forms, rendering templates, saving data, and validating input.

## Features

- **Add and delete expenses** with a description, amount, date and category
- **Filter** by start date, end date and category
- **Running total** for the current filter
- **Charts:** spending by category (pie) and spending over time (bar)
- **CSV export** of exactly what the current filter shows
- **Server-side validation** of every form field (required, numeric, positive, known category)
- **Responsive dark UI** that stacks into a single column on small screens

## Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Backend  | Python 3, Flask                     |
| Frontend | HTML (Jinja2 templates), CSS, JavaScript |
| Charts   | Chart.js                            |
| Storage  | JSON file                           |

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/firdavz/python-finance-tracker.git
cd python-finance-tracker

# optional: create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

### Run

```bash
python financeapp.py
```

Then open **http://127.0.0.1:5000** in your browser.

`expenses.json` is created automatically the first time you add an expense.

## Project Structure

```
python-finance-tracker/
├── financeapp.py        # Flask app: routes, validation, persistence, chart data
├── templates/
│   └── index.html       # Dashboard (Jinja2 template)
├── static/
│   ├── style.css        # Layout and dark theme
│   └── script.js        # Chart rendering and delete confirmation
└── requirements.txt
```

## Routes

| Method | Route          | Description                                                      |
|--------|----------------|------------------------------------------------------------------|
| GET    | `/`            | Dashboard. Optional query params: `start`, `end`, `category`     |
| POST   | `/add`         | Validates the form and creates an expense                        |
| POST   | `/delete/<id>` | Deletes an expense by id                                         |
| GET    | `/export`      | Downloads filtered expenses as CSV (same query params as `/`)    |

## Data Model

Each expense is stored as one object in `expenses.json`:

```json
{
    "id": 1,
    "description": "Lunch",
    "amount": 12.5,
    "date": "2025-09-25",
    "category": "Food"
}
```

Categories: Food, Transport, Rent, Utilities, Health, Entertainment, Education, Business, Other.

## Design Decisions

- **Post/Redirect/Get.** Every POST request ends with a redirect. Refreshing the page after adding or deleting never resubmits the form.
- **Filters live in the URL.** Filtering uses GET query parameters, so any filtered view can be bookmarked or shared. The CSV export reuses the same parameters, so it always matches what is on screen.
- **ISO dates.** Dates are stored as `YYYY-MM-DD` strings, so date-range filtering is a simple string comparison with no parsing.
- **Validation on the server.** The HTML form checks input in the browser, but the backend validates everything again, because requests can be sent without using the form.
- **Safe ids.** A new id is the current highest id plus one, not `len(list) + 1`, so ids stay unique after deletions.
- **Safe output.** Jinja2 escapes user input when rendering, and chart data is passed to JavaScript with `tojson`.
- **Charts are prepared in Python.** Totals per category and per day are calculated on the backend; JavaScript only draws them.

## Known Limitations

This is a learning project, and these trade-offs were made on purpose:

- **JSON file storage** is not safe when several requests write at the same time. A real deployment would use a database.
- **No login.** All data is shared by anyone who opens the app.
- **No CSRF protection** on the forms.
- **Debug mode is on** in `financeapp.py`. It must be turned off for production.
- **Charts need internet**, because Chart.js is loaded from a CDN.

## Roadmap

- [ ] Move storage to SQLite
- [ ] Add unit tests with pytest
- [ ] Edit existing expenses
- [ ] Track income as well as expenses
- [ ] User accounts and CSRF protection (Flask-Login, Flask-WTF)
