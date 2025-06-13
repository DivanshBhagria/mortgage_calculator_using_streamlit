import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

# the code renders from top to bottom

st.title("Mortgage Repayments Calculator")

st.write("### Input Data")
col1, col2 = st.columns(2)          # if i dont want my elements to not display in a single column,, i can also use this column component  to split it up into 2 different columns
home_value = col1.number_input("Home Value", min_value=0, value=500000)        #   here we're also setting default,minimum value
deposit = col1.number_input("Deposit", min_value=0, value=100000)
interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.0, value=5.5)
loan_term = col2.number_input("Loan Term (in years)", min_value=1, value=30)

# Calculate the repayments.   (just maths)
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

# Display the repayments.
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write("### Repayments")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")       #  this metric element will make the numbers kind of pop out and a little bit bigger than i just wrote it as plain text 
col2.metric(label="Total Repayments", value=f"${total_payments:,.0f}")
col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")

# Create a data-frame with the payment schedule.
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i / 12)  # Calculate the year into the loan
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

# Display the data-frame as a chart.
st.write("### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payments_df)


# streamlit apps are easy to deploy, you can use streamlit cloud to deploy for free if you're happy with your app to be publicly visible.
# First you  need to make sure that your app is published to github because thats where streamlit is going to read the source code and then deploy it from and if you have any python dependencied , then make sure to put them all into your requirements text file as well.
# when streamit tries to deploy your app, its going to run 'pip install' on  this requirements text file.