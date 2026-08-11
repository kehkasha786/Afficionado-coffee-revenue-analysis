import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Afficionado Coffee Roasters",
    page_icon="☕",
    layout="wide"
)

# ============================================================
# GLOBAL CHART STYLE - clean, neutral, single accent color
# ============================================================
px.defaults.template = "plotly_white"

ACCENT = "#3B5A6B"        # muted slate blue - primary bars
ALERT = "#B0413E"         # muted red - long-tail / underperforming
HERO_BG = "#E7F0EA"       # light green tint - hero products table
UNDER_BG = "#FBEAEA"      # light red tint - underperforming table
NEUTRAL_SEQUENCE = [
    "#3B5A6B", "#5C7C8A", "#8AA6B3", "#B4C7CF",
    "#6B6B6B", "#9C9C9C", "#C6C6C6", "#D8D8D8", "#E5E5E5"
]

# Get the folder where app.py is located
BASE_DIR = Path(__file__).parent


@st.cache_data
def load_data(path):
    return pd.read_csv(path)


df_raw = load_data(BASE_DIR / "cleaned_coffee_sales.csv")

# ============================================================
# SIDEBAR - NAVIGATION FIRST
# ============================================================
st.sidebar.title("☕ Afficionado Coffee Roasters")

page = st.sidebar.radio(
    "🧭 Navigate Dashboard",
    [
        "Page 1 - Business Overview",
        "Page 2 - Product Performance",
        "Page 3 - Revenue Concentration"
    ]
)

st.sidebar.divider()

# ============================================================
# SIDEBAR - FILTERS (SLICERS) - collapsed by default, compact
# ============================================================
store_options = sorted(df_raw["store_location"].unique())
category_options = sorted(df_raw["product_category"].unique())

with st.sidebar.expander("🔎 Filters", expanded=False):
    selected_stores = st.multiselect(
        "🏬 Store Location",
        options=store_options,
        default=store_options
    )

    selected_categories = st.multiselect(
        "📦 Product Category",
        options=category_options,
        default=category_options
    )

    # Product Type list depends on selected categories
    type_options = sorted(
        df_raw[df_raw["product_category"].isin(selected_categories)]["product_type"].unique()
    )

    selected_types = st.multiselect(
        "☕ Product Type",
        options=type_options,
        default=type_options
    )

    top_n = st.slider(
        "🔟 Top-N Products (applies to ranking charts & tables)",
        min_value=5,
        max_value=20,
        value=10,
        step=1
    )

# Apply filters
df = df_raw[
    (df_raw["store_location"].isin(selected_stores)) &
    (df_raw["product_category"].isin(selected_categories)) &
    (df_raw["product_type"].isin(selected_types))
]

st.sidebar.caption(f"Showing {len(df):,} of {len(df_raw):,} transactions")

st.sidebar.markdown("---")
st.sidebar.caption(
    "Built by Kehkasha Ansari  \n"
    "Business Analyst Intern, Unified Mentor  \n"
    "Capstone Project · 2026"
)

# Guard against empty selections after filtering
if df.empty:
    st.warning("No data matches the current filters. Please adjust the filters in the sidebar.")
    st.stop()

