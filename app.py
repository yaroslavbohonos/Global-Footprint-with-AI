import os
import dash
from dash import html, dcc
from dash_ag_grid import AgGrid as dag
import pandas as pd

from utils.data_loader import load_companies
from utils.scoring import compute_world_impact_score
from utils.api_clients import extract_company_esg

# ------------- LOAD DATA -------------
companies = load_companies()

# ------------- DEFINE COLUMNS FOR TABLE -------------
columnDefs = [
    {"headerName": "Name", "field": "Name", "sortable": True, "filter": True},
    {"headerName": "Sector", "field": "Sector", "sortable": True, "filter": True},
    {"headerName": "World Impact Score", "field": "WorldImpactScore", "sortable": True},
    {"headerName": "Environmental", "field": "Environmental"},
    {"headerName": "Social", "field": "Social"},
    {"headerName": "Governance", "field": "Governance"},
    {"headerName": "Transparency Index", "field": "TransparencyIndex"},
    {"headerName": "Scope 1-3 Emissions", "field": "ScopeEmissions"},
    {"headerName": "Sustainability Investment Ratio", "field": "SustainabilityInvestmentRatio"},
    {"headerName": "Data Confidence", "field": "DataConfidence"},
    # Extra columns left empty for now
    {"headerName": "Report", "field": "Report", "cellRenderer": "''"},
    {"headerName": "Remove", "field": "Remove", "cellRenderer": "''"}
]

# ------------- CREATE APP -------------
app = dash.Dash(__name__)
app.title = "Global Footprint Tracker"

# ------------- LAYOUT -------------
app.layout = html.Div([
    # Fixed top nav
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

            dag(
                id="watch-table",
                columnDefs=columnDefs,
                rowData=companies.to_dict("records"),  # now pre-populated automatically
                defaultColDef={
                    "sortable": True,
                    "filter": True,
                    "resizable": True,
                    "wrapHeaderText": True,
                    "autoHeaderHeight": True,
                },
                dashGridOptions={"domLayout": "autoHeight", "animateRows": True},
                style={"width": "100%", "marginBottom": "20px"}
            )
        ], id="watchlist-section", className="section"),

        # Reports section
        html.Section([
            html.H2("Company Report"),
            html.Div("Select a company from the Watchlist to generate a detailed AI sustainability report.", className="report-window")
        ], id="reports-section", className="section"),

        # Reliability
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

# Smooth scroll JS
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
    app.run(debug=True)
