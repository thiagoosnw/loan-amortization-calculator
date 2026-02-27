import streamlit as st
import pandas as pd
import io

st.title("Loan Amortization Calculator\nCreated by Thiago Alcebiades")

principal = st.number_input("Principal Amount ($)", min_value=0.0, value=5000.0)
interest_rate = st.number_input("Monthly Interest Rate (e.g., 0.05 for 5%)", min_value=0.0, value=0.05)
term = st.number_input("Term (Months)", min_value=1, value=4, step=1)

# 3. Calculate Button
if st.button("Calculate"):
    
    payment = principal * (interest_rate * (1 + interest_rate)**term) / ((1 + interest_rate)**term - 1)
    
    remaining_balance = principal
    schedule = []

    for month in range(1, int(term) + 1):
        interest_paid = remaining_balance * interest_rate
        principal_amortized = payment - interest_paid
        remaining_balance -= principal_amortized
        
        if month == term:
            remaining_balance = 0.0
            
        schedule.append({
            "Month": month,
            "Payment": round(payment, 2),
            "Interest Paid": round(interest_paid, 2),
            "Principal Amortized": round(principal_amortized, 2),
            "Remaining Balance": round(remaining_balance, 2)
        })

    df = pd.DataFrame(schedule)
    df.set_index('Month', inplace=True)
    st.write("### Amortization Schedule")
    st.dataframe(df)

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Amortization')

    st.download_button(
        label="Download as Excel",
        data=buffer.getvalue(),
        file_name="amortization_table.xlsx",
        mime="application/vnd.ms-excel"
    )
