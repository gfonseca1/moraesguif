import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb

# Connect to the DuckDB database
conn = duckdb.connect("my_db.duckdb")


# Function to load data from dbt models or create sample data if not exists
def load_data(model_name):
    try:
        query = f"SELECT * FROM {model_name}"
        return pd.read_sql_query(query, conn)
    except Exception:
        st.warning(f"Table '{model_name}' not found. Using sample data.")
        if model_name == "expenses":
            return pd.DataFrame(
                {
                    "date": pd.date_range(start="2023-01-01", periods=5),
                    "category": ["Food", "Rent", "Utilities", "Entertainment", "Transport"],
                    "amount": [100, 1000, 200, 50, 75],
                }
            )
        elif model_name == "income":
            return pd.DataFrame(
                {
                    "date": pd.date_range(start="2023-01-01", periods=5),
                    "source": ["Salary", "Freelance", "Investments", "Salary", "Bonus"],
                    "amount": [3000, 500, 200, 3000, 1000],
                }
            )


# Streamlit app
def main():
    st.title("Personal Finance Dashboard")

    # Load transformed data
    expenses = load_data("expenses")
    income = load_data("income")

    # Display summary statistics
    st.header("Summary")
    total_income = income["amount"].sum()
    total_expenses = expenses["amount"].sum()
    st.metric("Total Income", f"${total_income:,.2f}")
    st.metric("Total Expenses", f"${total_expenses:,.2f}")
    st.metric("Net Savings", f"${total_income - total_expenses:,.2f}")

    # Expenses by category
    st.header("Expenses by Category")
    fig = px.pie(expenses, values="amount", names="category", title="Expense Distribution")
    st.plotly_chart(fig)

    # Income vs Expenses over time
    st.header("Income vs Expenses Over Time")
    combined = pd.concat(
        [
            expenses.groupby("date")["amount"].sum().reset_index(name="Expenses"),
            income.groupby("date")["amount"].sum().reset_index(name="Income"),
        ],
        axis=1,
    )
    combined = combined.loc[:, ~combined.columns.duplicated()].set_index("date")
    fig = px.line(combined, title="Income vs Expenses Over Time")
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
