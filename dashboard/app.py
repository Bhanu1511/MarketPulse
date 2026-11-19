import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="MarketPulse | Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "analysis_outputs"

BRL_TO_INR = 15.8392
EXCHANGE_RATE_DATE = "19 November 2026"


# =====================================================
# 2. LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    return {
        "monthly": pd.read_csv(DATA_DIR / "monthly_revenue.csv"),
        "category": pd.read_csv(DATA_DIR / "category_revenue.csv"),
        "segments": pd.read_csv(DATA_DIR / "customer_segments.csv"),
        "delivery": pd.read_csv(DATA_DIR / "delivery_performance.csv"),
        "reviews": pd.read_csv(DATA_DIR / "review_distribution.csv"),
        "satisfaction": pd.read_csv(DATA_DIR / "delivery_satisfaction.csv")
    }


try:
    data = load_data()

except Exception as e:
    st.error(f"Unable to load project data: {e}")
    st.stop()


monthly = data["monthly"].copy()
category = data["category"].copy()
segments = data["segments"].copy()
delivery = data["delivery"].copy()
reviews = data["reviews"].copy()
satisfaction = data["satisfaction"].copy()


# =====================================================
# 3. CURRENCY CONVERSION
# =====================================================

monthly["revenue"] = monthly["revenue"] * BRL_TO_INR
category["revenue"] = category["revenue"] * BRL_TO_INR

monthly["month_date"] = pd.to_datetime(
    monthly["month"],
    errors="coerce"
)

monthly = monthly.sort_values("month_date").reset_index(drop=True)


# =====================================================
# 4. CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F5F7FB;
    color: #17243A;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #101D35 0%,
        #172A49 100%
    );
    border-right: 1px solid #263957;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 30px 18px;
}

.brand-container {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}

.brand-logo {
    width: 45px;
    height: 45px;
    min-width: 45px;
    background: linear-gradient(135deg, #12A892, #176B87);
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 19px;
    font-weight: 800;
}

.brand-name {
    font-size: 23px;
    font-weight: 800;
    color: #FFFFFF;
}

.brand-sub {
    font-size: 9px;
    color: #91A7C5;
    letter-spacing: 1.5px;
    margin-bottom: 35px;
}

.sidebar-label {
    color: #8195B3;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin: 25px 0 12px 8px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 8px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: transparent;
    padding: 12px 14px;
    border-radius: 9px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #263D5E;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: #176B87;
    border-left: 4px solid #43D6C5;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    color: #E8EEF8 !important;
    font-size: 13px;
    font-weight: 600;
}

[data-testid="stSidebar"] [data-testid="stRadio"] input {
    display: none;
}

.sidebar-info {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 10px;
    padding: 14px;
    margin-top: 12px;
    color: #DCE6F4;
    font-size: 12px;
    line-height: 1.8;
}

.sidebar-footer {
    color: #8195B3;
    font-size: 11px;
    margin-top: 35px;
    border-top: 1px solid #30425D;
    padding-top: 18px;
}

/* MAIN CONTENT */

.page-title {
    font-size: 30px;
    font-weight: 800;
    color: #17243A;
    margin-bottom: 3px;
}

.page-subtitle {
    color: #718096;
    font-size: 14px;
    margin-bottom: 25px;
}

.section-title {
    color: #17243A;
    font-size: 19px;
    font-weight: 700;
    margin: 25px 0 15px 0;
}

/* KPI CARDS */

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E8EDF5;
    border-radius: 13px;
    padding: 19px;
    min-height: 125px;
    box-shadow: 0 3px 12px rgba(20,40,80,0.04);
    border-top: 3px solid #176B87;
}

.metric-label {
    font-size: 13px;
    color: #718096;
    font-weight: 500;
}

.metric-value {
    font-size: 25px;
    font-weight: 800;
    color: #17243A;
    margin-top: 12px;
}

.metric-icon {
    font-size: 19px;
    float: right;
}

/* INSIGHTS */

