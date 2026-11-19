import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================================================
# MARKETPULSE 3.0 | BUSINESS & CUSTOMER INTELLIGENCE
# =========================================================
st.set_page_config(
    page_title="MarketPulse | Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "analysis_outputs"

# Historical conversion assumption used in this portfolio project.
# This is a fixed illustrative conversion rate, not a live FX quote.
BRL_TO_INR = 15.8392
RATE_BASIS_DATE = "19 November 2026"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:Inter,sans-serif;}
.stApp {background:#F4F7FB;color:#17243A;}
[data-testid="stHeader"] {background:transparent;}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#101D35,#1B3152);}
[data-testid="stSidebar"] [data-testid="stRadio"] label p {color:#EAF0F8!important;font-size:13px;font-weight:600;}
[data-testid="stSidebar"] [data-testid="stRadio"] label {padding:8px 10px;border-radius:8px;}
.brand {color:white;font-size:25px;font-weight:800;margin:8px 0 2px;}
.brand-sub {color:#9CB0CA;font-size:10px;letter-spacing:1.5px;margin-bottom:25px;}
.page-title {font-size:30px;font-weight:800;color:#17243A;}
.page-sub {font-size:14px;color:#718096;margin:5px 0 22px;}
.section-title {font-size:19px;font-weight:700;color:#17243A;margin:24px 0 12px;}
.metric-card {background:white;border:1px solid #E6ECF4;border-top:3px solid #16839A;border-radius:12px;padding:16px;min-height:105px;box-shadow:0 3px 12px #15294a0b;}
.metric-label {font-size:12px;color:#718096;}
.metric-value {font-size:23px;font-weight:800;color:#17243A;margin-top:10px;}
.insight {background:white;border-left:4px solid #12A892;border-radius:8px;padding:14px;margin:10px 0;color:#334155;line-height:1.5;}
div[data-testid="stPlotlyChart"] {background:white;border:1px solid #E6ECF4;border-radius:12px;padding:7px;}
.stDownloadButton button {background:#176B87;color:white;border:0;border-radius:8px;font-weight:600;}
.footer {text-align:center;color:#8793A5;font-size:12px;padding:22px;}
</style>
""", unsafe_allow_html=True)

FILES = {
    "monthly": "monthly_revenue.csv",
    "category": "category_revenue.csv",
    "segments": "customer_segments.csv",
    "delivery": "delivery_performance.csv",
    "reviews": "review_distribution.csv",
    "satisfaction": "delivery_satisfaction.csv",
    "geography": "geographic_sales.csv",
    "payments": "payment_analysis.csv",
    "sellers": "seller_analysis.csv",
    "seller_states": "seller_state_analysis.csv",
    "clv": "customer_clv.csv",
    "clv_summary": "clv_summary.csv",
    "purchase": "purchase_comparison.csv",
    "retention": "retention_summary.csv",
    "monthly_customers": "monthly_customers.csv",
    "monthly_new_returning": "monthly_new_returning.csv",
    "frequency": "customer_frequency.csv",
    "category_advanced": "category_performance_advanced.csv",
    "products": "product_performance_advanced.csv",
    "low_categories": "low_performing_categories.csv",
}

@st.cache_data
def load_all():
    frames, missing = {}, []
    for key, filename in FILES.items():
        path = DATA / filename
        if path.exists():
            try:
                frames[key] = pd.read_csv(path)
            except Exception:
                frames[key] = None
                missing.append(filename + " (could not read)")
        else:
            frames[key] = None
            missing.append(filename)
    return frames, missing

D, MISSING = load_all()

def get(key):
    return D.get(key)

def has(key):
    frame = get(key)
    return isinstance(frame, pd.DataFrame) and not frame.empty

def heading(text, subtitle=""):
    st.markdown(f'<div class="page-title">{text}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="page-sub">{subtitle}</div>', unsafe_allow_html=True)

def section(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)

def metric(label, value, icon=""):
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{icon} {label}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True,
    )

def metrics(items):
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        with col:
            metric(*item)

def plot(fig, height=370):
    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter", color="#334155"),
        margin=dict(l=25, r=20, t=55, b=25),
        legend=dict(orientation="h", y=1.12),
    )
    st.plotly_chart(fig, use_container_width=True)

def download(frame, filename):
    if isinstance(frame, pd.DataFrame) and not frame.empty:
        st.download_button(
            "⬇ Download CSV",
            frame.to_csv(index=False).encode("utf-8"),
            file_name=filename,
            mime="text/csv",
        )

def inr(value):
    return f"₹{value:,.0f}"

# Convert copied dataframes for display. Cached source frames remain untouched.
def converted(key, columns):
    frame = get(key)
    if not isinstance(frame, pd.DataFrame):
        return pd.DataFrame()
    frame = frame.copy()
    for col in columns:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce") * BRL_TO_INR
    return frame

monthly = converted("monthly", ["revenue"])
category = converted("category", ["revenue"])
geography = converted("geography", ["total_revenue"])
payments = converted("payments", ["total_payment_value", "average_payment"])
sellers = converted("sellers", ["total_revenue", "average_item_price", "average_order_value"])
seller_states = converted("seller_states", ["total_revenue"])
clv = converted("clv", ["total_revenue", "average_order_value"])
clv_summary = converted("clv_summary", ["total_revenue", "average_revenue"])
purchase = converted("purchase", ["total_revenue", "average_revenue"])
category_advanced = converted("category_advanced", ["total_revenue", "average_item_price"])
products = converted("products", ["total_revenue", "average_item_price"])
low_categories = converted("low_categories", ["total_revenue"])

if not monthly.empty and "month" in monthly.columns:
    monthly["month_date"] = pd.to_datetime(monthly["month"], errors="coerce")
    monthly = monthly.sort_values("month_date")

delivery = get("delivery").copy() if has("delivery") else pd.DataFrame()
segments = get("segments").copy() if has("segments") else pd.DataFrame()
reviews = get("reviews").copy() if has("reviews") else pd.DataFrame()
satisfaction = get("satisfaction").copy() if has("satisfaction") else pd.DataFrame()

if monthly.empty or delivery.empty:
    st.error("Required files monthly_revenue.csv or delivery_performance.csv are missing or empty.")
    st.stop()

# Project-wide headline metrics
revenue_total = pd.to_numeric(monthly.get("revenue", pd.Series(dtype=float)), errors="coerce").sum()
orders_total = pd.to_numeric(delivery.get("total_orders", pd.Series(dtype=float)), errors="coerce").sum()
customers_total = (
    pd.to_numeric(segments["total_customers"], errors="coerce").sum()
    if "total_customers" in segments.columns else 0
)
on_time_count = 0
if {"delivery_status", "total_orders"}.issubset(delivery.columns):
    on_time_count = delivery.loc[
        delivery["delivery_status"].astype(str).str.lower().eq("on time"), "total_orders"
    ].sum()
on_time_pct = on_time_count / orders_total * 100 if orders_total else 0
avg_rating = 0
if {"review_score", "total_reviews"}.issubset(reviews.columns):
    n = pd.to_numeric(reviews["total_reviews"], errors="coerce").sum()
    if n:
        avg_rating = (
            pd.to_numeric(reviews["review_score"], errors="coerce")
            * pd.to_numeric(reviews["total_reviews"], errors="coerce")
        ).sum() / n

PAGES = [
    "🏠 Business Overview",
    "📈 Revenue Analytics",
    "👥 Customer Analytics",
    "💎 Customer Lifetime Value",
    "🔄 Customer Retention",
    "🛍️ Product Analytics",
    "🏪 Seller Analytics",
    "🌍 Geographic Analytics",
    "💳 Payment Analytics",
    "🚚 Operations",
    "⭐ Customer Satisfaction",
]

with st.sidebar:
    st.markdown('<div class="brand">▣ MarketPulse</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">BUSINESS INTELLIGENCE PLATFORM</div>', unsafe_allow_html=True)
    page = st.radio("Navigation", PAGES, label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**DATA SOURCE**")
    st.markdown(
        '<div style="color:#DCE6F4;font-size:12px;line-height:1.8">'
        '🇧🇷 Brazilian Olist E-Commerce<br>2016–2018<br><br>'
        'Display currency: INR<br>Source currency: BRL</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.caption("MARKETPULSE · PORTFOLIO PROJECT")

st.markdown(
    '<div class="page-title">MarketPulse</div>'
    '<div class="page-sub">Monitor performance. Understand customers. Make better decisions.</div>',
    unsafe_allow_html=True,
)
if MISSING:
    with st.expander(f"{len(FILES)-len(MISSING)} of {len(FILES)} analysis files loaded"):
        st.write("Missing or unreadable files:", MISSING)

# 1. OVERVIEW
if page == PAGES[0]:
    metrics([
        ("Total Revenue", f"₹{revenue_total/1e7:.2f} Cr", "💰"),
        ("Delivered Orders", f"{orders_total:,.0f}", "📦"),
        ("Unique Customers", f"{customers_total:,.0f}", "👥"),
        ("On-Time Delivery", f"{on_time_pct:.1f}%", "🚚"),
        ("Average Rating", f"{avg_rating:.2f}/5", "⭐"),
    ])
    st.caption(f"Revenue is converted from BRL at a fixed project rate of 1 BRL = ₹{BRL_TO_INR:.4f} (basis date: {RATE_BASIS_DATE}); not a live exchange rate.")
    section("Monthly Revenue Trend")
    plot(px.area(monthly, x="month", y="revenue", markers=True,
                 labels={"month": "Month", "revenue": "Revenue (INR)"}), 370)
    left, right = st.columns(2)
    with left:
        if not category.empty and "category" in category.columns:
            section("Top Revenue Categories")
            topcat = category.nlargest(10, "revenue").sort_values("revenue")
            plot(px.bar(topcat, x="revenue", y="category", orientation="h",
                        labels={"revenue": "Revenue (INR)", "category": "Category"}), 420)
    with right:
        if not segments.empty and {"customer_segment", "total_customers"}.issubset(segments.columns):
            section("Customer Segments")
            plot(px.pie(segments, names="customer_segment", values="total_customers", hole=.55), 420)
    if not monthly.empty:
        peak = monthly.loc[monthly["revenue"].idxmax(), "month"]
        st.markdown(f'<div class="insight">📈 Highest monthly revenue occurred in <b>{peak}</b>.</div>', unsafe_allow_html=True)

# 2. REVENUE
elif page == PAGES[1]:
    heading("Revenue Analytics", "Explore revenue trends, month-over-month growth and category performance.")
    months = monthly["month"].astype(str).tolist()
    chosen = st.multiselect("Select months", months, default=months)
    filtered = monthly[monthly["month"].astype(str).isin(chosen)].copy()
    if not filtered.empty:
        metrics([
            ("Revenue in Selection", f"₹{filtered['revenue'].sum()/1e7:.2f} Cr", "💰"),
            ("Highest Month", str(filtered.loc[filtered["revenue"].idxmax(), "month"]), "📈"),
            ("Lowest Month", str(filtered.loc[filtered["revenue"].idxmin(), "month"]), "📉"),
        ])
        section("Monthly Revenue")
        plot(px.line(filtered, x="month", y="revenue", markers=True,
                     labels={"revenue": "Revenue (INR)"}), 390)
    growth = monthly.copy()
    growth["previous_revenue"] = growth["revenue"].shift(1)
    growth["growth_percentage"] = (
        (growth["revenue"] - growth["previous_revenue"])
        / growth["previous_revenue"].replace(0, pd.NA) * 100
    )
    growth = growth[growth["month"].astype(str).isin(chosen)].dropna(subset=["growth_percentage"])
    growth = growth[growth["month"].astype(str) != "2017-01"]
    if not growth.empty:
        section("Month-over-Month Growth")
        fig = px.bar(growth, x="month", y="growth_percentage",
                     color="growth_percentage",
                     color_continuous_scale=["#E76F51", "#F4B942", "#12A892"],
                     labels={"growth_percentage": "Growth (%)"})
        fig.add_hline(y=0, line_dash="dash", line_color="#718096")
        plot(fig, 360)
    st.caption("January 2017 is excluded from the growth chart because the December 2016 base is exceptionally small.")
    if not category.empty:
        section("Category Revenue")
        selected_categories = st.multiselect("Filter categories", category["category"].tolist(),
                                              default=category["category"].tolist())
        cat_view = category[category["category"].isin(selected_categories)]
        plot(px.bar(cat_view.sort_values("revenue"), x="revenue", y="category", orientation="h",
                    labels={"revenue": "Revenue (INR)"}), 460)
    download(filtered, "marketpulse_revenue_inr.csv")
    download(growth, "marketpulse_growth_report.csv")

# 3. CUSTOMER ANALYTICS
elif page == PAGES[2]:
    heading("Customer Analytics", "Understand RFM segments and purchase behaviour.")
    if not segments.empty:
        metrics([
            ("Customers in Segments", f"{customers_total:,.0f}", "👥"),
            ("Segments", f"{segments['customer_segment'].nunique()}", "🧩"),
        ])
        section("RFM Customer Segments")
        plot(px.bar(segments.sort_values("total_customers"), x="total_customers",
                    y="customer_segment", orientation="h",
                    labels={"total_customers": "Customers", "customer_segment": "Segment"}), 430)
        st.dataframe(segments.sort_values("total_customers", ascending=False),
                     use_container_width=True, hide_index=True)
        download(segments, "rfm_customer_segments.csv")
    if not purchase.empty:
        section("One-Time vs Repeat Customers")
        if {"purchase_type", "total_customers"}.issubset(purchase.columns):
            plot(px.bar(purchase, x="purchase_type", y="total_customers",
                        color="purchase_type",
                        labels={"purchase_type": "Customer Type", "total_customers": "Customers"}), 350)
        st.dataframe(purchase, use_container_width=True, hide_index=True)
        download(purchase, "purchase_comparison_inr.csv")

# 4. CLV
elif page == PAGES[3]:
    heading("Customer Lifetime Value", "Historical customer revenue from delivered orders; not a forecast of future value.")
    if clv.empty:
        st.info("customer_clv.csv is not available.")
    else:
        metrics([
            ("Customers Analysed", f"{len(clv):,}", "👥"),
            ("Historical Revenue", f"₹{clv['total_revenue'].sum()/1e7:.2f} Cr", "💰"),
            ("Average Revenue / Customer", inr(clv["total_revenue"].mean()), "💎"),
            ("Repeat Customers", f"{(clv['total_orders'] > 1).sum():,}", "🔁"),
        ])
        section("Top 20 Customers by Historical Revenue")
        top = clv.nlargest(20, "total_revenue").copy()
        top["customer_label"] = top["customer_unique_id"].astype(str).str[:12]
        plot(px.bar(top.sort_values("total_revenue"), x="total_revenue", y="customer_label",
                    orientation="h", labels={"total_revenue": "Historical Revenue (INR)",
                    "customer_label": "Customer ID"}), 520)
        if not clv_summary.empty:
            section("Revenue-Based Customer Segments")
            if {"customer_segment", "total_revenue"}.issubset(clv_summary.columns):
                plot(px.bar(clv_summary, x="customer_segment", y="total_revenue",
                            color="customer_segment",
                            labels={"total_revenue": "Historical Revenue (INR)"}), 360)
            st.dataframe(clv_summary, use_container_width=True, hide_index=True)
        download(clv, "customer_clv_inr.csv")

# 5. RETENTION
elif page == PAGES[4]:
    heading("Customer Retention", "Track repeat purchasing and monthly active customer behaviour.")
    retention = get("retention")
    if isinstance(retention, pd.DataFrame) and not retention.empty:
        st.dataframe(retention, use_container_width=True, hide_index=True)
        if {"metric", "value"}.issubset(retention.columns):
            values = dict(zip(retention["metric"], retention["value"]))
            metrics([
                ("Total Customers", f"{int(values.get('Total Customers', 0)):,}", "👥"),
                ("Repeat Customers", f"{int(values.get('Repeat Customers', 0)):,}", "🔁"),
                ("Repeat Purchase Rate", f"{float(values.get('Repeat Purchase Rate', 0)):.2f}%", "📊"),
                ("One-Time Rate", f"{float(values.get('One-Time Customer Rate', 0)):.2f}%", "🛒"),
            ])
    if has("monthly_customers"):
        mc = get("monthly_customers")
        section("Monthly Active Customers")
        plot(px.line(mc, x="purchase_month", y="active_customers", markers=True,
                     labels={"purchase_month": "Month", "active_customers": "Active Customers"}), 370)
    if has("monthly_new_returning"):
        mnr = get("monthly_new_returning")
        section("New vs Returning Customers")
        if {"purchase_month", "customer_type", "customer_count"}.issubset(mnr.columns):
            plot(px.bar(mnr, x="purchase_month", y="customer_count", color="customer_type",
                        barmode="stack",
                        labels={"purchase_month": "Month", "customer_count": "Customers",
                                "customer_type": "Customer Type"}), 410)
        download(mnr, "monthly_new_returning.csv")
    if has("frequency"):
        freq = get("frequency")
        section("Customer Purchase Frequency")
        if "purchase_type" in freq.columns:
            counts = freq["purchase_type"].value_counts().rename_axis("purchase_type").reset_index(name="customers")
            plot(px.pie(counts, names="purchase_type", values="customers", hole=.55), 350)
        download(freq, "customer_frequency.csv")

# 6. PRODUCT
elif page == PAGES[5]:
    heading("Product Analytics", "Compare category revenue and identify best-selling products.")
    if not category_advanced.empty:
        metrics([
            ("Categories", f"{len(category_advanced):,}", "🗂️"),
            ("Category Revenue", f"₹{category_advanced['total_revenue'].sum()/1e7:.2f} Cr", "💰"),
            ("Items Sold", f"{category_advanced['total_items_sold'].sum():,.0f}", "📦"),
        ])
        section("Category Revenue Performance")
        top = category_advanced.nlargest(15, "total_revenue").sort_values("total_revenue")
        plot(px.bar(top, x="total_revenue", y="product_category_name_english", orientation="h",
                    labels={"total_revenue": "Revenue (INR)",
                            "product_category_name_english": "Category"}), 500)
        if "revenue_percentage" in category_advanced.columns:
            section("Category Revenue Share")
            plot(px.bar(category_advanced.nlargest(12, "revenue_percentage"),
                        x="product_category_name_english", y="revenue_percentage",
                        labels={"revenue_percentage": "Revenue Share (%)",
                                "product_category_name_english": "Category"}), 380)
        download(category_advanced, "category_performance_inr.csv")
    if not products.empty:
        section("Best-Selling Products")
        top_products = products.nlargest(15, "total_items_sold").sort_values("total_items_sold")
        plot(px.bar(top_products, x="total_items_sold", y="product_id", orientation="h",
                    labels={"total_items_sold": "Items Sold", "product_id": "Product ID"}), 500)
        st.dataframe(products.nlargest(20, "total_revenue"), use_container_width=True, hide_index=True)
        download(products, "product_performance_inr.csv")
    if not low_categories.empty:
        section("Lowest-Revenue Categories")
        st.dataframe(low_categories, use_container_width=True, hide_index=True)
        download(low_categories, "low_performing_categories_inr.csv")

# 7. SELLERS
elif page == PAGES[6]:
    heading("Seller Performance", "Understand seller revenue, order activity and state contribution.")
    if not sellers.empty:
        metrics([
            ("Sellers Analysed", f"{sellers['seller_id'].nunique():,}", "🏪"),
            ("Seller Item Revenue", f"₹{sellers['total_revenue'].sum()/1e7:.2f} Cr", "💰"),
            ("Seller-Associated Orders", f"{sellers['total_orders'].sum():,.0f}", "📦"),
            ("Items Sold", f"{sellers['total_items_sold'].sum():,.0f}", "🛍️"),
        ])
        section("Top 15 Sellers by Item Revenue")
        top_sellers = sellers.nlargest(15, "total_revenue").copy()
        top_sellers["seller_label"] = top_sellers["seller_id"].astype(str).str[:12]
        plot(px.bar(top_sellers.sort_values("total_revenue"), x="total_revenue",
                    y="seller_label", orientation="h",
                    labels={"total_revenue": "Item Revenue (INR)", "seller_label": "Seller ID"}), 480)
        st.dataframe(sellers.nlargest(25, "total_revenue"), use_container_width=True, hide_index=True)
        st.caption("Seller item revenue uses item price and excludes freight. Seller-associated orders can include the same order for multiple sellers.")
        download(sellers, "seller_analysis_inr.csv")
    if not seller_states.empty:
        section("Seller Performance by State")
        metrics([
            ("States", f"{seller_states['seller_state'].nunique()}", "🗺️"),
            ("Sellers", f"{seller_states['total_sellers'].sum():,}", "🏪"),
            ("Seller Item Revenue", f"₹{seller_states['total_revenue'].sum()/1e7:.2f} Cr", "💰"),
        ])
        plot(px.bar(seller_states.nlargest(12, "total_revenue").sort_values("total_revenue"),
                    x="total_revenue", y="seller_state", orientation="h",
                    labels={"total_revenue": "Item Revenue (INR)", "seller_state": "State"}), 430)
        download(seller_states, "seller_state_analysis_inr.csv")

# 8. GEOGRAPHY
elif page == PAGES[7]:
    heading("Geographic Analytics", "Explore customer revenue and order distribution across Brazilian states.")
    if geography.empty:
        st.info("geographic_sales.csv is not available.")
    else:
        metrics([
            ("States", f"{geography['state'].nunique()}", "🗺️"),
            ("Revenue", f"₹{geography['total_revenue'].sum()/1e7:.2f} Cr", "💰"),
            ("Orders", f"{geography['total_orders'].sum():,.0f}", "📦"),
            ("Customers", f"{geography['total_customers'].sum():,.0f}", "👥"),
        ])
        section("Revenue by State")
        plot(px.bar(geography.nlargest(15, "total_revenue").sort_values("total_revenue"),
                    x="total_revenue", y="state", orientation="h",
                    labels={"total_revenue": "Revenue (INR)", "state": "State"}), 500)
        section("Orders by State")
        plot(px.bar(geography.nlargest(15, "total_orders").sort_values("total_orders"),
                    x="total_orders", y="state", orientation="h",
                    labels={"total_orders": "Orders", "state": "State"}), 500)
        st.dataframe(geography.sort_values("total_revenue", ascending=False),
                     use_container_width=True, hide_index=True)
        download(geography, "geographic_sales_inr.csv")

# 9. PAYMENTS
elif page == PAGES[8]:
    heading("Payment Analytics", "Understand payment methods, transaction volume and average payment.")
    if payments.empty:
        st.info("payment_analysis.csv is not available.")
    else:
        metrics([
            ("Payment Value", f"₹{payments['total_payment_value'].sum()/1e7:.2f} Cr", "💳"),
            ("Payment Transactions", f"{payments['total_transactions'].sum():,.0f}", "🧾"),
            ("Orders with Payments", f"{payments['total_orders'].sum():,.0f}", "📦"),
            ("Payment Methods", f"{payments['payment_type'].nunique()}", "🏦"),
        ])
        section("Payment Value by Method")
        plot(px.bar(payments.sort_values("total_payment_value"), x="total_payment_value",
                    y="payment_type", orientation="h",
                    labels={"total_payment_value": "Payment Value (INR)",
                            "payment_type": "Payment Method"}), 420)
        left, right = st.columns(2)
        with left:
            section("Transaction Mix")
            plot(px.pie(payments, names="payment_type", values="total_transactions", hole=.55), 360)
        with right:
            section("Average Payment")
            plot(px.bar(payments, x="payment_type", y="average_payment",
                        labels={"average_payment": "Average Payment (INR)",
                                "payment_type": "Payment Method"}), 360)
        if "average_installments" in payments.columns:
            section("Average Installments")
            plot(px.bar(payments, x="payment_type", y="average_installments",
                        labels={"average_installments": "Average Installments",
                                "payment_type": "Payment Method"}), 340)
        st.dataframe(payments, use_container_width=True, hide_index=True)
        st.caption("Payment transaction count and distinct order count are different measures; an order may have multiple payment records.")
        download(payments, "payment_analysis_inr.csv")

# 10. OPERATIONS
elif page == PAGES[9]:
    heading("Operations & Delivery", "Monitor delivery outcomes and fulfilment performance.")
    late_count = 0
    if {"delivery_status", "total_orders"}.issubset(delivery.columns):
        late_count = delivery.loc[
            delivery["delivery_status"].astype(str).str.lower().eq("late"), "total_orders"
        ].sum()
    metrics([
        ("Delivered Orders Analysed", f"{orders_total:,.0f}", "📦"),
        ("On-Time Delivery", f"{on_time_pct:.2f}%", "🚚"),
        ("Late Orders", f"{late_count:,.0f}", "⏱️"),
    ])
    section("Delivery Performance")
    if {"delivery_status", "total_orders"}.issubset(delivery.columns):
        plot(px.pie(delivery, names="delivery_status", values="total_orders", hole=.55,
                    color="delivery_status",
                    color_discrete_map={"On Time": "#12A892", "Late": "#E76F51"}), 370)
    st.dataframe(delivery, use_container_width=True, hide_index=True)
    download(delivery, "delivery_performance.csv")

# 11. SATISFACTION
elif page == PAGES[10]:
    heading("Customer Satisfaction", "Explore review scores and delivery satisfaction.")
    if not reviews.empty:
        review_count = pd.to_numeric(reviews["total_reviews"], errors="coerce").sum()
        five_star = reviews.loc[reviews["review_score"] == 5, "total_reviews"].sum()
        metrics([
            ("Total Reviews", f"{review_count:,.0f}", "⭐"),
            ("Average Rating", f"{avg_rating:.2f}/5", "🌟"),
            ("Five-Star Reviews", f"{five_star:,.0f}", "🏆"),
        ])
        section("Review Score Distribution")
        plot(px.bar(reviews, x="review_score", y="total_reviews",
                    labels={"review_score": "Review Score", "total_reviews": "Reviews"}), 370)
        st.dataframe(reviews, use_container_width=True, hide_index=True)
        download(reviews, "review_distribution.csv")
    if not satisfaction.empty:
        section("Delivery Status vs Average Review")
        plot(px.bar(satisfaction, x="delivery_status", y="average_review_score",
                    color="delivery_status",
                    color_discrete_map={"On Time": "#176B87", "Late": "#E76F51"},
                    labels={"delivery_status": "Delivery Status",
                            "average_review_score": "Average Review Score"}), 370)
        st.markdown(
            '<div class="insight">💡 Delivery delays are associated with lower average review scores in this dataset. '
            'This association does not establish causation.</div>',
            unsafe_allow_html=True,
        )
        download(satisfaction, "delivery_satisfaction.csv")

st.markdown("---")
st.markdown(
    '<div class="footer"><b>MARKETPULSE</b><br>BUSINESS & CUSTOMER INTELLIGENCE PLATFORM<br><br>'
    'Built with Python · SQL · PostgreSQL · Pandas · Plotly · Streamlit</div>',
    unsafe_allow_html=True,
)
