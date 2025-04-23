import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import socket

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Define the layout for the main page
main_page_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div([
            html.H2("OPEN PORT SCANNER", style={"margin-bottom": "0"})
        ], style={"text-align": "center"})),
        dbc.Col(dbc.Button(html.Img(src="images/menu.png"), href="/info", color="primary", n_clicks=0, 
                           style={"border-radius": "50%", "width": "40px", "height": "40px"}), width="auto"),
    ], align="center", justify="between", className="my-4", style={"background-color": "#f8f9fa", "padding": "10px", "border-radius": "8px", "border": "2px solid #000"}),  
    html.H2("Port Scanner", className="text-center my-4"),
    dbc.Row([
        dbc.Col([
            dbc.Button("Scan", id="scan-button", color="success", n_clicks=0),
        ], width="auto"),
    ], className="text-center mb-4", justify="center"),
    dbc.Row([
        dbc.Col([
            dcc.Loading(
                id="loading-animation",
                type="dot",
                children=[html.Div(id="output-content")]
            )
        ], className="text-center")
    ]),
    # Additional content sections
    dbc.Row([
        dbc.Col([
            html.H3("What is an Open Port Scanner?", style={"font-size": "24px"}),
            html.P("An open port scanner is a tool used to test a server or host for open ports. It helps identify which ports are open, which services are running, and potential vulnerabilities.", style={"font-size": "20px"}),
        ], className="my-4"),
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("How to Use It?", style={"font-size": "24px"}),
            html.Ul([
                html.Li("Step 1: Click on the 'Scan' button.", style={"font-size": "20px"}),
                html.Li("Step 2: The scanner will check for open ports on the local system.", style={"font-size": "20px"}),
                html.Li("Step 3: View the results displayed on the dashboard.", style={"font-size": "20px"}),
                html.Li("Step 4: If no open ports are found, a message will be displayed.", style={"font-size": "20px"}),
            ]),
        ], className="my-4"),
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("What are the Benefits?", style={"font-size": "24px"}),
            html.Ul([
                html.Li("Security: Identifies open ports and potential vulnerabilities.", style={"font-size": "20px"}),
                html.Li("Network Management: Helps manage and monitor network services.", style={"font-size": "20px"}),
                html.Li("Troubleshooting: Assists in diagnosing network issues.", style={"font-size": "20px"}),
                html.Li("Compliance: Ensures that only necessary ports are open and accessible.", style={"font-size": "20px"}),
            ]),
        ], className="my-4"),
    ]),
])

# Info Page Layout
info_page_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(src="images/acelogo.png", height="80px"), width="auto"),
        dbc.Col(html.Div([
            html.H2("ADHIYAMAAN COLLEGE OF ENGINEERING", style={"margin-bottom": "0"}),
            html.H5("(AUTONOMOUS)", style={"margin-top": "0", "margin-bottom": "5px"}),  
            html.H5("DEPARTMENT OF CSE(CYBER SECURITY)", style={"margin-top": "5px"})
        ], style={"text-align": "center"})),
        dbc.Col(html.Img(src="images/cyberlogo.png", height="80px"), width="auto")
    ], align="center", justify="center", className="my-4", style={"background-color": "#f8f9fa", "padding": "10px", "border-radius": "8px", "border": "2px solid #000"}),  
    dbc.Row([
        dbc.Col(dbc.Button("Back", href="/", color="secondary", n_clicks=0), width="auto")
    ], align="center", justify="center", className="my-4"),
])

# Port Scanning Callback
@app.callback(
    Output("output-content", "children"),
    [Input("scan-button", "n_clicks")]
)
def scan_ports(n_clicks):
    if n_clicks:
        total_ports = 70  # Total ports scanned
        open_ports = []
        common_ports = {
            20: "FTP Data Transfer",
            21: "FTP Control",
            22: "SSH - Secure Shell",
            23: "Telnet - Remote Login Service",
            25: "SMTP - Email Routing",
            53: "DNS - Domain Name System",
            80: "HTTP - Web Traffic",
            110: "POP3 - Email Retrieval",
            143: "IMAP - Internet Message Access Protocol",
            443: "HTTPS - Secure Web Traffic",
            3306: "MySQL Database",
            3389: "RDP - Remote Desktop Protocol"
        }

        for port in range(1, total_ports + 1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex(('localhost', port))
            if result == 0:
                open_ports.append(port)
            s.close()

        if open_ports:
            open_ports_info = html.Div([
                html.H4("⚠ Open Ports Detected!"),
                html.P(f"Total Scanned Ports: {total_ports}"),
                html.P(f"Open Ports: {', '.join(map(str, open_ports))}"),
            ])
        else:
            open_ports_info = html.Div([
                html.H4("✅ Hurray! Your system has no open ports."),
                html.P(f"Total Scanned Ports: {total_ports}")
            ])

        major_ports_section = html.Div([
            html.H3("🔹 Major Ports & Their Tasks"),
            html.Ul([html.Li(f"Port {port}: {desc}") for port, desc in common_ports.items()])
        ])

        security_tips = html.Div([
            html.H3("🛡 How to Prevent Open Ports from Attacks"),
            html.Ul([
                html.Li("Close unnecessary ports using a firewall."),
                html.Li("Use strong passwords and authentication methods."),
                html.Li("Enable intrusion detection systems (IDS)."),
                html.Li("Regularly scan for vulnerabilities."),
                html.Li("Use VPNs to encrypt traffic.")
            ])
        ])

        open_port_uses = html.Div([
            html.H3("🔧 Open Ports Can Be Used For"),
            html.Ul([
                html.Li("Hosting web applications (Port 80, 443)."),
                html.Li("Secure remote access (Port 22 for SSH)."),
                html.Li("Database connections (Port 3306 for MySQL)."),
                html.Li("Email services (Port 25 for SMTP)."),
                html.Li("wifi services (Port 44 for lan).")
            ])
        ])

        return html.Div([
            open_ports_info,
            major_ports_section,
            security_tips,
            open_port_uses
        ])

    return html.Div()

@app.callback(Output("page-content", "children"), 
              [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/info":
        return info_page_layout
    else:
        return main_page_layout

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

if __name__ == "_main_":
    app.run_server(debug=True)