.insight-card {
    background: #FFFFFF;
    border-left: 4px solid #12A892;
    border-radius: 10px;
    padding: 17px;
    margin-bottom: 12px;
    box-shadow: 0 3px 12px rgba(20,40,80,0.04);
    color: #334155;
    font-size: 14px;
    line-height: 1.6;
}

/* CHARTS */

div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #E8EDF5;
    border-radius: 12px;
    padding: 10px;
}

/* BUTTONS */

.stDownloadButton button {
    background: #176B87;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 9px 18px;
    font-weight: 600;
}

.stDownloadButton button:hover {
    background: #12566D;
    color: white;
}

.footer {
    text-align: center;
    color: #8793A5;
    font-size: 12px;
    padding: 25px;
}

hr {
    border-color: #E5EAF2;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 5. BUSINESS METRICS
# =====================================================

total_revenue = monthly["revenue"].sum()

total_orders = delivery["total_orders"].sum()

total_customers = segments["total_customers"].sum()

on_time_orders = delivery.loc[
    delivery["delivery_status"] == "On Time",
    "total_orders"
].sum()

on_time_rate = (
    on_time_orders / total_orders * 100
    if total_orders else 0
)

average_rating = (
    (reviews["review_score"] * reviews["total_reviews"]).sum()
    / reviews["total_reviews"].sum()
)

average_order_value = (
    total_revenue / total_orders
    if total_orders else 0
)


# =====================================================
# 6. CHART DESIGN
# =====================================================

CHART_LAYOUT = {
    "paper_bgcolor": "#FFFFFF",
    "plot_bgcolor": "#FFFFFF",

    "font": {
        "family": "Inter",
        "color": "#334155"
    },

    "margin": {
        "l": 20,
        "r": 20,
        "t": 55,
        "b": 25
    },

    "legend": {
        "orientation": "h",
        "y": 1.12
    }
}


# =====================================================
# 7. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
        <div class="brand-container">
            <div class="brand-logo">MP</div>
            <div class="brand-name">MarketPulse</div>
        </div>

        <div class="brand-sub">
            BUSINESS INTELLIGENCE & ANALYTICS
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="sidebar-label">MAIN MENU</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "🏠  Business Overview",
            "📈  Revenue Analytics",
            "👥  Customer Analytics",
            "🚚  Operations"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-label">DATA SOURCE</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
        <div class="sidebar-info">
            <b>🇧🇷 Brazilian E-Commerce</b><br>
            Olist Public Dataset<br>
            <span style="color:#91A7C5">2016 – 2018</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-info">
            <b>💱 Display Currency</b><br>
            Indian Rupee (INR)<br>
            <span style="color:#91A7C5">Converted from BRL</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-footer">
            <b>MARKETPULSE</b><br>
            Business Intelligence Platform<br>
            Version 2.0
        </div>
    """, unsafe_allow_html=True)


# =====================================================
# 8. MAIN HEADER
# =====================================================

st.markdown(
    '<div class="page-title">Business Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Monitor performance. Understand customers. Make better decisions.'
    '</div>',
    unsafe_allow_html=True
)


# =====================================================
# 9. KPI CARDS
# =====================================================

def metric_card(label, value, icon):

    html = (
        '<div class="metric-card">'
        f'<span class="metric-icon">{icon}</span>'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def show_kpis():

    cols = st.columns(5)

    metrics = [
        ("Total Revenue", f"₹ {total_revenue / 10000000:.2f} Cr", "💰"),
        ("Delivered Orders", f"{total_orders:,}", "📦"),
        ("Unique Customers", f"{total_customers:,}", "👥"),
        ("On-Time Delivery", f"{on_time_rate:.1f}%", "🚚"),
        ("Average Rating", f"{average_rating:.2f}/5", "⭐")
    ]

    for col, item in zip(cols, metrics):
        with col:
            metric_card(*item)

    st.caption(
        f"Average order value: ₹ {average_order_value:,.2f} "
        f"| Revenue converted from BRL to INR at "
        f"1 BRL = ₹{BRL_TO_INR}. "
        f"Rate date: {EXCHANGE_RATE_DATE}."
    )


# =====================================================
# 10. BUSINESS OVERVIEW
# =====================================================

if page == "🏠  Business Overview":

    show_kpis()

    st.markdown(
        '<div class="section-title">Revenue Performance</div>',
        unsafe_allow_html=True
    )

    fig = px.area(
        monthly,
        x="month",
        y="revenue",
        markers=True,
        labels={
            "month": "Month",
            "revenue": "Revenue (INR)"
        }
    )

    fig.update_traces(
        line=dict(color="#176B87", width=3),
        fillcolor="rgba(23,107,135,0.12)",
        hovertemplate="%{x}<br>Revenue: ₹ %{y:,.2f}<extra></extra>"
    )

    fig.update_layout(
        **CHART_LAYOUT,
        height=370,
        yaxis_tickformat=",.0f"
    )

    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="section-title">Top Product Categories</div>',
            unsafe_allow_html=True
        )

        fig = px.bar(
            category.sort_values("revenue"),
            x="revenue",
            y="category",
            orientation="h",
            labels={
                "revenue": "Revenue (INR)",
                "category": "Category"
            }
        )

        fig.update_traces(
            marker_color="#176B87",
            hovertemplate="%{y}<br>Revenue: ₹ %{x:,.2f}<extra></extra>"
        )

        fig.update_layout(
            **CHART_LAYOUT,
            height=390,
            xaxis_tickformat=",.0f"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        st.markdown(
            '<div class="section-title">Customer Segments</div>',
            unsafe_allow_html=True
        )

        fig = px.pie(
            segments,
            names="customer_segment",
            values="total_customers",
            hole=0.58
        )

        fig.update_traces(
            marker=dict(
                colors=[
                    "#176B87",
                    "#12A892",
                    "#62B6CB",
                    "#F4B942",
                    "#7589A8",
                    "#A6B9D0"
                ]
            ),
            textinfo="percent"
        )

        fig.update_layout(
            **CHART_LAYOUT,
            height=390
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="section-title">Business Highlights</div>',
        unsafe_allow_html=True
    )

    peak_month = monthly.loc[
        monthly["revenue"].idxmax(), "month"
    ]

    peak_category = category.loc[
        category["revenue"].idxmax(), "category"
    ]

    st.markdown(
        f"""
        <div class="insight-card">
            📈 <b>Revenue peak:</b>
            {peak_month} recorded the highest monthly revenue.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="insight-card">
            🏆 <b>Leading category:</b>
            {peak_category} generated the highest revenue
            among the displayed categories.
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# 11. REVENUE ANALYTICS
# =====================================================

elif page == "📈  Revenue Analytics":

    st.markdown(
        '<div class="page-title">Revenue Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Explore revenue trends, monthly growth and category performance.'
        '</div>',
        unsafe_allow_html=True
    )

    selected_months = st.multiselect(
        "Filter by month",
        monthly["month"].tolist(),
        default=monthly["month"].tolist()
    )

    filtered = monthly[
        monthly["month"].isin(selected_months)
    ].copy()

    # ==========================================
    # REVENUE GROWTH CALCULATION
    # ==========================================

    growth_data = monthly.copy()

    growth_data["previous_revenue"] = (
        growth_data["revenue"].shift(1)
    )

    growth_data["growth_percentage"] = (
        (
            growth_data["revenue"]
            - growth_data["previous_revenue"]
        )
        / growth_data["previous_revenue"].replace(0, pd.NA)
    ) * 100

    growth_filtered = growth_data[
        growth_data["month"].isin(selected_months)
    ].copy()

    # ==========================================
    # SELECTED PERIOD REVENUE
    # ==========================================

    st.metric(
        "Revenue in Selected Period",
        f"₹ {filtered['revenue'].sum() / 10000000:.2f} Cr"
    )

    # ==========================================
    # MONTHLY REVENUE TREND
    # ==========================================

    st.markdown(
        '<div class="section-title">Monthly Revenue Trend</div>',
        unsafe_allow_html=True
    )

    if not filtered.empty:

        fig = px.line(
            filtered,
            x="month",
            y="revenue",
            markers=True,
            labels={
                "month": "Month",
                "revenue": "Revenue (INR)"
            }
        )

        fig.update_traces(
            line=dict(color="#176B87", width=3),
            hovertemplate="%{x}<br>Revenue: ₹ %{y:,.2f}<extra></extra>"
        )

        fig.update_layout(
            **CHART_LAYOUT,
            height=400,
            yaxis_tickformat=",.0f"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Select at least one month to view revenue.")

    # ==========================================
    # REVENUE GROWTH ANALYSIS
    # ==========================================

    st.markdown(
        '<div class="section-title">Revenue Growth Analysis</div>',
        unsafe_allow_html=True
    )

    valid_growth = growth_filtered.dropna(
        subset=["growth_percentage"]
    )

    if not filtered.empty:

        highest_month = filtered.loc[
            filtered["revenue"].idxmax()
        ]

        lowest_month = filtered.loc[
            filtered["revenue"].idxmin()
        ]

        col1, col2, col3 = st.columns(3)

        with col1:

            if not valid_growth.empty:

                latest_growth = valid_growth.iloc[-1]

                growth_value = latest_growth["growth_percentage"]

                st.metric(
                    "Latest Monthly Growth",
                    f"{growth_value:.2f}%",
                    delta=f"{growth_value:.2f}%"
                )

            else:
                st.metric(
                    "Latest Monthly Growth",
                    "N/A"
                )

        with col2:

            st.metric(
                "Highest Revenue Month",
                highest_month["month"],
                f"₹ {highest_month['revenue']:,.0f}"
            )

        with col3:

            st.metric(
                "Lowest Revenue Month",
                lowest_month["month"],
                f"₹ {lowest_month['revenue']:,.0f}"
            )

    # ==========================================
    # MONTHLY GROWTH CHART
    # ==========================================

    st.markdown(
        '<div class="section-title">Month-over-Month Growth</div>',
        unsafe_allow_html=True
    )

    chart_growth = growth_filtered[
        growth_filtered["month"] != "2017-01"
    ].dropna(
        subset=["growth_percentage"]
    )

    if not chart_growth.empty:

        fig = px.bar(
            chart_growth,
            x="month",
            y="growth_percentage",
            color="growth_percentage",
            color_continuous_scale=[
                "#E76F51",
                "#F4B942",
                "#12A892"
            ],
            labels={
                "month": "Month",
                "growth_percentage": "Growth (%)"
            }
        )

        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="#718096"
        )

        fig.update_layout(
            **CHART_LAYOUT,
            height=370,
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("Not enough monthly data to calculate growth.")

    st.caption(
        "Growth compares revenue with the previous calendar month. "
        "January 2017 is excluded from the growth chart because "
        "December 2016 had exceptionally low revenue, producing "
        "a misleading percentage increase."
    )

    # ==========================================
    # MONTHLY COMPARISON TABLE
    # ==========================================

    st.markdown(
        '<div class="section-title">Monthly Revenue Comparison</div>',
        unsafe_allow_html=True
    )

    growth_table = growth_filtered[
        [
            "month",
            "previous_revenue",
            "revenue",
            "growth_percentage"
        ]
    ].rename(columns={
        "month": "Month",
        "previous_revenue": "Previous Revenue (INR)",
        "revenue": "Current Revenue (INR)",
        "growth_percentage": "Growth (%)"
    })

    st.dataframe(
        growth_table.round(2),
        use_container_width=True,
        hide_index=True
    )

    # ==========================================
    # CATEGORY ANALYSIS
    # ==========================================

    st.markdown(
        '<div class="section-title">Category Analysis</div>',
        unsafe_allow_html=True
    )

    selected_categories = st.multiselect(
        "Filter by category",
        category["category"].tolist(),
        default=category["category"].tolist()
    )

    filtered_cat = category[
        category["category"].isin(selected_categories)
    ]

    if not filtered_cat.empty:

        fig = px.bar(
            filtered_cat.sort_values("revenue"),
            x="revenue",
            y="category",
            orientation="h",
            labels={
                "revenue": "Revenue (INR)",
                "category": "Category"
            }
        )

        fig.update_traces(
            marker_color="#12A892",
            hovertemplate="%{y}<br>Revenue: ₹ %{x:,.2f}<extra></extra>"
        )

        fig.update_layout(
            **CHART_LAYOUT,
            height=420,
            xaxis_tickformat=",.0f"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        "⬇ Download Revenue Report",
        filtered.to_csv(index=False),
        file_name="marketpulse_revenue_inr.csv",
        mime="text/csv"
    )

    st.download_button(
        "⬇ Download Growth Report",
        growth_filtered.to_csv(index=False),
        file_name="marketpulse_growth_report.csv",
        mime="text/csv"
    )


# =====================================================
# 12. CUSTOMER ANALYTICS
# =====================================================

elif page == "👥  Customer Analytics":

    st.markdown(
        '<div class="page-title">Customer Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Understand customer behaviour through RFM segmentation.'
        '</div>',
        unsafe_allow_html=True
    )

    st.metric(
        "Total Unique Customers",
        f"{total_customers:,}"
    )

    st.markdown(
        '<div class="section-title">Customer Segmentation</div>',
        unsafe_allow_html=True
    )

    fig = px.bar(
        segments.sort_values("total_customers"),
        x="total_customers",
        y="customer_segment",
        orientation="h",
        labels={
            "total_customers": "Number of Customers",
            "customer_segment": "Segment"
        }
    )

    fig.update_traces(
        marker_color="#176B87"
    )

    fig.update_layout(
        **CHART_LAYOUT,
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="section-title">Segment Details</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        segments.sort_values(
            "total_customers",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇ Download Customer Report",
        segments.to_csv(index=False),
        file_name="marketpulse_customers.csv",
        mime="text/csv"
    )


# =====================================================
# 13. OPERATIONS
# =====================================================

elif page == "🚚  Operations":

    st.markdown(
        '<div class="page-title">Operations & Satisfaction</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Track delivery performance and customer experience.'
        '</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    # DELIVERY PERFORMANCE

    with left:

        st.markdown(
            '<div class="section-title">Delivery Performance</div>',
            unsafe_allow_html=True
        )

        fig = px.pie(
            delivery,
            names="delivery_status",
            values="total_orders",
            hole=0.58,
            color="delivery_status",
            color_discrete_map={
                "On Time": "#12A892",
                "Late": "#E76F51"
            }
        )

        fig.update_layout(
            **CHART_LAYOUT,
            height=370
        )

        st.plotly_chart(fig, use_container_width=True)

    # CUSTOMER SATISFACTION

    with right:

        st.markdown(
            '<div class="section-title">Delivery vs Satisfaction</div>',
            unsafe_allow_html=True
        )

        fig = px.bar(
            satisfaction,
            x="delivery_status",
            y="average_review_score",
            color="delivery_status",
            color_discrete_map={
                "On Time": "#176B87",
                "Late": "#E76F51"
            },
            labels={
                "delivery_status": "Delivery Status",
                "average_review_score": "Average Rating"
            }
        )

        fig.update_layout(
            **CHART_LAYOUT,
            height=370,
            yaxis=dict(range=[0, 5])
        )

        st.plotly_chart(fig, use_container_width=True)

    # REVIEW DISTRIBUTION

    st.markdown(
        '<div class="section-title">Customer Review Distribution</div>',
        unsafe_allow_html=True
    )

    fig = px.bar(
        reviews,
        x="review_score",
        y="total_reviews",
        labels={
            "review_score": "Review Score",
            "total_reviews": "Number of Reviews"
        }
    )

    fig.update_traces(
        marker_color="#12A892"
    )

    fig.update_layout(
        **CHART_LAYOUT,
        height=350
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class="insight-card">
            💡 <b>Key finding:</b>
            Late deliveries are associated with substantially
            lower average customer ratings than on-time deliveries.
            This is an association, not proof of causation.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.download_button(
        "⬇ Download Review Report",
        reviews.to_csv(index=False),
        file_name="marketpulse_reviews.csv",
        mime="text/csv"
    )


# =====================================================
# 14. FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">
        <b>MARKETPULSE</b><br>
        BUSINESS INTELLIGENCE & ANALYTICS<br><br>
        Built with Python • SQL • PostgreSQL • Pandas • Plotly • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)