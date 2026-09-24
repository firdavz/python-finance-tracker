# Expense Tracker
# simple finance tracker, I made it to learn backend with Python (Flask)

import csv
import io
import json
import os
from datetime import date

from flask import Flask, render_template, request, redirect, url_for, Response

app = Flask(__name__)

# all expenses are saved in this file, no database for now
DATA_FILE = os.path.join(os.path.dirname(__file__), "expenses.json")

categories = ["Food", "Transport", "Rent", "Utilities", "Health",
              "Entertainment", "Education", "Business", "Other"]

# colors for the pie chart, I picked them by hand
colors = {
    "Food": "#36a2eb",
    "Transport": "#ff6384",
    "Rent": "#9966ff",
    "Utilities": "#ff9f40",
    "Health": "#4bc0c0",
    "Entertainment": "#ffcd56",
    "Education": "#a3e635",
    "Business": "#f472b6",
    "Other": "#94a3b8",
}


def load_expenses():
    # if the file is not created yet we just start with empty list
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)


def filter_expenses(expenses, start, end, category):
    result = []
    for e in expenses:
        # dates are saved like "2025-09-25" so I can compare them as strings
        if start and e["date"] < start:
            continue
        if end and e["date"] > end:
            continue
        if category != "All" and e["category"] != category:
            continue
        result.append(e)
    return result


def get_total(expenses):
    total = 0
    for e in expenses:
        total += e["amount"]
    return total


def get_filters():
    # filters come from the url, for example /?start=2025-09-01&category=Food
    start = request.args.get("start", "")
    end = request.args.get("end", "")
    category = request.args.get("category", "All")
    return start, end, category


@app.route("/")
def index():
    start, end, category = get_filters()
    error = request.args.get("error", "")

    expenses = load_expenses()
    filtered = filter_expenses(expenses, start, end, category)
    filtered.sort(key=lambda e: e["date"], reverse=True)  # newest first

    total = get_total(filtered)

    # data for the charts, the drawing itself is done in script.js
    # pie chart: total per category (same order as categories list)
    pie_labels = []
    pie_values = []
    pie_colors = []
    for c in categories:
        amount = 0
        for e in filtered:
            if e["category"] == c:
                amount += e["amount"]
        if amount > 0:
            pie_labels.append(c)
            pie_values.append(amount)
            pie_colors.append(colors[c])

    # bar chart: total per day
    by_date = {}
    for e in filtered:
        if e["date"] in by_date:
            by_date[e["date"]] += e["amount"]
        else:
            by_date[e["date"]] = e["amount"]
    bar_labels = sorted(by_date)
    bar_values = []
    for day in bar_labels:
        bar_values.append(by_date[day])

    chart_data = {
        "pie_labels": pie_labels,
        "pie_values": pie_values,
        "pie_colors": pie_colors,
        "bar_labels": bar_labels,
        "bar_values": bar_values,
    }

    return render_template(
        "index.html",
        expenses=filtered,
        total=total,
        categories=categories,
        chart_data=chart_data,
        start=start,
        end=end,
        category=category,
        today=str(date.today()),
        error=error,
    )


@app.route("/add", methods=["POST"])
def add_expense():
    description = request.form.get("description", "").strip()
    amount = request.form.get("amount", "")
    day = request.form.get("date", "")
    category = request.form.get("category", "Other")

    # checking inputs again on the server
    # (the browser checks too but someone can skip that)
    if description == "":
        return redirect(url_for("index", error="Please write a description"))
    try:
        amount = float(amount)
    except ValueError:
        return redirect(url_for("index", error="Amount must be a number"))
    if amount <= 0:
        return redirect(url_for("index", error="Please enter a positive number"))
    if day == "":
        day = str(date.today())
    if category not in categories:
        category = "Other"

    expenses = load_expenses()

    # at first I used len(expenses) + 1 for id but after deleting
    # two expenses could get the same id, so now I take biggest id + 1
    new_id = 1
    for e in expenses:
        if e["id"] >= new_id:
            new_id = e["id"] + 1

    expense = {
        "id": new_id,
        "description": description,
        "amount": amount,
        "date": day,
        "category": category,
    }
    expenses.append(expense)
    save_expenses(expenses)

    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    expenses = load_expenses()
    new_list = []
    for e in expenses:
        if e["id"] != expense_id:
            new_list.append(e)
    save_expenses(new_list)
    return redirect(url_for("index"))


@app.route("/export")
def export_csv():
    # exports only what you see with the current filter
    start, end, category = get_filters()
    filtered = filter_expenses(load_expenses(), start, end, category)
    filtered.sort(key=lambda e: e["date"])

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Description", "Category", "Amount"])
    for e in filtered:
        writer.writerow([e["date"], e["description"], e["category"], f"{e['amount']:.2f}"])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=expenses.csv"},
    )


if __name__ == "__main__":
    # debug=True so the server restarts by itself when I change the code
    app.run(debug=True)
