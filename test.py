import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.set_page_config(page_title="Global Internet Freedom Dashboard", layout="wide", page_icon="🌍")

st.markdown("""
<style>
body {
    background-color:#0f172a;
    color:white;
}
.block-container{
    padding-top:2rem;
}
section[data-testid="stSidebar"]{
    background-color:#020617;
}
h1,h2,h3{
    color:#f8fafc;
}
.metric-card{
    background:rgba(255,255,255,0.05);
    border-radius:12px;
    padding:20px;
    backdrop-filter:blur(10px);
    border:1px solid rgba(255,255,255,0.1);
}
.dataframe{
    background:rgba(255,255,255,0.05);
}
</style>
""", unsafe_allow_html=True)

sns.set_style("whitegrid")
sns.set_palette("viridis")

new_data = pd.read_csv("cleaned_data/iso.csv")
new_data['year'] = pd.to_datetime(new_data['year']).dt.year

st.title("🌍 Global Internet Freedom Dashboard")
st.markdown("Interactive analysis of **internet access, governance indicators, and freedom scores worldwide.**")

st.sidebar.title("Navigation")
menu = ["Country Explorer","Global Trends","Country Comparison","Correlation Heatmap","Forecasts","World Map"]
choice = st.sidebar.radio("Select Analysis Section", menu)

if choice == "Country Explorer":
    countries = sorted(new_data['country'].unique())
    selected_country = st.selectbox("Select Country", countries)
    country_df = new_data[new_data['country'] == selected_country]

    col1, col2 = st.columns([2,1])
    with col1:
        fig = px.line(
            country_df,
            x="year",
            y="freedom_score",
            markers=True,
            color_discrete_sequence=["#22c55e"]
        )
        fig.update_layout(height=420, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        latest = country_df.iloc[-1]
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Freedom Score", int(latest["freedom_score"]))
        st.metric("Internet Access %", round(latest["wdi_internet"],1))
        st.metric("HDI", round(latest["undp_hdi"],3))
        st.markdown('</div>', unsafe_allow_html=True)

    indicators = ["wdi_internet","wdi_gdpcapcon2015","undp_hdi","vdem_libdem","ti_cpi"]
    fig, axs = plt.subplots(1,5,figsize=(20,4))
    for i, col in enumerate(indicators):
        sns.regplot(
            data=country_df,
            x=col,
            y="freedom_score",
            ax=axs[i],
            scatter_kws={"alpha":0.7},
            line_kws={"color":"#f97316"}
        )
        axs[i].set_title(col)
    st.pyplot(fig)

elif choice == "Global Trends":
    for col in ["wdi_gdpcapcon2015","undp_hdi","vdem_libdem","ti_cpi","wdi_internet","freedom_score"]:
        new_data[col] = pd.to_numeric(new_data[col], errors='coerce')
    yearly = new_data.groupby("year").mean(numeric_only=True).reset_index()

    fig = px.line(
        yearly,
        x="year",
        y=["freedom_score","wdi_internet"],
        markers=True,
        color_discrete_sequence=["#22c55e","#38bdf8"]
    )
    fig.update_layout(height=500, template="plotly_dark", legend_title="Indicator")
    st.plotly_chart(fig, use_container_width=True)

elif choice == "Country Comparison":
    first_last = new_data.groupby("country").agg(
        first_year=('year','min'),
        last_year=('year','max'),
        first_score=('freedom_score','first'),
        last_score=('freedom_score','last')
    ).reset_index()

    fig = px.bar(
        first_last,
        x="country",
        y="last_score",
        color="last_score",
        color_continuous_scale="viridis",
        title="Latest Freedom Score by Country"
    )
    fig.update_layout(template="plotly_dark", height=450)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(first_last, use_container_width=True)

elif choice == "Correlation Heatmap":
    numeric_cols = ["wdi_internet","wdi_gdpcapcon2015","undp_hdi","vdem_libdem","ti_cpi","freedom_score"]
    corr = new_data[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap="mako", linewidths=0.5, ax=ax)
    st.pyplot(fig)

elif choice == "Forecasts":
    forecast_years = 10
    countries = ['Australia','Germany','Thailand','India','China']
    fig, axes = plt.subplots(3,2,figsize=(14,10))
    axes = axes.flatten()
    for i, country in enumerate(countries):
        ax = axes[i]
        series = new_data[new_data["country"]==country].set_index("year")["freedom_score"].sort_index()
        series = series.dropna()
        if len(series) < 3:
            ax.set_title(country)
            continue
        model = ExponentialSmoothing(series, trend="add", seasonal=None, damped_trend=True)
        fit = model.fit()
        forecast = fit.forecast(forecast_years)
        ax.plot(series.index, series.values, label="Historical")
        ax.plot(range(series.index[-1]+1, series.index[-1]+1+forecast_years), forecast.values, "--", label="Forecast")
        ax.axvline(series.index[-1], linestyle=":", color="gray")
        ax.set_title(country)
        ax.legend()
    for j in range(len(countries), len(axes)):
        fig.delaxes(axes[j])
    plt.tight_layout()
    st.pyplot(fig)

elif choice == "World Map":
    latest_year = new_data["year"].max()
    map_df = new_data[new_data["year"]==latest_year]
    fig = px.choropleth(
        map_df,
        locations="ccodealp",
        locationmode="ISO-3",
        color="freedom_score",
        hover_name="country",
        color_continuous_scale="viridis",
        title=f"Freedom Score ({latest_year})"
    )
    fig.update_layout(template="plotly_dark", height=650)
    st.plotly_chart(fig, use_container_width=True)