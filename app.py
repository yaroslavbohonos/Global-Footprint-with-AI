import dash
from dash import html, dcc, Input, Output
import dash_ag_grid as dag
import pandas as pd

# --- Initialize app ---
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Global Footprint with AI"

# --- Sample data ---
data = [
    {
        "Name": "Company A",
        "Sector": "Energy",
        "World Impact Score": 72,
        "Environmental": 70,
        "Social": 65,
        "Governance": 80,
        "Transparency Index": 60,
        "Scope 1-3 Emissions": "High",
        "Sustainability Investment Ratio": "12%",
        "Data Confidence": "High",
    },
    {
        "Name": "Company B",
        "Sector": "Tech",
        "World Impact Score": 88,
        "Environmental": 85,
        "Social": 82,
        "Governance": 90,
        "Transparency Index": 75,
        "Scope 1-3 Emissions": "Medium",
        "Sustainability Investment Ratio": "28%",
        "Data Confidence": "Medium",
    },
]
df = pd.DataFrame(data)

# --- Build columnDefs using flex to auto-fit content ---
columnDefs = [
    {"headerName": "Name", "field": "Name", "flex": 1},
    {"headerName": "Sector", "field": "Sector", "flex": 1},
    {"headerName": "World\nImpact\nScore", "field": "World Impact Score", "flex": 1},
    {"headerName": "Environmental", "field": "Environmental", "flex": 1},
    {"headerName": "Social", "field": "Social", "flex": 1},
    {"headerName": "Governance", "field": "Governance", "flex": 1},
    {"headerName": "Transparency\nIndex", "field": "Transparency Index", "flex": 1},
    {"headerName": "Scope 1–3\nEmissions", "field": "Scope 1-3 Emissions", "flex": 1},
    {"headerName": "Sustainability\nInvestment\nRatio", "field": "Sustainability Investment Ratio", "flex": 1},
    {"headerName": "Data\nConfidence", "field": "Data Confidence", "flex": 1},
    {"headerName": "Report", "field": "Report", "cellRenderer": "AgGridButton", "cellRendererParams": {"label": "View"}, "flex": 1},
    {"headerName": "Remove", "field": "Remove", "cellRenderer": "AgGridButton", "cellRendererParams": {"label": "✖"}, "flex": 1},
]


# --- Layout ---
app.layout = html.Div([

    # Fixed navigation bar
    html.Nav([
        html.Div("🌍 Global Footprint with AI", className="nav-logo"),
        html.Ul([
            html.Li(html.A("Home", href="#home-section")),
            html.Li(html.A("How It Works", href="#how-section")),
            html.Li(html.A("Watchlist", href="#watchlist-section")),
            html.Li(html.A("Reports", href="#reports-section")),
            html.Li(html.A("Reliability", href="#reliability-section")),
        ], className="nav-links")
    ], className="navbar"),

    # Page content
    html.Div([
        # Home section
        html.Section([
            html.H1("Assessing Companies’ Global Footprint with AI", className="title"),
            html.P("Transparent, data-driven insights for investors, regulators, journalists, and consumers.", className="slogan")
        ], id="home-section", className="section"),

        # How It Works
        html.Section([
            html.H2("How It Works"),
            html.Ol([
                html.Li("🔍 Search or select a company from the global database."),
                html.Li("🧠 AI extracts sustainability data from reports and filings."),
                html.Li("📊 Model calculates impact and transparency scores."),
                html.Li("💬 View insights, trends, and AI-generated reports.")
            ])
        ], id="how-section", className="section"),

        # Watchlist section
        html.Section([
            html.H2("Company Watchlist"),
            dcc.Input(id="search-bar", type="text", placeholder="Search company...", className="search-bar"),
            html.Button("Search", id="search-btn", className="search-btn"),
            html.Br(), html.Br(),
            dag.AgGrid(
                id="watch-table",
                columnDefs=columnDefs,
                rowData=df.to_dict("records"),
                defaultColDef={
                    "sortable": True,
                    "filter": True,
                    "resizable": True,
                    "wrapHeaderText": True,
                    "autoHeaderHeight": True,
                },
                dashGridOptions={
                    "domLayout": "autoHeight",
                    "animateRows": True
                },
                style={"width": "100%", "marginBottom": "20px"}
            )
        ], id="watchlist-section", className="section"),

        # Reports section
        html.Section([
            html.H2("Company Report"),
            html.Div("Select a company from the Watchlist to generate a detailed AI sustainability report.", className="report-window")
        ], id="reports-section", className="section"),

        # About section
        html.Section([
            html.H2("How and Why This Score Can Be Used"),
            html.P("""
                The Global Impact Score summarizes environmental, social, and governance performance
                into one transparent indicator. It helps:
                • Investors assess ESG resilience
                • Journalists verify green claims
                • Regulators monitor compliance
                • Consumers make informed decisions
            """),
            html.P("""
                ⚠️ Drawbacks: The score depends on data availability and standardization.
                AI can speed up and improve consistency but must be supported by verified disclosures.
            """, className="drawbacks")
        ], id="reliability-section", className="section")
    ])
])

# Smooth scroll
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <script>
        document.addEventListener("DOMContentLoaded", function() {
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    e.preventDefault();
                    document.querySelector(this.getAttribute('href')).scrollIntoView({
                        behavior: 'smooth'
                    });
                });
            });
        });
        </script>
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>
'''

if __name__ == "__main__":
    app.run_server(debug=True)
