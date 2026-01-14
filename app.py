import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="NestWorth - UX Prototype",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal CSS for faster loading
st.markdown("""
<style>
    .stButton button {border-radius: 8px;}
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# DISCLAIMER BANNER
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; margin-bottom: 30px; border: 3px solid #5a67d8;'>
    <h2 style='color: white; margin: 0 0 15px 0; text-align: center;'>🎨 Interactive UX Prototype & Design Showcase</h2>
    <div style='background-color: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 10px; color: #2d3748;'>
        <p style='margin: 0 0 15px 0; font-size: 16px; line-height: 1.6;'>
            <strong>📋 What This Is:</strong> This is a <strong>non-functional prototype</strong> designed to showcase UI/UX concepts, 
            interactive elements, and visual design patterns for the NestWorth budgeting application.
        </p>
        <p style='margin: 0 0 15px 0; font-size: 16px; line-height: 1.6;'>
            <strong>🧩 Think of This As:</strong> A LEGO instruction manual! Each section demonstrates different components 
            (buttons, graphs, dropdowns, charts, filters) that <em>could be implemented</em> in the actual application. 
            These are examples and inspiration—not strict requirements.
        </p>
        <p style='margin: 0 0 0 0; font-size: 16px; line-height: 1.6;'>
            <strong>💡 Purpose:</strong> Explore different pages to see visual examples of: data visualization techniques, 
            interactive controls, forecasting interfaces, scenario planning tools, and budget management layouts. 
            Use these ideas to guide your implementation decisions!
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🏠 NestWorth")
st.sidebar.markdown("---")

# Sidebar disclaimer
st.sidebar.info("💡 **Prototype Mode**: This is a design showcase. All data is mock/simulated.")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Transactions", "Savings Funds", "Cash on Hand", "Budget", "Forecasting", "Balance History"]
)

# Mock data
@st.cache_data
def get_mock_transactions():
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    return pd.DataFrame({
        'Date': dates,
        'Description': ['United Airlines', 'Walmart', 'Shell Gas', 'Netflix', 'Starbucks'] * 6,
        'Amount': [-450, -120, -45, -15.99, -6.50] * 6,
        'Category': ['Travel', 'Groceries', 'Fuel', 'Entertainment', 'Dining out'] * 6,
        'Account': ['Tutorial Credit Card', 'Debit Card', 'Credit Card', 'Credit Card', 'Debit Card'] * 6
    })

@st.cache_data
def get_savings_funds():
    return [
        {
            'name': 'Car Maintenance Fund',
            'balance': 0,
            'goal': 7000,
            'monthly_contribution': 7000,
            'categories': ['Car Insurance', 'Rent']
        },
        {
            'name': 'Emergency Fund',
            'balance': 1200,
            'goal': None,
            'monthly_contribution': 0,
            'categories': []
        },
        {
            'name': 'Future Investments',
            'balance': 500,
            'goal': None,
            'monthly_contribution': 0,
            'categories': []
        }
    ]

# =======================
# DASHBOARD PAGE (Combined Overview)
# =======================
if page == "Dashboard":
    st.title("🏠 Dashboard Overview")
    
    # Top section: Current Status + Forecast Preview side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Current Month Status")
        st.markdown("""
        <div style='background-color: #e8f4f8; padding: 20px; border-radius: 10px; margin-bottom: 15px;'>
            <p style='color: gray; margin: 0;'>Cash on Hand</p>
            <h2 style='margin: 5px 0;'>$5,500.00</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Current budget status
        st.markdown("**Budget Status**")
        current_spend = 790
        budget = 750
        
        progress = (current_spend / budget)
        color = "#f44336" if progress > 1 else "#4caf50"
        
        st.markdown(f"""
        <div style='background-color: #f0f0f0; border-radius: 10px; height: 30px; position: relative; overflow: hidden; margin-bottom: 10px;'>
            <div style='background-color: {color}; height: 100%; width: {min(progress * 100, 100)}%;'></div>
            <div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 14px; font-weight: bold;'>
                ${current_spend} / ${budget}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if progress > 1:
            st.error(f"⚠️ ${current_spend - budget} over budget this month")
        else:
            st.success(f"✅ ${budget - current_spend} remaining")
    
    with col2:
        st.subheader("🔮 Next Month Forecast")
        st.markdown("""
        <div style='background-color: #fff8e1; padding: 20px; border-radius: 10px; margin-bottom: 15px;'>
            <p style='color: gray; margin: 0;'>Projected Cash on Hand</p>
            <h2 style='margin: 5px 0;'>$5,820.00</h2>
            <p style='color: green; font-size: 14px; margin-top: 5px;'>↑ +$320 expected increase</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Forecast indicators
        st.markdown("**Forecast Confidence**")
        confidence_metrics = [
            {"label": "Income Prediction", "value": 92, "color": "#4caf50"},
            {"label": "Expense Prediction", "value": 85, "color": "#ff9800"},
            {"label": "Overall Confidence", "value": 88, "color": "#2196f3"}
        ]
        
        for metric in confidence_metrics:
            st.markdown(f"""
            <div style='margin-bottom: 10px;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                    <span style='font-size: 13px;'>{metric['label']}</span>
                    <span style='font-size: 13px; font-weight: bold;'>{metric['value']}%</span>
                </div>
                <div style='background-color: #e0e0e0; border-radius: 10px; height: 8px; overflow: hidden;'>
                    <div style='background-color: {metric['color']}; height: 100%; width: {metric['value']}%;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Cash flow projection chart
    st.subheader("💹 6-Month Cash Flow Projection")
    
    months = pd.date_range(start=datetime.now(), periods=6, freq='MS')
    actual_values = [5500, 5200, 5100]  # Past 3 months
    forecast_values = [5500, 5820, 6150, 6280]  # Current + next 3 months
    
    fig = go.Figure()
    
    # Historical line (solid)
    fig.add_trace(go.Scatter(
        x=months[:3],
        y=actual_values,
        mode='lines+markers',
        name='Actual',
        line=dict(color='#2196f3', width=3),
        marker=dict(size=10)
    ))
    
    # Forecast line (dashed)
    fig.add_trace(go.Scatter(
        x=months[2:],
        y=forecast_values,
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#ff9800', width=3, dash='dash'),
        marker=dict(size=10, symbol='diamond')
    ))
    
    # Confidence range
    upper_bound = [val * 1.1 for val in forecast_values]
    lower_bound = [val * 0.9 for val in forecast_values]
    
    fig.add_trace(go.Scatter(
        x=months[2:],
        y=upper_bound,
        mode='lines',
        name='Upper Range',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=months[2:],
        y=lower_bound,
        mode='lines',
        name='Confidence Range',
        line=dict(width=0),
        fillcolor='rgba(255, 152, 0, 0.2)',
        fill='tonexty',
        showlegend=True
    ))
    
    fig.update_layout(
        height=350,
        hovermode='x unified',
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Key insights and recommendations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background-color: #e8f5e9; padding: 20px; border-radius: 10px;'>
            <h4 style='margin: 0; color: #2e7d32;'>💡 Insight</h4>
            <p style='margin: 10px 0 0 0; font-size: 14px;'>Your savings rate is increasing. You're on track to reach your $10,000 emergency fund by August.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #fff3e0; padding: 20px; border-radius: 10px;'>
            <h4 style='margin: 0; color: #e65100;'>⚠️ Alert</h4>
            <p style='margin: 10px 0 0 0; font-size: 14px;'>Dining expenses are 20% higher than usual. Consider adjusting your budget.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color: #e3f2fd; padding: 20px; border-radius: 10px;'>
            <h4 style='margin: 0; color: #1565c0;'>🎯 Goal</h4>
            <p style='margin: 10px 0 0 0; font-size: 14px;'>Car Maintenance Fund needs $7,000. At current rate, you'll reach it in 4 months.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 View Forecast Details", use_container_width=True, type="primary"):
            st.info("Navigate to Forecasting page for detailed scenarios")
    with col2:
        if st.button("💰 Add to Savings", use_container_width=True):
            st.success("Deposit to savings fund")
    with col3:
        if st.button("📝 Adjust Budget", use_container_width=True):
            st.info("Go to Budget page")
    with col4:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.success("Data refreshed!")

# =======================
# TRANSACTIONS PAGE
# =======================
elif page == "Transactions":
    st.title("🧾 Transactions")
    
    # 1. KPIs at top - Clean and clear
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💵 Cash on Hand", "$5,500.00", delta="+$200", help="Your available cash after all obligations")
    with col2:
        st.metric("✅ Total Assets", "$6,000.00", help="All your bank and investment accounts")
    with col3:
        st.metric("❌ Total Liabilities", "$0.00", help="Credit cards and loans")
    with col4:
        st.metric("💰 Savings Funds", "$500.00", delta="+$50", help="Money set aside for future goals")
    
    st.markdown("---")
    
    # 2. VISUALS - Quick insights at a glance
    st.subheader("📊 Quick Insights")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("**Cash Flow Trend (Last 90 Days)**")
        days = pd.date_range(end=datetime.now(), periods=90, freq='D')
        
        # Generate dynamic data for three lines
        income_values = [3500 + (i * 10) + ((-1) ** i * 200) for i in range(90)]
        spending_values = [2800 + (i * 8) + ((-1) ** (i+1) * 150) for i in range(90)]
        investment_values = [500 + (i * 2) + ((-1) ** (i+2) * 50) for i in range(90)]
        
        fig = go.Figure()
        
        # Income line (green)
        fig.add_trace(go.Scatter(
            x=days, 
            y=income_values, 
            mode='lines',
            name='Income',
            line=dict(color='#4caf50', width=2.5),
            hovertemplate='<b>Income</b><br>%{y:$,.0f}<extra></extra>'
        ))
        
        # Spending line (red)
        fig.add_trace(go.Scatter(
            x=days, 
            y=spending_values, 
            mode='lines',
            name='Spending',
            line=dict(color='#f44336', width=2.5),
            hovertemplate='<b>Spending</b><br>%{y:$,.0f}<extra></extra>'
        ))
        
        # Investment line (blue)
        fig.add_trace(go.Scatter(
            x=days, 
            y=investment_values, 
            mode='lines',
            name='Investment',
            line=dict(color='#2196f3', width=2.5),
            hovertemplate='<b>Investment</b><br>%{y:$,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            height=250, 
            margin=dict(l=0, r=0, t=0, b=0), 
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with chart_col2:
        st.markdown("**Spending by Category**")
        categories = ['Groceries', 'Dining', 'Travel', 'Fuel', 'Entertainment']
        values = [250, 180, 450, 60, 75]
        colors = ['#5B8DB8', '#73B873', '#D97373', '#F4A460', '#9673B8']
        fig = px.pie(values=values, names=categories, color_discrete_sequence=colors)
        fig.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0), showlegend=True)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Action buttons BELOW VISUALS, aligned with table
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("📊 Offset Expenses", use_container_width=True, type="primary"):
            st.success("Match expenses to your savings funds")
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.success("Data refreshed!")
    
    st.markdown("---")
    
    # 3. FILTERS - Smart dropdowns with presets
    st.subheader("🔍 Filter Transactions")
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        time_filter = st.selectbox(
            "📅 Time Period",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Year to Date", "This Month", "Last Month", "All Time"],
            index=1,
            help="Choose a preset time range for quick filtering"
        )
    with col2:
        category_filter = st.multiselect(
            "🏷️ Categories",
            ["Travel", "Groceries", "Fuel", "Entertainment", "Dining out", "Utilities", "Shopping", "Transportation"],
            default=[],
            help="Select one or more categories. Leave empty for all."
        )
    with col3:
        account_filter = st.selectbox(
            "💳 Account",
            ["All Accounts", "Tutorial Credit Card", "Debit Card", "Savings Account"],
            help="Filter by specific account or view all"
        )
    
    st.markdown("---")
    
    # 4. TABLE - Filtered results
    st.subheader("📋 Transaction History")
    
    transactions_df = get_mock_transactions()
    
    # Filter data
    if category_filter and len(category_filter) > 0:
        transactions_df = transactions_df[transactions_df['Category'].isin(category_filter)]
    if account_filter != "All Accounts":
        transactions_df = transactions_df[transactions_df['Account'] == account_filter]
    
    # Show count
    st.caption(f"Showing {len(transactions_df)} transactions")
    
    st.dataframe(
        transactions_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Date": st.column_config.DateColumn("Date", format="MM/DD/YYYY"),
            "Amount": st.column_config.NumberColumn("Amount", format="$%.2f")
        }
    )

# =======================
# SAVINGS FUNDS PAGE
# =======================
elif page == "Savings Funds":
    st.title("💰 Savings Funds")
    
    # KPIs at top
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💵 Cash on Hand", "$5,500.00")
    with col2:
        st.metric("✅ Total Assets", "$6,000.00")
    with col3:
        st.metric("❌ Total Liabilities", "$0.00")
    with col4:
        st.metric("💰 Savings Funds", "$500.00")
    
    st.markdown("---")
    
    # Simple action buttons
    col1, col2, col3, col4 = st.columns([2, 2, 2, 6])
    with col1:
        if st.button("➕ New Fund", type="primary", use_container_width=True):
            st.info("Create new fund")
    with col2:
        if st.button("💵 Add Money", use_container_width=True):
            st.info("Add money to fund")
    with col3:
        if st.button("💸 Withdraw", use_container_width=True):
            st.info("Withdraw from fund")
    
    st.markdown("---")
    
    # Simple filter
    col1, col2 = st.columns([2, 1])
    with col1:
        fund_filter = st.selectbox(
            "📂 Filter Funds",
            ["All Funds", "With Goals", "Without Goals", "Car Maintenance Fund", "Emergency Fund", "Future Investments"]
        )
    with col2:
        sort_by = st.selectbox("Sort by:", ["Name", "Balance", "Goal Progress"])
    
    st.markdown("---")
    
    # Savings funds list
    funds = get_savings_funds()
    
    for fund in funds:
        with st.container():
            st.markdown(f"""
            <div class="fund-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h3 style="margin: 0;">{fund['name']}</h3>
                        <p style="color: gray; margin: 5px 0;">
                            {f"Monthly Contribution: ${fund['monthly_contribution']:,.2f}" if fund['monthly_contribution'] > 0 else "No Goal Set"}
                        </p>
                        {f'<p style="color: orange; margin: 5px 0;">⚠️ ${fund["monthly_contribution"]:,.2f} due this month</p>' if fund['monthly_contribution'] > 0 else ''}
                    </div>
                    <div style="text-align: right;">
                        <h2 style="color: green; margin: 0;">${fund['balance']:,.2f}</h2>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # PROGRESS BAR with clear visual indicator
            if fund['goal']:
                progress = min(fund['balance'] / fund['goal'], 1.0)
                remaining = fund['goal'] - fund['balance']
                
                st.progress(progress, text=f"${fund['balance']:,.2f} of ${fund['goal']:,.2f} saved ({progress*100:.1f}%)")
                
                if remaining > 0:
                    st.caption(f"💡 ${remaining:,.2f} remaining to reach goal")
                else:
                    st.success("🎉 Goal reached!")
            
            # Categories with better visual design
            if fund['categories']:
                st.markdown("**Linked Categories:**")
                for cat in fund['categories']:
                    st.markdown(f'<span class="category-chip">✓ {cat}</span>', unsafe_allow_html=True)
                st.caption("💡 Expenses in these categories will be tracked against this fund")
            else:
                st.info("💡 Link categories to automatically track expenses against this fund")
            
            # CLARIFIED ACTIONS
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button(f"📊 View History", key=f"view_{fund['name']}", use_container_width=True):
                    st.session_state[f"view_fund"] = fund['name']
            with col2:
                if st.button(f"✏️ Edit Settings", key=f"edit_{fund['name']}", use_container_width=True):
                    st.session_state[f"edit_fund"] = fund['name']
            with col3:
                if st.button(f"💵 Add Money", key=f"add_{fund['name']}", use_container_width=True, type="primary"):
                    st.success(f"Add money to {fund['name']}")
            
            # Show balance history if clicked
            if st.session_state.get(f"view_fund") == fund['name']:
                st.markdown("---")
                st.markdown("**📈 Balance Over Time**")
                
                dates = pd.date_range(end=datetime.now(), periods=12, freq='MS')
                balances = [max(0, fund['balance'] - (12-i)*50) for i in range(12)]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=balances,
                    mode='lines+markers',
                    line=dict(color='#4caf50', width=3),
                    marker=dict(size=8),
                    fill='tozeroy',
                    fillcolor='rgba(76, 175, 80, 0.1)'
                ))
                
                if fund['goal']:
                    fig.add_hline(y=fund['goal'], line_dash="dash", line_color="orange", 
                                annotation_text=f"Goal: ${fund['goal']:,.2f}")
                
                fig.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                
                if st.button("✕ Close", key=f"close_{fund['name']}"):
                    del st.session_state[f"view_fund"]
                    st.rerun()
            
            st.markdown("---")
    
    # Category management in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Manage Categories")
    
    categories = [
        "Car Insurance", "Internet", "Rent", "Subscriptions", 
        "Utilities", "Travel", "Wedding Expenses", "Dining out",
        "Entertainment", "Fuel", "Groceries"
    ]
    
    st.sidebar.multiselect(
        "Add categories to fund:",
        categories,
        default=[],
        key="quick_assign",
        help="Select categories to link to the active fund"
    )
    
    if page == "Savings Funds":
        st.sidebar.caption("💡 Linked to selected fund:")
        linked = ["Car Insurance", "Rent", "Travel", "Fuel"]
        for cat in linked:
            col1, col2 = st.sidebar.columns([4, 1])
            with col1:
                st.sidebar.markdown(f"<span style='color: green;'>✓</span> {cat}", unsafe_allow_html=True)
            with col2:
                if st.sidebar.button("✕", key=f"remove_{cat}"):
                    st.sidebar.info(f"Removed {cat}")

# =======================
# FORECASTING PAGE
# =======================
elif page == "Forecasting":
    st.title("🔮 Financial Forecasting")
    st.markdown("Plan your financial future with AI-powered projections and scenario planning")
    
    st.markdown("---")
    
    # Forecast KPIs at top
    st.subheader("📈 Forecast Summary (Next 30 Days)")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Projected Balance", "$5,820", delta="+$320", help="Expected end-of-month balance")
    with col2:
        st.metric("Expected Income", "$4,200", delta="+5%", help="Forecasted income")
    with col3:
        st.metric("Projected Expenses", "$3,880", delta="-2%", help="Expected spending")
    with col4:
        st.metric("Savings Growth", "$320", delta="+12%", help="Net savings increase")
    
    st.markdown("---")
    
    # Scenario Planning Section
    st.subheader("🎯 Scenario Planning")
    st.markdown("Adjust assumptions and see how they impact your financial future")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Adjust Your Assumptions:**")
        
        income_change = st.slider(
            "💵 Income Change (%)",
            min_value=-50,
            max_value=50,
            value=0,
            step=5,
            help="Adjust expected income increase or decrease"
        )
        
        expense_change = st.slider(
            "💳 Expense Change (%)",
            min_value=-50,
            max_value=50,
            value=0,
            step=5,
            help="Adjust expected spending increase or decrease"
        )
        
        investment_rate = st.slider(
            "📈 Investment Contribution (%)",
            min_value=0,
            max_value=30,
            value=10,
            step=5,
            help="Percentage of income to invest"
        )
        
        st.markdown("---")
        
        # Scenario presets
        st.markdown("**Quick Scenarios:**")
        if st.button("🎯 Conservative", use_container_width=True):
            st.info("Income -10%, Expenses +15%, Investment 5%")
        if st.button("📊 Balanced", use_container_width=True):
            st.info("Income +5%, Expenses +5%, Investment 10%")
        if st.button("🚀 Aggressive Growth", use_container_width=True):
            st.success("Income +10%, Expenses -10%, Investment 20%")
    
    with col2:
        st.markdown("**Impact on Future Cash Flow**")
        
        # Generate scenario-based forecast
        months = pd.date_range(start=datetime.now(), periods=12, freq='MS')
        
        # Base scenario
        base_values = [5500]
        for i in range(11):
            base_values.append(base_values[-1] + (4200 * 0.05) - (3880 * 0.05))
        
        # User scenario
        scenario_values = [5500]
        for i in range(11):
            monthly_income = 4200 * (1 + income_change/100)
            monthly_expense = 3880 * (1 + expense_change/100)
            monthly_investment = monthly_income * (investment_rate/100)
            net_change = monthly_income - monthly_expense - monthly_investment
            scenario_values.append(scenario_values[-1] + net_change)
        
        fig = go.Figure()
        
        # Base scenario (gray dashed)
        fig.add_trace(go.Scatter(
            x=months,
            y=base_values,
            mode='lines+markers',
            name='Current Trend',
            line=dict(color='#9e9e9e', width=2, dash='dash'),
            marker=dict(size=6)
        ))
        
        # User scenario (colored solid)
        scenario_color = '#4caf50' if scenario_values[-1] > base_values[-1] else '#f44336'
        
        fig.add_trace(go.Scatter(
            x=months,
            y=scenario_values,
            mode='lines+markers',
            name='Your Scenario',
            line=dict(color=scenario_color, width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            height=350,
            hovermode='x unified',
            margin=dict(l=0, r=0, t=0, b=0),
            yaxis_title="Balance ($)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Impact summary
        difference = scenario_values[-1] - base_values[-1]
        if difference > 0:
            st.success(f"✅ Your scenario results in ${difference:,.2f} more after 12 months!")
        else:
            st.error(f"⚠️ Your scenario results in ${abs(difference):,.2f} less after 12 months")
    
    st.markdown("---")
    
    # Detailed Category Forecasts
    st.subheader("📊 Category-Level Forecasts")
    
    tab1, tab2, tab3 = st.tabs(["💰 Income Forecast", "💳 Expense Forecast", "📈 Investment Forecast"])
    
    with tab1:
        st.markdown("**Projected Income Sources (Next 6 Months)**")
        
        income_data = pd.DataFrame({
            'Month': ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            'Salary': [3500, 3500, 3500, 3600, 3600, 3600],
            'Freelance': [500, 600, 550, 700, 650, 800],
            'Investments': [200, 220, 210, 250, 240, 280]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Salary', x=income_data['Month'], y=income_data['Salary'], marker_color='#4caf50'))
        fig.add_trace(go.Bar(name='Freelance', x=income_data['Month'], y=income_data['Freelance'], marker_color='#2196f3'))
        fig.add_trace(go.Bar(name='Investments', x=income_data['Month'], y=income_data['Investments'], marker_color='#ff9800'))
        
        fig.update_layout(barmode='stack', height=300, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption("💡 Freelance income shows strong growth trend. Consider increasing investment allocation.")
    
    with tab2:
        st.markdown("**Projected Expenses by Category (Next 6 Months)**")
        
        expense_categories = ['Groceries', 'Dining', 'Transport', 'Utilities', 'Entertainment']
        
        fig = go.Figure()
        
        for i, category in enumerate(expense_categories):
            values = [250 + i*50 + month*10 + ((-1)**month)*20 for month in range(6)]
            colors = ['#f44336', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5']
            
            fig.add_trace(go.Scatter(
                x=['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                y=values,
                mode='lines+markers',
                name=category,
                line=dict(color=colors[i], width=2),
                marker=dict(size=7)
            ))
        
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption("⚠️ Dining expenses trending upward. Consider setting a stricter budget.")
    
    with tab3:
        st.markdown("**Investment Growth Projection**")
        
        # Investment growth chart
        months = ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
        portfolio_values = [10000, 10420, 10850, 11290, 11740, 12200]
        contributions = [0, 400, 410, 420, 430, 440]
        gains = [0, 20, 20, 20, 20, 20]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Contributions',
            x=months,
            y=contributions,
            marker_color='#2196f3'
        ))
        
        fig.add_trace(go.Bar(
            name='Market Gains',
            x=months,
            y=gains,
            marker_color='#4caf50'
        ))
        
        fig.add_trace(go.Scatter(
            name='Total Portfolio',
            x=months,
            y=portfolio_values,
            mode='lines+markers',
            line=dict(color='#ff9800', width=3),
            marker=dict(size=10),
            yaxis='y2'
        ))
        
        fig.update_layout(
            barmode='stack',
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            yaxis=dict(title='Monthly Change ($)'),
            yaxis2=dict(title='Portfolio Value ($)', overlaying='y', side='right')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption("🎯 On track to reach $15,000 portfolio by end of year at current contribution rate.")
    
    st.markdown("---")
    
    # Forecast Confidence & Methodology
    with st.expander("ℹ️ How Forecasts Are Generated"):
        st.markdown("""
        **Our forecasting methodology combines:**
        
        1. **Historical Analysis**: We analyze your past 6-12 months of transactions to identify patterns
        2. **Seasonal Trends**: Account for predictable changes (holidays, annual expenses, etc.)
        3. **Machine Learning**: AI models predict future spending based on your habits
        4. **External Factors**: Consider economic indicators and market trends
        
        **Confidence Levels:**
        - 🟢 High (85%+): Based on consistent patterns
        - 🟡 Medium (70-85%): Some variability in historical data
        - 🔴 Low (<70%): Insufficient data or high volatility
        
        **Tips for Better Forecasts:**
        - Connect all your accounts for complete data
        - Categorize transactions consistently
        - Update your budget regularly
        - Review and adjust forecasts monthly
        """)

# =======================
#   for cat in linked:
        col1, col2 = st.sidebar.columns([4, 1])
        with col1:
            st.sidebar.markdown(f"<span style='color: green;'>✓</span> {cat}", unsafe_allow_html=True)
        with col2:
            if st.sidebar.button("✕", key=f"remove_{cat}"):
                st.sidebar.info(f"Removed {cat}")

# =======================
# CASH ON HAND PAGE
# =======================
elif page == "Cash on Hand":
    st.title("💵 Cash on Hand")
    
    # 1. SUMMARY - Big and clear with context
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 40px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
        <p style="color: gray; margin: 0; font-size: 18px;">💰 Current Cash on Hand</p>
        <h1 style="color: #2c3e50; margin: 10px 0; font-size: 56px;">$5,500.00</h1>
        <p style="color: gray; font-size: 14px;">Assets $6,000 - Liabilities $0 - Savings Funds $500</p>
        <p style="color: #5B8DB8; font-size: 12px; margin-top: 10px;">💡 This is your true available cash after all obligations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. SIMPLE CHART with preset dropdown
    st.subheader("💹 Cash Flow Trend")
    
    timeframe = st.selectbox(
        "Show last:",
        ["3 Months", "6 Months", "12 Months", "All Time"],
        index=2
    )
    
    # Generate mock data
    months = pd.date_range(start='2025-03-01', end='2026-01-01', freq='MS')
    values = [5000, 5200, 5100, 5300, 5250, 4800, 4500, 4200, 4100, 4800, 5500]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=values,
        mode='lines+markers',
        line=dict(color='#5B8DB8', width=3),
        marker=dict(size=10),
        fill='tozeroy',
        fillcolor='rgba(91, 141, 184, 0.1)'
    ))
    fig.update_layout(
        height=350,
        xaxis_title="",
        yaxis_title="",
        hovermode='x unified',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 3. SIMPLIFIED CONFIGURATION
    with st.expander("⚙️ Advanced: Configure Accounts", expanded=False):
        st.info("💡 **How Cash on Hand is calculated:** Assets (what you have) - Liabilities (what you owe) - Savings Funds (money set aside for goals)")
        st.caption("Customize which accounts count as assets or liabilities:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Assets (+)**")
            st.checkbox("Tutorial Credit Card - $5,000", value=True)
            st.checkbox("Savings Account - $1,000", value=True)
        
        with col2:
            st.markdown("**Liabilities (-)**")
            st.info("No liabilities configured")
        
        if st.button("💾 Save Configuration"):
            st.success("Configuration saved!")

# =======================
# BUDGET PAGE
# =======================
elif page == "Budget":
    st.title("💰 Budget Overview")
    
    # Simple month selection
    col1, col2 = st.columns([2, 4])
    with col1:
        current_month = st.selectbox("📅 Viewing:", ["January 2026", "December 2025", "November 2025"])
    with col2:
        st.markdown("<p style='color: gray; padding-top: 8px;'>Compare against your 3-month average</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # BIG PICTURE SUMMARY
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background-color: #e8f4f8; padding: 25px; border-radius: 10px; text-align: center;'>
            <p style='color: gray; margin: 0;'>Monthly Budget 💡</p>
            <h2 style='margin: 5px 0;'>$750</h2>
            <p style='color: gray; font-size: 12px; margin-top: 5px;'>Your planned spending</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background-color: #fff8e1; padding: 25px; border-radius: 10px; text-align: center;'>
            <p style='color: gray; margin: 0;'>Spent This Month 💳</p>
            <h2 style='margin: 5px 0;'>$790</h2>
            <p style='color: gray; font-size: 12px; margin-top: 5px;'>Actual spending so far</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background-color: #ffebee; padding: 25px; border-radius: 10px; text-align: center;'>
            <p style='color: gray; margin: 0;'>Difference ⚠️</p>
            <h2 style='margin: 5px 0; color: #d32f2f;'>+$40</h2>
            <p style='color: #d32f2f; margin: 5px 0; font-size: 14px;'>5.3% over budget</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # SIMPLIFIED CATEGORY VIEW
    st.subheader("📊 Spending by Category")
    
    category_data = [
        {"Category": "🍽️ Dining out", "Budget": 150, "Spent": 180, "Status": "over"},
        {"Category": "🎬 Entertainment", "Budget": 80, "Spent": 75, "Status": "good"},
        {"Category": "⛽ Fuel", "Budget": 60, "Spent": 60, "Status": "good"},
        {"Category": "🛒 Groceries", "Budget": 250, "Spent": 250, "Status": "good"},
        {"Category": "💆 Personal Care", "Budget": 40, "Spent": 35, "Status": "good"},
        {"Category": "🛍️ Shopping", "Budget": 100, "Spent": 120, "Status": "over"},
        {"Category": "🚗 Transportation", "Budget": 70, "Spent": 70, "Status": "good"},
    ]
    
    for cat in category_data:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                st.markdown(f"**{cat['Category']}**")
            
            with col2:
                percentage = (cat['Spent'] / cat['Budget']) * 100 if cat['Budget'] > 0 else 0
                color = "#d32f2f" if percentage > 100 else "#4caf50"
                st.markdown(f"""
                <div style='background-color: #f0f0f0; border-radius: 10px; height: 25px; position: relative; overflow: hidden;'>
                    <div style='background-color: {color}; height: 100%; width: {min(percentage, 100)}%; border-radius: 10px;'></div>
                    <div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 12px; font-weight: bold;'>
                        {percentage:.0f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"<p style='text-align: center;'>${cat['Spent']} / ${cat['Budget']}</p>", unsafe_allow_html=True)
            
            with col4:
                if cat['Status'] == "over":
                    st.markdown("🔴")
                else:
                    st.markdown("🟢")
            
            st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # OPTIONAL: Big expenses
    with st.expander("🎯 One-Time / Big Expenses", expanded=False):
        st.markdown("Track expenses that don't happen every month")
        
        big_expenses = pd.DataFrame({
            'Category': ['Travel', 'Wedding Expenses'],
            'Budgeted': [500, 1000],
            'Spent': [0, 0]
        })
        
        st.dataframe(big_expenses, use_container_width=True, hide_index=True)
        
        if st.button("➕ Add One-Time Expense"):
            st.info("Add one-time expense")

# =======================
# BALANCE HISTORY PAGE
# =======================
else:
    st.title("📊 Balance History")
    st.info("Balance History page - Track your net worth over time")
    st.markdown("**Coming soon:** Historical charts and trends for all your accounts")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔒 Security Protocol")
st.sidebar.markdown("**SUPPORT ID**")
st.sidebar.code("0d72a4c4...")
st.sidebar.caption("Share this ID for help. We do not see your data.")

if st.sidebar.button("➕ Connect Account", use_container_width=True):
    st.sidebar.success("Connect new account feature")
