
try:
    import streamlit as st
    import matplotlib.pyplot as plt
    import pandas as pd
except ImportError as e:
    print(f"Error importing required modules: {e}")
    raise e

# Configure the page
st.set_page_config(
    page_title="My Accessible Budget Helper",
    page_icon="💰",
    layout="centered"
)

# Inject Custom CSS for visual accessibility (huge text, extreme high contrast, dark-mode readable)
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-size: 32px !important;
        color: #000000 !important;
    }
    h1 {
        font-size: 52px !important;
        color: #FFD700 !important;
        background-color: #000000 !important;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 5px solid #FFFFFF !important;
        font-weight: 900 !important;
        margin-bottom: 30px !important;
    }
    h2 {
        font-size: 42px !important;
        color: #FFFFFF !important;
        background-color: #002D62 !important;
        padding: 15px;
        border-radius: 10px;
        border: 4px solid #FFFFFF !important;
        font-weight: 900 !important;
        margin-top: 30px !important;
        margin-bottom: 20px !important;
    }
    h3 {
        font-size: 36px !important;
        color: #FFFFFF !important;
        background-color: #385723 !important;
        padding: 15px;
        border-radius: 10px;
        border: 4px solid #FFFFFF !important;
        font-weight: 900 !important;
        margin-top: 25px !important;
        margin-bottom: 15px !important;
    }
    /* Force numeric/text inputs to have an extremely high-contrast light background and dark text */
    .stNumberInput div div input, .stTextInput div div input {
        font-size: 36px !important;
        height: 80px !important;
        font-weight: 900 !important;
        color: #000000 !important;
        background-color: #FFFFFF !important; /* Force clean white background */
        border: 4px solid #002D62 !important;     /* High-contrast border color */
    }
    .budget-card {
        background-color: #FFFFFF !important;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        border: 5px solid #002D62 !important;
        box-shadow: 4px 4px 0px #000000;
    }
    .budget-card strong {
        font-size: 34px !important;
        color: #000000 !important;
        font-weight: 900 !important;
        display: block;
    }
    .budget-amount {
        font-size: 40px !important;
        color: #002D62 !important;
        font-weight: 900 !important;
        display: block;
        margin-top: 10px;
        margin-bottom: 5px;
        background-color: #FFF2CC;
        padding: 5px 10px;
        border-radius: 5px;
        border: 2px solid #D66000;
    }
    .savings-card {
        background-color: #FFFFFF !important;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        border: 5px solid #385723 !important;
        box-shadow: 4px 4px 0px #000000;
    }
    .tracker-card {
        background-color: #FFFFFF !important;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        border: 5px solid #4B0082 !important;
        box-shadow: 4px 4px 0px #000000;
    }
    .info-card {
        background-color: #FFFFFF !important;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        border: 5px solid #D66000 !important;
        font-size: 28px !important;
        color: #000000 !important;
        box-shadow: 4px 4px 0px #000000;
    }
</style>
""", unsafe_allow_html=True)

st.title("💰 My Easy Budget Tracker")
st.write("Welcome! This app helps you manage your money easily. You can set your starting balance and track your monthly income below.")

st.markdown("---")

# Balance and Income Input Section
st.header("1. Your Bank Account Setup")

col_bal1, col_bal2 = st.columns(2)
with col_bal1:
    starting_balance = st.number_input(
        "Starting Account Balance ($):",
        min_value=0.0,
        value=150.00,
        step=10.0,
        help="How much money you already have in your account right now."
    )
with col_bal2:
    base_income = 662.00
    current_income = st.number_input(
        "Monthly Income ($):",
        min_value=0.0,
        value=base_income,
        step=10.0,
        help="The money you receive each month from Social Security or other sources."
    )

total_funds = starting_balance + current_income
st.markdown(f"""<div class='info-card' style='border-color: #228B22;'>
    <strong style='font-size: 30px; color: #228B22;'>💵 Total Available Funds: ${total_funds:.2f}</strong><br>
    (Starting Balance of ${starting_balance:.2f} + Monthly Income of ${current_income:.2f})
