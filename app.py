import random
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st
from sklearn.ensemble import IsolationForest
from streamlit_autorefresh import st_autorefresh


st.set_page_config(page_title="Fin-Sentinel", layout="wide")


st.markdown(
    """
    <style>
    :root {
        --bg: #081120;
        --panel: rgba(12, 23, 42, 0.86);
        --panel-strong: rgba(15, 30, 56, 0.96);
        --border: rgba(148, 163, 184, 0.16);
        --text: #e5eefc;
        --muted: #8fa6c8;
        --blue: #45c2ff;
        --cyan: #7ce7ff;
        --red: #ff6b81;
        --amber: #ffb85c;
        --green: #29d391;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(69, 194, 255, 0.14), transparent 30%),
            radial-gradient(circle at top right, rgba(255, 107, 129, 0.10), transparent 28%),
            linear-gradient(180deg, #07101d 0%, #0b1730 52%, #091120 100%);
        color: var(--text);
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1220px;
    }

    h1, h2, h3 {
        color: #f7fbff;
        letter-spacing: -0.02em;
    }

    p, li, label {
        color: var(--text);
    }

    [data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(15, 30, 56, 0.95), rgba(10, 21, 39, 0.95));
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.22);
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #f8fbff;
        font-weight: 700;
    }

    div[data-testid="stVerticalBlock"] > div:has(> div.section-card) {
        margin-bottom: 1rem;
    }

    .hero-card,
    .section-card,
    .glass-card {
        border: 1px solid var(--border);
        background: linear-gradient(180deg, rgba(14, 26, 49, 0.95), rgba(8, 18, 32, 0.95));
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.24);
        animation: riseIn 360ms ease-out both;
    }

    .hero-card {
        padding: 1.5rem 1.6rem;
        margin-bottom: 1.25rem;
        overflow: hidden;
        position: relative;
    }

    .hero-card::after {
        content: "";
        position: absolute;
        inset: auto -80px -80px auto;
        width: 220px;
        height: 220px;
        border-radius: 999px;
        background: radial-gradient(circle, rgba(69, 194, 255, 0.20), transparent 70%);
    }

    .section-card {
        padding: 1.2rem 1.25rem 0.4rem 1.25rem;
        margin: 0.7rem 0 1.25rem 0;
    }

    .glass-card {
        padding: 1rem 1.1rem;
    }

    .eyebrow {
        color: var(--cyan);
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-size: 0.76rem;
        font-weight: 700;
        margin-bottom: 0.45rem;
    }

    .hero-title {
        font-size: 2.5rem;
        line-height: 1;
        margin: 0;
        font-weight: 800;
    }

    .hero-subtitle {
        margin: 0.8rem 0 0 0;
        color: var(--muted);
        max-width: 760px;
        font-size: 1rem;
        line-height: 1.6;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 750;
        margin-bottom: 0.2rem;
    }

    .section-copy {
        color: var(--muted);
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }

    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-top: 1rem;
    }

    .pill {
        border: 1px solid rgba(124, 231, 255, 0.2);
        background: rgba(124, 231, 255, 0.08);
        color: #dff9ff;
        padding: 0.45rem 0.75rem;
        border-radius: 999px;
        font-size: 0.84rem;
    }

    .status-strip {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.8rem;
        margin-top: 0.9rem;
    }

    .status-chip {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 0.85rem 0.95rem;
    }

    .status-chip strong {
        display: block;
        color: #f7fbff;
        font-size: 1rem;
    }

    .status-chip span {
        color: var(--muted);
        font-size: 0.85rem;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="slider"] {
        border-radius: 14px !important;
    }

    .stButton button {
        border-radius: 14px;
        border: 1px solid rgba(124, 231, 255, 0.24);
        background: linear-gradient(135deg, #10284d, #123765);
        color: #f7fbff;
        font-weight: 700;
        padding: 0.65rem 1.05rem;
        transition: all 0.18s ease;
    }

    .stButton button:hover {
        border-color: rgba(124, 231, 255, 0.42);
        transform: translateY(-1px);
        box-shadow: 0 10px 24px rgba(18, 55, 101, 0.28);
    }

    .live-toolbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border: 1px solid var(--border);
        border-radius: 16px;
        background: rgba(11, 23, 42, 0.8);
        padding: 0.65rem 0.85rem;
        margin-bottom: 0.8rem;
        animation: riseIn 360ms ease-out both;
    }

    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        color: #d6f7ff;
        font-size: 0.85rem;
    }

    .live-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--green);
        box-shadow: 0 0 0 0 rgba(41, 211, 145, 0.7);
        animation: pulseDot 1.8s infinite;
    }

    div[data-testid="stTable"] table {
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
    }

    div[data-testid="stTable"] thead tr th {
        background: rgba(69, 194, 255, 0.08);
        color: #d8ebff;
        border-bottom: 1px solid var(--border);
    }

    div[data-testid="stTable"] tbody tr td {
        background: rgba(255, 255, 255, 0.02);
        color: #ebf3ff;
        border-bottom: 1px solid rgba(148, 163, 184, 0.08);
    }

    @media (max-width: 900px) {
        .hero-title {
            font-size: 2rem;
        }

        .status-strip {
            grid-template-columns: 1fr;
        }
    }

    @keyframes riseIn {
        from {
            transform: translateY(8px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }

    @keyframes pulseDot {
        0% {
            box-shadow: 0 0 0 0 rgba(41, 211, 145, 0.68);
        }
        70% {
            box-shadow: 0 0 0 9px rgba(41, 211, 145, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(41, 211, 145, 0);
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    local_path = Path(__file__).with_name("creditcard.csv")

    if local_path.exists():
        return pd.read_csv(local_path)

    url = "https://drive.google.com/uc?id=1R3a_Cwv_gmoBxBat0S0c_G5TquJ5XzLd"
    return pd.read_csv(url)


@st.cache_resource
def train_model(frame: pd.DataFrame):
    feature_cols = [column for column in frame.columns if column != "Class"]
    features = frame[feature_cols].copy()
    fitted_model = IsolationForest(contamination=0.002, random_state=42)
    fitted_model.fit(features)
    score_values = fitted_model.decision_function(features)
    return fitted_model, feature_cols, score_values


def section_intro(title: str, copy: str):
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-title">{title}</div>
            <div class="section-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_altair(chart: alt.Chart) -> alt.Chart:
    return chart.configure(
        background="transparent",
        padding={"left": 10, "right": 10, "top": 10, "bottom": 0},
    ).configure_axis(
        labelColor="#c8d8ee",
        titleColor="#c8d8ee",
        gridColor="rgba(148, 163, 184, 0.16)",
        domain=False,
        tickColor="rgba(148, 163, 184, 0.16)",
    ).configure_view(
        strokeOpacity=0
    ).configure_title(
        color="#f7fbff",
        fontSize=16,
        anchor="start",
    ).configure_legend(
        labelColor="#d9e8fb",
        titleColor="#d9e8fb",
    )


data = load_data()
model_data = data.copy()

if "transaction_count" not in st.session_state:
    st.session_state.transaction_count = 0

if "last_risk_score" not in st.session_state:
    st.session_state.last_risk_score = None

if "sim_influence" not in st.session_state:
    st.session_state.sim_influence = 0.0

if "sim_context" not in st.session_state:
    st.session_state.sim_context = {
        "merchant": None,
        "city": None,
        "amount": 0,
        "late_night": False,
        "repeat_attempt": False,
        "decision": "Baseline monitoring",
    }

model, feature_columns, scores = train_model(model_data)
data["fraud_probability"] = 1 - scores

total_transactions = len(data)
fraud_transactions = len(data[data["Class"] == 1])
fraud_rate = (fraud_transactions / total_transactions) * 100
average_amount = data["Amount"].mean()

st.markdown(
    f"""
    <div class="hero-card">
        <div class="eyebrow">Real-Time Risk Command Center</div>
        <h1 class="hero-title">Fin-Sentinel</h1>
        <p class="hero-subtitle">
            This dashboard simulates a fintech fraud monitoring system used to detect suspicious payment activity in real time.
        </p>
        <div class="pill-row">
            <div class="pill">Isolation Forest Monitoring</div>
            <div class="pill">Behavioral Anomaly Signals</div>
            <div class="pill">Live Investigation Workflow</div>
        </div>
        <div class="status-strip">
            <div class="status-chip">
                <strong>{total_transactions:,}</strong>
                <span>Transactions in scope</span>
            </div>
            <div class="status-chip">
                <strong>{fraud_rate:.2f}%</strong>
                <span>Observed fraud rate</span>
            </div>
            <div class="status-chip">
                <strong>₹{average_amount:,.0f}</strong>
                <span>Average transaction amount</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

toolbar_left, toolbar_mid, toolbar_right = st.columns([1.45, 1.2, 1.1])
with toolbar_left:
    st.markdown(
        """
        <div class="live-toolbar">
            <div class="live-badge">
                <span class="live-dot"></span>
                Live monitoring active
            </div>
            <div style="color:#8fa6c8;font-size:0.83rem;">Premium demo mode</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with toolbar_mid:
    auto_refresh_enabled = st.toggle("Auto-refresh feed", value=True)
with toolbar_right:
    refresh_seconds = st.selectbox("Refresh every", [8, 12, 20, 30, 45, 60], index=1)

if auto_refresh_enabled:
    st_autorefresh(interval=refresh_seconds * 1000, key="dashboard_refresh_timer")


section_intro(
    "Executive Risk Overview",
    "Core business indicators to orient investigators before drilling into live alerts and patterns.",
)

metric_cols = st.columns(4)
metric_cols[0].metric("Total Transactions", f"{total_transactions:,}")
metric_cols[1].metric("Fraud Cases", f"{fraud_transactions:,}")
metric_cols[2].metric("Fraud Rate", f"{fraud_rate:.2f}%")
metric_cols[3].metric("Simulations Run", st.session_state.transaction_count)


section_intro(
    "Fraud Intelligence Signals",
    "High-value behavior and model-based risk help surface where review capacity should focus first.",
)

high_value = data[data["Amount"] > 5000]
dynamic_threshold = max(0.45, 0.7 - (st.session_state.sim_influence * 0.2))
high_risk = high_value[high_value["fraud_probability"] > dynamic_threshold]
signal_cols = st.columns(3)
signal_cols[0].metric("High Value Transactions", f"{len(high_value):,}", "> ₹5,000")
signal_cols[1].metric("High Risk in This Band", f"{len(high_risk):,}")
signal_rate = (len(high_risk) / len(high_value)) * 100 if len(high_value) > 0 else 0
signal_cols[2].metric("High-Value Risk Rate", f"{signal_rate:.2f}%", f"Threshold {dynamic_threshold:.2f}")


section_intro(
    "Live Fraud Monitoring Feed",
    "A compact watchlist of simulated alerts with clearer severity and faster scanning.",
)

merchants = [
    "Amazon",
    "Flipkart",
    "Swiggy",
    "Zomato",
    "Steam Games",
    "Luxury Watches",
    "Crypto Exchange",
    "Electronics Hub",
]
cities = ["Bangalore", "Delhi", "Mumbai", "Hyderabad", "Chennai"]

alerts = []
sim_boost = int(st.session_state.sim_influence * 26)
focus_merchant = st.session_state.sim_context["merchant"]
focus_city = st.session_state.sim_context["city"]
for _ in range(6):
    merchant_choice = random.choice(merchants)
    city_choice = random.choice(cities)
    context_bonus = 0
    if focus_merchant and merchant_choice == focus_merchant:
        context_bonus += 12
    if focus_city and city_choice == focus_city:
        context_bonus += 10
    risk = min(99, random.randint(20, 95) + sim_boost + context_bonus)
    if risk >= 75:
        status = "High Risk"
    elif risk >= 45:
        status = "Medium Risk"
    else:
        status = "Normal"

    alerts.append(
        {
            "Transaction ID": random.randint(100000, 999999),
            "Amount (₹)": random.randint(100, 50000),
            "Merchant": merchant_choice,
            "City": city_choice,
            "Risk Score": risk,
            "Alert Status": status,
        }
    )

alerts_df = pd.DataFrame(alerts).sort_values("Risk Score", ascending=False)
feed_left, feed_right = st.columns([1.6, 1])

with feed_left:
    st.table(alerts_df)

with feed_right:
    watchlist_chart = style_altair(
        alt.Chart(alerts_df)
        .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
        .encode(
            x=alt.X("Risk Score:Q", scale=alt.Scale(domain=[0, 100])),
            y=alt.Y("Merchant:N", sort="-x", title=None),
            color=alt.Color(
                "Alert Status:N",
                scale=alt.Scale(
                    domain=["Normal", "Medium Risk", "High Risk"],
                    range=["#2dd4bf", "#ffb85c", "#ff6b81"],
                ),
                legend=None,
            ),
            tooltip=["Merchant", "City", "Risk Score", "Alert Status"],
        )
        .properties(height=280, title="Alert Severity by Merchant")
    )
    st.altair_chart(watchlist_chart, use_container_width=True)


section_intro(
    "Risk Landscape",
    "Merchant and location signals arranged side by side for faster pattern recognition.",
)

merchant_risk = {merchant: random.randint(5, 90) for merchant in merchants}
city_risk = {city: random.randint(20, 80) for city in cities}
if focus_merchant in merchant_risk:
    merchant_risk[focus_merchant] = min(99, merchant_risk[focus_merchant] + int(22 * st.session_state.sim_influence))
if focus_city in city_risk:
    city_risk[focus_city] = min(99, city_risk[focus_city] + int(18 * st.session_state.sim_influence))

merchant_df = pd.DataFrame(
    {
        "Merchant": merchants,
        "Risk Score": [merchant_risk[merchant] for merchant in merchants],
    }
).sort_values("Risk Score", ascending=False)

city_df = pd.DataFrame(
    {
        "City": cities,
        "Risk Score": [city_risk[city] for city in cities],
    }
).sort_values("Risk Score", ascending=False)

risk_left, risk_right = st.columns([1, 1.1])

with risk_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Merchant Risk Monitoring")
    st.table(merchant_df)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card" style="margin-top:0.9rem;">', unsafe_allow_html=True)
    st.subheader("High Risk Merchants")
    high_risk_merchants = merchant_df[merchant_df["Risk Score"] >= 70]
    st.table(high_risk_merchants if not high_risk_merchants.empty else merchant_df.head(3))
    st.markdown("</div>", unsafe_allow_html=True)

with risk_right:
    city_chart = style_altair(
        alt.Chart(city_df)
        .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
        .encode(
            x=alt.X("City:N", sort=None, title=None),
            y=alt.Y("Risk Score:Q", title="Risk Score"),
            color=alt.Color("Risk Score:Q", scale=alt.Scale(scheme="teals")),
            tooltip=["City", "Risk Score"],
        )
        .properties(height=390, title="City Fraud Risk Ranking")
    )
    st.altair_chart(city_chart, use_container_width=True)


section_intro(
    "Transaction Behavior Analytics",
    "Two views of the dataset: overall class balance and where fraud rate rises with transaction size.",
)

fraud_counts = data["Class"].value_counts().reset_index()
fraud_counts.columns = ["Transaction Type", "Count"]
fraud_counts["Transaction Type"] = fraud_counts["Transaction Type"].map({0: "Normal", 1: "Fraud"})

data["amount_bucket"] = pd.cut(
    data["Amount"],
    bins=[0, 1000, 5000, 10000, 50000],
    labels=["0-1k", "1k-5k", "5k-10k", "10k+"],
).astype(str)

fraud_rate_bucket = (
    data.groupby("amount_bucket", dropna=False)["Class"].mean().mul(100).reset_index()
)
fraud_rate_bucket.columns = ["Amount Range", "Fraud Rate (%)"]

analytics_left, analytics_right = st.columns(2)

with analytics_left:
    transaction_chart = style_altair(
        alt.Chart(fraud_counts)
        .mark_arc(innerRadius=70, outerRadius=120)
        .encode(
            theta=alt.Theta("Count:Q"),
            color=alt.Color(
                "Transaction Type:N",
                scale=alt.Scale(domain=["Normal", "Fraud"], range=["#45c2ff", "#ff6b81"]),
                legend=alt.Legend(orient="bottom"),
            ),
            tooltip=["Transaction Type", "Count"],
        )
        .properties(height=320, title="Transaction Type Distribution")
    )
    st.altair_chart(transaction_chart, use_container_width=True)

with analytics_right:
    bucket_chart = style_altair(
        alt.Chart(fraud_rate_bucket)
        .mark_line(point=alt.OverlayMarkDef(size=90, filled=True), strokeWidth=3)
        .encode(
            x=alt.X("Amount Range:N", sort=None),
            y=alt.Y("Fraud Rate (%):Q"),
            color=alt.value("#7ce7ff"),
            tooltip=["Amount Range", "Fraud Rate (%)"],
        )
        .properties(height=320, title="Fraud Rate by Transaction Amount")
    )
    st.altair_chart(bucket_chart, use_container_width=True)


section_intro(
    "Fraud Network Investigation",
    "A relationship map showing where merchants and cities accumulate suspicious transactions.",
)

network_rows = []
merchant_risk_map = dict(zip(merchant_df["Merchant"], merchant_df["Risk Score"]))
city_risk_map = dict(zip(city_df["City"], city_df["Risk Score"]))

for index in range(18):
    city = random.choice(cities)
    merchant = random.choice(merchants[:6])
    risk_score = round(min(0.99, random.random() + (st.session_state.sim_influence * 0.28)), 2)
    if focus_merchant and merchant == focus_merchant:
        risk_score = round(min(0.99, risk_score + 0.11), 2)
    if focus_city and city == focus_city:
        risk_score = round(min(0.99, risk_score + 0.09), 2)
    network_rows.append(
        {
            "Transaction ID": f"TX-{1000 + index}",
            "City": city,
            "Merchant": merchant,
            "Merchant Risk": merchant_risk_map.get(merchant, 0),
            "City Risk": city_risk_map.get(city, 0),
            "Transaction Risk": risk_score,
            "Status": "High Risk" if risk_score > 0.7 else "Normal",
        }
    )

network_df = pd.DataFrame(network_rows)

network_left, network_right = st.columns([1.25, 0.9])

with network_left:
    network_chart = style_altair(
        alt.Chart(network_df)
        .mark_circle(size=230, opacity=0.86)
        .encode(
            x=alt.X("Merchant:N", sort=None),
            y=alt.Y("City:N", sort=None),
            color=alt.Color(
                "Transaction Risk:Q",
                scale=alt.Scale(domain=[0, 1], range=["#29d391", "#ffb85c", "#ff6b81"]),
            ),
            size=alt.Size("Merchant Risk:Q", scale=alt.Scale(range=[100, 650]), legend=None),
            tooltip=[
                "Transaction ID",
                "City",
                "Merchant",
                "Merchant Risk",
                "City Risk",
                "Transaction Risk",
                "Status",
            ],
        )
        .properties(height=360, title="Merchant and City Relationship Map")
    )
    st.altair_chart(network_chart, use_container_width=True)

with network_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Investigation Insights")
    st.markdown(
        """
        - Multiple high-risk transactions around one merchant can suggest merchant compromise.
        - Location clusters can point to region-specific fraud activity.
        - Elevated merchant and city risk together deserve faster manual review.
        """
    )
    st.table(network_df[["Transaction ID", "Merchant", "City", "Status"]].head(6))
    st.markdown("</div>", unsafe_allow_html=True)


section_intro(
    "Fraud Investigation Simulator",
    "Run a smoother scenario check using transaction context, then summarize the result in a review-ready format.",
)

sim_left, sim_right = st.columns([1.1, 0.9])

with sim_left:
    amount = st.slider("Transaction Amount (₹)", 10, 50000, 3500, step=250)
    merchant_category = st.selectbox("Merchant", merchants)
    location = st.selectbox("Location", cities)
    late_night = st.toggle("Late-night transaction pattern", value=False)
    repeat_attempt = st.toggle("Repeated attempt from same customer", value=False)
    submitted = st.button("Run Fraud Check", use_container_width=True)

with sim_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Simulation Guidance")
    st.caption("Use the toggles to mimic more suspicious behavior and compare the resulting score.")
    st.markdown(
        f"""
        - Selected merchant: **{merchant_category}**
        - Selected city: **{location}**
        - Transaction amount: **₹{amount:,.0f}**
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    st.session_state.transaction_count += 1

    sample = model_data[model_data["Class"] == 0].sample(1).copy()
    x_sample = sample[feature_columns].copy()
    baseline_score = model.decision_function(x_sample)[0]

    merchant_risk_boost = merchant_risk.get(merchant_category, 0) * 0.18
    city_risk_boost = city_risk.get(location, 0) * 0.12
    amount_boost = min(amount / 1000, 50) * 0.55
    behavior_boost = (12 if late_night else 0) + (16 if repeat_attempt else 0)
    risk_score = int((0.5 - baseline_score) * 100 + merchant_risk_boost + city_risk_boost + amount_boost + behavior_boost)
    risk_score = max(1, min(risk_score, 99))
    st.session_state.last_risk_score = risk_score
    st.session_state.sim_influence = min(1.0, risk_score / 100)
    st.session_state.sim_context = {
        "merchant": merchant_category,
        "city": location,
        "amount": amount,
        "late_night": late_night,
        "repeat_attempt": repeat_attempt,
        "decision": "Pending",
    }
    st.rerun()

if st.session_state.last_risk_score is not None:
    risk_score = st.session_state.last_risk_score
    result_left, result_right = st.columns([1, 1])

    with result_left:
        st.metric("Fraud Risk Score", f"{risk_score}/100")
        st.progress(risk_score / 100)

        if risk_score >= 75:
            st.error("Escalate this transaction for immediate manual review.")
            decision_label = "Immediate review"
        elif risk_score >= 45:
            st.warning("This transaction shows medium-risk behavior and should be monitored.")
            decision_label = "Monitor closely"
        else:
            st.success("This transaction appears relatively normal for the current profile.")
            decision_label = "Allow with monitoring"
        st.session_state.sim_context["decision"] = decision_label

    with result_right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Decision Summary")
        st.markdown(
            f"""
            - Recommended action: **{decision_label}**
            - Merchant context: **{merchant_category}**
            - Location context: **{location}**
            - Transaction amount: **₹{amount:,.0f}**
            - Behavioral flags: **{"Late-night" if late_night else "No"}**, **{"Repeated attempt" if repeat_attempt else "No"}**
            """
        )
        st.markdown("</div>", unsafe_allow_html=True)

section_intro(
    "Simulation Impact Snapshot",
    "Simulator outcomes now feed the live dashboard, shifting alert pressure and location or merchant concentration in real time.",
)
impact_left, impact_mid, impact_right = st.columns(3)
impact_left.metric("Dashboard Pressure", f"{int(st.session_state.sim_influence * 100)}%")
impact_mid.metric("Focused Merchant", st.session_state.sim_context["merchant"] or "None")
impact_right.metric("Focused City", st.session_state.sim_context["city"] or "None")