# ============================================================
# PAGE 1 - BUSINESS OVERVIEW
# ============================================================
if page == "Page 1 - Business Overview":
    st.title("☕ Afficionado Coffee Roasters")
    st.subheader("Product Optimization & Revenue Contribution Analysis")

    n_stores = df["store_location"].nunique()
    n_products = df["product_id"].nunique()
    n_categories = df["product_category"].nunique()

    st.markdown(
        f"📅 **Data Period:** {int(df['year'].min())}"
        + (f"–{int(df['year'].max())}" if df['year'].min() != df['year'].max() else "")
        + f"  |  🏬 **Store Locations:** {n_stores}  |  📦 **Products Tracked:** "
        f"{n_products} across {n_categories} categories"
    )
    st.caption(
        "An intern capstone project analyzing product performance and revenue "
        "concentration to support menu optimization decisions."
    )

    st.divider()

    # KPI Calculations
    total_revenue = df["Revenue"].sum()
    total_units = df["transaction_qty"].sum()
    total_products = df["product_id"].nunique()
    total_categories = df["product_category"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")

    with col2:
        st.metric("📦 Total Units Sold", f"{total_units:,.0f}")

    with col3:
        st.metric("☕ Total Products", f"{total_products:,}")

    with col4:
        st.metric("🗂️ Total Categories", f"{total_categories:,}")

    st.divider()

    # ============================================================
    # PREPARE DATA FOR CHARTS
    # ============================================================

    category_revenue = (
        df.groupby("product_category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    top_revenue = (
        df.groupby("product_type")["Revenue"]
        .sum()
        .nlargest(top_n)
        .sort_values()
    )

    top_sales = (
        df.groupby("product_type")["transaction_qty"]
        .sum()
        .nlargest(top_n)
        .sort_values()
    )

    category_revenue_donut = (
        df.groupby("product_category")["Revenue"]
        .sum()
    )

    top_category = category_revenue.index[0]
    top_category_share = (category_revenue.iloc[0] / category_revenue.sum()) * 100
    second_category = category_revenue.index[1]
    second_category_share = (category_revenue.iloc[1] / category_revenue.sum()) * 100
    combined_top2_share = top_category_share + second_category_share

    top_product_by_revenue = top_revenue.index[-1]
    top_product_by_volume = top_sales.index[-1]

    # ============================================================
    # VISUAL 1 - REVENUE BY PRODUCT CATEGORY
    # ============================================================

    fig1 = px.bar(
        x=category_revenue.index,
        y=category_revenue.values,
        title="Revenue by Product Category",
        labels={"x": "Product Category", "y": "Revenue"},
        text=category_revenue.values
    )
    fig1.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside",
        marker_color=ACCENT
    )
    fig1.update_layout(showlegend=False)

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown(
        f"📌 **Key finding:** **{top_category}** leads by a wide margin, followed by "
        f"**{second_category}** — together the two categories bring in about "
        f"{combined_top2_share:.0f}% of everything the business earns."
    )

    st.divider()

    # ============================================================
    # VISUAL 2 - TOP N PRODUCTS BY REVENUE
    # ============================================================

    fig2 = px.bar(
        x=top_revenue.values,
        y=top_revenue.index,
        orientation="h",
        title=f"Top {top_n} Products by Revenue",
        labels={"x": "Revenue", "y": "Product"},
        text=top_revenue.values
    )
    fig2.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside",
        marker_color=ACCENT
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        f"📌 **Key finding:** **{top_product_by_revenue}** stands out as the single "
        f"biggest earner on the entire menu — ahead of every other item shown above."
    )

    st.divider()

    # ============================================================
    # VISUAL 3 - TOP N PRODUCTS BY SALES VOLUME
    # ============================================================

    fig3 = px.bar(
        x=top_sales.values,
        y=top_sales.index,
        orientation="h",
        title=f"Top {top_n} Products by Sales Volume",
        labels={"x": "Units Sold", "y": "Product"},
        text=top_sales.values
    )
    fig3.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        marker_color=ACCENT
    )

    st.plotly_chart(fig3, use_container_width=True)

    if top_product_by_volume == top_product_by_revenue:
        volume_line = (
            f"📌 **Key finding:** **{top_product_by_volume}** also leads in unit sales — "
            f"it's both the most popular and the most profitable single product."
        )
    else:
        volume_line = (
            f"📌 **Key finding:** The biggest earner isn't the best-seller by volume — "
            f"**{top_product_by_volume}** sells in higher quantities, showing that "
            f"popularity and revenue don't always move together."
        )
    st.markdown(volume_line)

    st.divider()

    # ============================================================
    # VISUAL 4 - REVENUE DISTRIBUTION BY PRODUCT CATEGORY
    # ============================================================

    fig4 = px.pie(
        values=category_revenue_donut.values,
        names=category_revenue_donut.index,
        hole=0.5,
        title="Revenue Distribution by Product Category",
        color_discrete_sequence=NEUTRAL_SEQUENCE
    )
    fig4.update_traces(textinfo="label+percent")

    st.plotly_chart(fig4, use_container_width=True)

    st.markdown(
        f"📌 **Key finding:** {top_category} and {second_category} dominate the "
        f"revenue mix, while the remaining categories make up a long tail of smaller "
        f"contributions."
    )