</div>""", unsafe_allow_html=True)

# Compute dynamic scaling ratio based on base recommendation
scale_factor = current_income / base_income if base_income > 0 else 0

# Original allocations scaled to current income
gym = 109.95 * scale_factor
phone = 84.27 * scale_factor
water = 52.64 * scale_factor
electric = 42.67 * scale_factor
savings = 100.00 * scale_factor
food = 225.00 * scale_factor
buffer = current_income - (gym + phone + water + electric + savings + food)

st.markdown("---")

# Recommendations displaying
st.header("2. Your Recommended Budget & Due Dates")
st.write("💡 *Not sure what these mean? Hover over or tap the boxes for simple explanations! You can customize due dates below.*")

# Customizable Due Dates
col_date1, col_date2 = st.columns(2)
with col_date1:
    gym_due = st.text_input("💪 Gym Bill Due Date:", value="5th of every month")
    phone_due = st.text_input("📱 Phone Bill Due Date:", value="12th of every month")
    water_due = st.text_input("💧 Water Bill Due Date:", value="18th of every month")
with col_date2:
    electric_due = st.text_input("⚡ Electric Bill Due Date:", value="22nd of every month")
    food_due = st.text_input("🍎 Groceries Frequency:", value="Every Saturday")

st.markdown("### Your Monthly Allocations")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""<div class='budget-card' title='This is your money for eating.'>
        <strong>🍎 Food & Groceries</strong>
        <span class='budget-amount'>${food:.2f}</span>
        <span style='font-size: 26px; color: #000000; font-weight: 900;'>When: {food_due}</span><br>
        <span style='font-size: 24px; color: #555555;'>Weekly limit: ${food/4:.2f}</span>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class='budget-card' title='Your monthly gym membership fee.'>
        <strong>💪 Gym Membership</strong>
        <span class='budget-amount'>${gym:.2f}</span>
        <span style='font-size: 26px; color: #000000; font-weight: 900;'>Due: {gym_due}</span>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class='budget-card' title='Your mobile connection plan.'>
        <strong>📱 Phone Bill</strong>
        <span class='budget-amount'>${phone:.2f}</span>
        <span style='font-size: 26px; color: #000000; font-weight: 900;'>Due: {phone_due}</span>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class='budget-card' title='Estimated cost for home water usage.'>
        <strong>💧 Water Bill</strong>
        <span class='budget-amount'>${water:.2f}</span>
        <span style='font-size: 26px; color: #000000; font-weight: 900;'>Due: {water_due}</span>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class='budget-card' title='Estimated cost for electricity.'>
        <strong>⚡ Electric Bill</strong>
        <span class='budget-amount'>${electric:.2f}</span>
        <span style='font-size: 26px; color: #000000; font-weight: 900;'>Due: {electric_due}</span>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class='budget-card' title='Leftover buffer.'>
        <strong>🛡️ Leftover Buffer</strong>
        <span class='budget-amount'>${buffer:.2f}</span>
        <span style='font-size: 26px; color: #000000; font-weight: 900;'>Use only when needed</span>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# Dynamic Money / Payment Tracker Section
st.header("📈 Interactive Money & Payment Tracker")
st.write("Check off your monthly expenses once you pay them to stay on track!")

if 'paid_status' not in st.session_state:
    st.session_state['paid_status'] = {
        'Food': False,
        'Gym': False,
        'Phone': False,
        'Water': False,
        'Electric': False,
        'Savings': False
    }

col_track1, col_track2 = st.columns(2)
with col_track1:
    st.write("**Mark as Paid:**")
    st.session_state['paid_status']['Food'] = st.checkbox(f"🍎 Food (${food:.2f})", value=st.session_state['paid_status']['Food'])
    st.session_state['paid_status']['Gym'] = st.checkbox(f"💪 Gym (${gym:.2f})", value=st.session_state['paid_status']['Gym'])
    st.session_state['paid_status']['Phone'] = st.checkbox(f"📱 Phone (${phone:.2f})", value=st.session_state['paid_status']['Phone'])

with col_track2:
    st.session_state['paid_status']['Water'] = st.checkbox(f"💧 Water (${water:.2f})", value=st.session_state['paid_status']['Water'])
    st.session_state['paid_status']['Electric'] = st.checkbox(f"⚡ Electric (${electric:.2f})", value=st.session_state['paid_status']['Electric'])
    st.session_state['paid_status']['Savings'] = st.checkbox(f"⭐ Savings (${savings:.2f})", value=st.session_state['paid_status']['Savings'])

# Calculate totals
total_bills = gym + phone + water + electric + savings + food
paid_amount = 0
if st.session_state['paid_status']['Food']: paid_amount += food
if st.session_state['paid_status']['Gym']: paid_amount += gym
if st.session_state['paid_status']['Phone']: paid_amount += phone
if st.session_state['paid_status']['Water']: paid_amount += water
if st.session_state['paid_status']['Electric']: paid_amount += electric
if st.session_state['paid_status']['Savings']: paid_amount += savings

remaining_bills = total_bills - paid_amount
current_account_balance = total_funds - paid_amount

st.markdown(f"""<div class='tracker-card'>
    <strong style='font-size: 30px; color: #4B0082;'>📊 Account & Spending Progress:</strong><br>
    • <strong>Starting Funds (Balance + Income):</strong> ${total_funds:.2f}<br>
    • <span style='color: #228B22;'>Total Paid Out So Far:</span> ${paid_amount:.2f}<br>
    • <span style='color: #4B0082; font-weight: bold;'>Actual Money Left in Account:</span> ${current_account_balance:.2f}<br>
    • <span style='color: #B22222;'>Unpaid Bills Remaining:</span> ${remaining_bills:.2f}
