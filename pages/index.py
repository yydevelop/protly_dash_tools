import dash_html_components as html
import dash_core_components as dcc

layout = html.Div([
    dcc.Link('Go to minutes', href='/minutes'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])