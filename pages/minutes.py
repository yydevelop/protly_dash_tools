from sre_parse import State
from dash import dcc, html, Input, Output, callback
import dash_core_components as dcc
import dash_html_components as html
import os
import base64

layout = html.Div([

html.Div(
	dcc.Upload(
		id='upload-data',
		children=html.Div([
			'Drag and Drop or ',
			html.A('Select Files')
		]),
		style={
			'width': '100%',
			'height': '60px',
			'lineHeight': '60px',
			'borderWidth': '1px',
			'borderStyle': 'dashed',
			'borderRadius': '5px',
			'textAlign': 'center',
			'margin': '10px'
		},
		# Limit file types to .mp4
		accept='.mp4'
	),
	style={'width': '50%', 'margin': '0 auto'}
),
    html.Div(
        id='output-data-upload',
        style={'width': '50%', 'margin': '0 auto'}
    ),
    html.Div(
        dcc.Input(id='input-box', type='text', value='default text'),
        style={'width': '50%', 'margin': '0 auto'}
    ),
    html.Div(
        html.Button('Submit', id='button'),
        style={'width': '50%', 'margin': '0 auto'}
    ),
    html.Div(
        id='output-container-button',
        children='Enter something in the box and press submit.',
        style={'width': '50%', 'margin': '0 auto'}
    ),
])

@callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is None:
        return 'No file uploaded.'
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        #相対パスのカレントディレクトリ直下にファイルを保存
		filename = os.path.join(os.getcwd(), filename)
        with open(filename, 'wb') as f:
			f.write(decoded)
        return f'Uploaded file: {filename}'