</div>""", unsafe_allow_html=True)

# Paid vs Remaining Bar Chart
st.write("### Progress Chart (Paid vs Remaining)")
fig2, ax2 = plt.subplots(figsize=(8, 4))

# High contrast green and crimson bars
categories = ['Paid Out', 'Remaining in Bank']
amounts = [paid_amount, current_account_balance]
colors2 = ['#228B22', '#4B0082']

bars = ax2.barh(categories, amounts, color=colors2, edgecolor='#000000', height=0.5, linewidth=3)
ax2.set_xlabel('Amount ($)', fontsize=18, fontweight='bold', color='#000000')
ax2.tick_params(axis='both', which='major', labelsize=18, labelcolor='#000000')
ax2.xaxis.grid(True, linestyle='--', alpha=0.6, color='#000000')

# Add labels to bars
for bar in bars:
    width = bar.get_width()
    ax2.text(width + 5, bar.get_y() + bar.get_height()/2, f'${width:.2f}',
             va='center', ha='left', fontsize=18, fontweight='bold', color='#000000')

fig2.patch.set_facecolor('#ffffff')
ax2.set_facecolor('#ffffff')
plt.tight_layout()
st.pyplot(fig2)

st.markdown("---")

# Visual Budget Chart Section
st.header("📊 Your Monthly Budget Distribution")
st.write("This pie chart shows how your monthly income is divided.")

if current_income > 0:
    labels = ['Food', 'Gym', 'Phone', 'Water', 'Electric', 'Savings', 'Buffer']
    sizes = [food, gym, phone, water, electric, savings, max(0, buffer)]
    colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#B19CD9', '#FFD700', '#A1CAF1']

    fig, ax = plt.subplots(figsize=(10, 10))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        textprops=dict(size=22, weight="bold", color="#000000")
    )
    for autotext in autotexts:
        autotext.set_fontsize(20)
        autotext.set_color('#000000')
    fig.patch.set_facecolor('#ffffff')
    ax.axis('equal')
    st.pyplot(fig)
else:
    st.write("Please enter an income above $0 to view your chart.")

st.markdown("---")

# Savings Section with simple math breakdown
st.header("3. Future Savings Impact")

st.markdown(f"""<div class='savings-card'>
    <h3 style='color: #FFFFFF; font-weight: 900;'>⭐ Monthly Savings Goal: ${savings:.2f}</h3>
    <p style='font-size: 28px; color: #000000;'><strong>🧮 How the math works:</strong></p>
    <p style='font-size: 26px; margin-left: 20px; color: #000000;'>
        • 1 Year has 12 months.<br>
        • If you save <strong>${savings:.2f}</strong> every month:<br>
        &nbsp;&nbsp;<em>${savings:.2f} × 12 months = <strong style='font-size: 32px; color: #228B22;'>${savings * 12:,.2f}</strong> saved!</em>
    </p>
    <p style='font-size: 26px; margin-left: 20px; color: #000000;'>
        • If you do not touch your monthly buffer (<strong>${buffer:.2f}</strong>):<br>
        &nbsp;&nbsp;<em>${buffer:.2f} × 12 months = <strong style='font-size: 32px; color: #228B22;'>${buffer * 12:,.2f}</strong> extra buffer!</em>
    </p>
</div>""", unsafe_allow_html=True)

st.markdown("---")

# Helpful Resources & Info
st.header("📚 Helpful Information & Resources")

st.markdown("""<div class='info-card'>
    <strong style='font-size: 30px; color: #D66000;'>💡 Financial Glossary (Made Simple):</strong><br><br>
    • <strong>Starting Balance:</strong> The total money already sitting in your bank account before any new income comes in.<br><br>
    • <strong>Budget:</strong> A plan showing how much money you have and how you spend it.<br><br>
    • <strong>Savings:</strong> Money you keep in a safe place (like a bank account) to use in the future.<br><br>
    • <strong>Buffer / Emergency Fund:</strong> Extra money kept for unexpected events, like a phone screen repair or doctor visit.
</div>""", unsafe_allow_html=True)

st.write("Here are some helpful links you can visit to learn more about managing money:")
st.markdown("- 🔗 [Social Security Administration (SSA) Updates](https://www.ssa.gov) - Track your benefits.")
st.markdown("- 🔗 [MyMoney.gov](https://www.mymoney.gov) - Fun and simple guides to understanding money.")
st.markdown("- 🔗 [Hands on Banking](https://handsonbanking.org) - Interactive resources for learning financial basics.")