# ============================================================
# PAGE 2 - PRODUCT PERFORMANCE
# ============================================================
elif page == "Page 2 - Product Performance":
    st.title("📊 Product Performance & Menu Optimization")
    st.caption(
        "Moving from category-level trends to individual product performance — "
        "revenue per unit, contribution share, and where volume and revenue align or don't."
    )

    st.divider()

    # ============================================================
    # BASE PRODUCT SUMMARY (used across this page)
    # ============================================================

    product_summary = (
        df.groupby("product_type")
        .agg(
            Units_Sold=("transaction_qty", "sum"),
            Total_Revenue=("Revenue", "sum")
        )
        .reset_index()
    )

    product_summary["Revenue_Per_Unit"] = (
        product_summary["Total_Revenue"] / product_summary["Units_Sold"]
    )

    product_summary["Sales Rank"] = (
        product_summary["Units_Sold"]
        .rank(method="min", ascending=False)
        .astype(int)
    )

    product_summary["Revenue Rank"] = (
        product_summary["Total_Revenue"]
        .rank(method="min", ascending=False)
        .astype(int)
    )

    total_revenue_all = df["Revenue"].sum()
    product_summary["Revenue_Contribution_Pct"] = (
        product_summary["Total_Revenue"] * 100 / total_revenue_all
    )

    # ============================================================
    # VISUAL 1 - REVENUE PER UNIT BY PRODUCT (Top N)
    # ============================================================

    revenue_per_unit = (
        product_summary
        .sort_values("Revenue_Per_Unit", ascending=False)
        .head(top_n)
        .sort_values("Revenue_Per_Unit")
    )
    top_rpu_product = revenue_per_unit.iloc[-1]["product_type"]
    top_rpu_value = revenue_per_unit.iloc[-1]["Revenue_Per_Unit"]

    fig_rpu = px.bar(
        revenue_per_unit,
        x="Revenue_Per_Unit",
        y="product_type",
        orientation="h",
        title=f"Top {top_n} Products by Revenue Per Unit",
        labels={"Revenue_Per_Unit": "Revenue Per Unit ($)", "product_type": "Product"},
        text="Revenue_Per_Unit"
    )
    fig_rpu.update_traces(
        texttemplate="$%{text:.2f}",
        textposition="outside",
        marker_color=ACCENT
    )

    st.plotly_chart(fig_rpu, use_container_width=True)

    st.markdown(
        f"📌 **Key finding:** **{top_rpu_product}** earns around ${top_rpu_value:,.2f} "
        f"per unit sold — well above the rest of the menu, even without high volume."
    )

    st.divider()

    # ============================================================
    # VISUAL 2 - REVENUE CONTRIBUTION (%) BY PRODUCT (Top N)
    # ============================================================

    revenue_contribution = (
        product_summary
        .sort_values("Total_Revenue", ascending=False)
        .head(top_n)
        .sort_values("Total_Revenue")
    )
    top_contrib_pct = revenue_contribution.iloc[-1]["Revenue_Contribution_Pct"]
    top_contrib_product = revenue_contribution.iloc[-1]["product_type"]

    fig_contrib = px.bar(
        revenue_contribution,
        x="Revenue_Contribution_Pct",
        y="product_type",
        orientation="h",
        title=f"Revenue Contribution (%) - Top {top_n} Products",
        labels={"Revenue_Contribution_Pct": "Revenue Contribution (%)", "product_type": "Product"},
        text="Revenue_Contribution_Pct"
    )
    fig_contrib.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        marker_color=ACCENT
    )

    st.plotly_chart(fig_contrib, use_container_width=True)

    st.markdown(
        f"📌 **Key finding:** **{top_contrib_product}** alone accounts for about "
        f"{top_contrib_pct:.1f}% of total revenue — a single product carrying a "
        f"meaningful share of the entire business."
    )

    st.divider()

    # ============================================================
    # VISUAL 3 - SALES VOLUME VS REVENUE (SCATTER)
    # ============================================================

    median_units = product_summary["Units_Sold"].median()
    median_revenue = product_summary["Total_Revenue"].median()

    # Only label the standout products (top ~30% by units or revenue) so
    # labels don't overlap in the crowded lower-left cluster.
    units_thresh = product_summary["Units_Sold"].quantile(0.7)
    revenue_thresh = product_summary["Total_Revenue"].quantile(0.7)
    product_summary["label"] = product_summary.apply(
        lambda r: r["product_type"]
        if (r["Units_Sold"] >= units_thresh or r["Total_Revenue"] >= revenue_thresh)
        else "",
        axis=1
    )

    fig_scatter = px.scatter(
        product_summary,
        x="Units_Sold",
        y="Total_Revenue",
        text="label",
        hover_name="product_type",
        title="Sales Volume vs Revenue",
        labels={"Units_Sold": "Units Sold", "Total_Revenue": "Revenue ($)"}
    )
    fig_scatter.update_traces(
        textposition="top center",
        textfont=dict(size=11),
        marker=dict(size=9, color=ACCENT)
    )
    fig_scatter.add_vline(x=median_units, line_dash="dot", line_color="#9C9C9C")
    fig_scatter.add_hline(y=median_revenue, line_dash="dot", line_color="#9C9C9C")
    fig_scatter.update_layout(
        height=650,
        margin=dict(t=60, b=40, l=40, r=40)
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown(
        "📌 **Key finding:** Products in the upper-right sell high volumes at high "
        "revenue — the strongest all-round performers. Products in the lower-left sell "
        "little and earn little, and are the ones most worth reviewing. Only standout "
        "products are labeled here to keep the chart readable; hover over any dot for "
        "its exact numbers."
    )

    st.divider()

    # ============================================================
    # TABLE 1 - PRODUCT RANKING (Sales Rank vs Revenue Rank)
    # ============================================================

    ranking_table = (
        product_summary
        .sort_values("Sales Rank")
        .head(top_n)
    )

    st.markdown(f"#### 🏅 Product Ranking - Top {top_n} by Sales Volume")

    st.dataframe(
        ranking_table[
            ["product_type", "Units_Sold", "Total_Revenue", "Sales Rank", "Revenue Rank"]
        ].rename(columns={
            "product_type": "Product",
            "Units_Sold": "Units Sold",
            "Total_Revenue": "Revenue"
        }).style.format({"Revenue": "${:,.2f}", "Units Sold": "{:,}"}),
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        "📌 **Key finding:** Comparing the two rank columns shows whether a product's "
        "popularity (Sales Rank) matches its earning power (Revenue Rank) — a big gap "
        "between the two usually means a pricing or positioning opportunity."
    )

    st.divider()

    # ============================================================
    # TABLE 2 - HERO PRODUCTS (Top N in BOTH sales & revenue)
    # ============================================================

    hero_products = (
        product_summary[
            (product_summary["Sales Rank"] <= top_n) &
            (product_summary["Revenue Rank"] <= top_n)
        ]
        .sort_values("Revenue Rank")
    )

    st.markdown("#### 🏆 Hero Products")

    st.dataframe(
        hero_products[
            ["product_type", "Units_Sold", "Total_Revenue", "Revenue_Per_Unit"]
        ].rename(columns={
            "product_type": "Product",
            "Units_Sold": "Units Sold",
            "Total_Revenue": "Total Revenue",
            "Revenue_Per_Unit": "Revenue Per Unit"
        }).style.format({
            "Total Revenue": "${:,.2f}",
            "Revenue Per Unit": "${:,.2f}",
            "Units Sold": "{:,}"
        }).set_properties(**{"background-color": HERO_BG, "color": "#1F3B2C"}),
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        f"📌 **Key finding:** These **{len(hero_products)} products** rank in the Top "
        f"{top_n} for both sales volume and revenue. They form the backbone of the "
        f"menu and deserve the most attention when it comes to availability and quality."
    )

    st.divider()

    # ============================================================
    # TABLE 3 - UNDERPERFORMING PRODUCTS (Bottom N by units sold)
    # ============================================================

    underperforming = (
        product_summary
        .sort_values("Units_Sold", ascending=True)
        .head(top_n)
    )

    st.markdown("#### ⚠️ Underperforming Products")

    st.dataframe(
        underperforming[
            ["product_type", "Units_Sold", "Total_Revenue", "Revenue_Per_Unit"]
        ].rename(columns={
            "product_type": "Product",
            "Units_Sold": "Units Sold",
            "Total_Revenue": "Total Revenue",
            "Revenue_Per_Unit": "Revenue Per Unit"
        }).style.format({
            "Total Revenue": "${:,.2f}",
            "Revenue Per Unit": "${:,.2f}",
            "Units Sold": "{:,}"
        }).set_properties(**{"background-color": UNDER_BG, "color": "#5C1F1C"}),
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        f"📌 **Key finding:** These are the {top_n} lowest-selling products in the "
        f"current filter — worth watching if the goal is to trim the menu or run "
        f"targeted promotions."
    )

# ============================================================
# PAGE 3 - REVENUE CONCENTRATION
# ============================================================
elif page == "Page 3 - Revenue Concentration":
    st.title("📊 Revenue Contribution & Menu Optimization")
    st.caption(
        "Stepping back from individual products to ask: how dependent is the "
        "business on a small handful of items, and where does that concentration come from?"
    )

    st.divider()

    # ============================================================
    # BASE DATA
    # ============================================================

    category_summary = (
        df.groupby("product_category")["Revenue"]
        .sum()
        .reset_index()
        .rename(columns={"Revenue": "Total_Revenue"})
    )
    category_summary["vs_Average"] = (
        category_summary["Total_Revenue"] - category_summary["Total_Revenue"].mean()
    )
    category_summary["Direction"] = category_summary["vs_Average"].apply(
        lambda v: "Above Average" if v >= 0 else "Below Average"
    )
    category_summary = category_summary.sort_values("vs_Average", ascending=True)

    product_revenue = (
        df.groupby("product_type")["Revenue"]
        .sum()
        .reset_index()
        .rename(columns={"Revenue": "Total_Revenue"})
        .sort_values("Total_Revenue", ascending=False)
        .reset_index(drop=True)
    )

    overall_revenue = product_revenue["Total_Revenue"].sum()
    product_revenue["Cumulative_Revenue"] = product_revenue["Total_Revenue"].cumsum()
    product_revenue["Cumulative_Pct"] = (
        product_revenue["Cumulative_Revenue"] / overall_revenue
    )

    topN_revenue = product_revenue.head(top_n)["Total_Revenue"].sum()
    revenue_concentration_ratio = round((topN_revenue / overall_revenue) * 100, 2)

    products_to_80pct = int((product_revenue["Cumulative_Pct"] < 0.8).sum() + 1)
    total_products_count = len(product_revenue)

    above_avg_categories = category_summary[category_summary["Direction"] == "Above Average"]
    above_avg_names = ", ".join(above_avg_categories["product_category"].tolist())
    above_avg_count = len(above_avg_categories)
    total_categories_count = len(category_summary)

    # ============================================================
    # KPI - TOP N REVENUE CONCENTRATION RATIO
    # ============================================================

    st.metric(f"🎯 Top {top_n} Revenue Concentration Ratio", f"{revenue_concentration_ratio}%")
    st.markdown(
        f"📌 **Key finding:** Just {top_n} out of {total_products_count} products "
        f"generate nearly {revenue_concentration_ratio}% of total revenue. The "
        f"business leans heavily on a small set of anchor items rather than an "
        f"even spread across the menu."
    )

    st.divider()

    # ============================================================
    # VISUAL 1 - CATEGORY REVENUE VS AVERAGE
    # ============================================================

    fig_cat_avg = px.bar(
        category_summary,
        x="vs_Average",
        y="product_category",
        orientation="h",
        color="Direction",
        color_discrete_map={"Above Average": ACCENT, "Below Average": "#B8B8B8"},
        title="Category Revenue vs Average",
        labels={"vs_Average": "Category Revenue vs Average", "product_category": "Product Category"},
        text="vs_Average"
    )
    fig_cat_avg.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig_cat_avg.update_layout(legend_title_text="")

    st.plotly_chart(fig_cat_avg, use_container_width=True)

    st.markdown(
        f"📌 **Key finding:** Only **{above_avg_count} of {total_categories_count} "
        f"categories** — {above_avg_names} — earn above the average category revenue. "
        f"Every other category sits below it, reinforcing how narrow the revenue base "
        f"really is."
    )

    st.divider()

    # ============================================================
    # VISUAL 2 - TOP N ANCHOR PRODUCTS
    # ============================================================

    topN_anchor = product_revenue.head(top_n).sort_values("Total_Revenue")

    fig_anchor = px.bar(
        topN_anchor,
        x="Total_Revenue",
        y="product_type",
        orientation="h",
        title=f"Top {top_n} Anchor Products",
        labels={"Total_Revenue": "Revenue ($)", "product_type": "Product"},
        text="Total_Revenue"
    )
    fig_anchor.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside",
        marker_color=ACCENT
    )

    st.plotly_chart(fig_anchor, use_container_width=True)

    st.markdown(
        "📌 **Key finding:** These are the anchor products responsible for that "
        "concentration — the ones carrying the business. Protecting their "
        "availability, pricing, and quality matters more than any other menu decision."
    )

    st.divider()

    # ============================================================
    # VISUAL 3 - TOP 30 PRODUCTS: CUMULATIVE REVENUE CONTRIBUTION
    # ============================================================

    top30_pareto = product_revenue.head(30)

    fig_pareto = px.bar(
        top30_pareto,
        x="product_type",
        y="Cumulative_Pct",
        title="Top 30 Products - Cumulative Revenue Contribution",
        labels={"product_type": "Product", "Cumulative_Pct": "Cumulative Revenue %"},
        text="Cumulative_Pct"
    )
    fig_pareto.update_traces(
        texttemplate="%{text:.0%}",
        textposition="outside",
        marker_color=ACCENT
    )
    fig_pareto.add_hline(
        y=0.8,
        line_dash="dot",
        line_color="#9C9C9C",
        annotation_text="80% threshold"
    )
    fig_pareto.update_yaxes(tickformat=".0%")

    st.plotly_chart(fig_pareto, use_container_width=True)

    st.markdown(
        f"📌 **Key finding:** It takes just **{products_to_80pct} products** to reach "
        f"80% of total revenue — a classic Pareto (80/20) effect, though slightly "
        f"flatter than the textbook rule since the full menu spans "
        f"{total_products_count} products. This chart always shows the top 30 products "
        f"to illustrate the full concentration curve, independent of the Top-N filter."
    )

    st.divider()

    # ============================================================
    # VISUAL 4 - BOTTOM N PRODUCTS BY REVENUE (LONG-TAIL)
    # ============================================================

    bottomN_revenue = product_revenue.tail(top_n).sort_values("Total_Revenue")

    fig_bottom = px.bar(
        bottomN_revenue,
        x="Total_Revenue",
        y="product_type",
        orientation="h",
        title=f"Bottom {top_n} Products by Revenue (Long-Tail)",
        labels={"Total_Revenue": "Revenue ($)", "product_type": "Product"},
        text="Total_Revenue"
    )
    fig_bottom.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside",
        marker_color=ALERT
    )

    st.plotly_chart(fig_bottom, use_container_width=True)

    st.markdown(
        "📌 **Key finding:** These products barely move the needle on revenue and "
        "are the strongest candidates for bundling, repricing, or removal from the menu."
    )