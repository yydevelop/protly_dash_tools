import dash
import dash_html_components as html
from dash.dependencies import Input, Output

from pages import index, minutes, page2
import dash_core_components as dcc

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
			  [Input('url', 'pathname')])
def display_page(pathname):
	if pathname == '/minutes':
		return minutes.layout
	elif pathname == '/page-2':
		return page2.layout
	else:
		return index.layout

if __name__ == '__main__':
	app.run_server(debug=True)