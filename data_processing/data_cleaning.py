import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import base64
import io
import plotly.express as px  # Puedes cambiar esto por la biblioteca de gráficos que prefieras

# Crear una aplicación Dash
app = dash.Dash(__name__)

# Diseño de la interfaz de usuario
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arrastra y suelta o ',
            html.A('selecciona archivos')
        ]),
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(id='graph-output')  # Agregamos un espacio para visualizar gráficos
])

# Función para cargar y procesar los datos
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    return df.to_json(orient='split'), filename

# Callback para cargar y mostrar los datos
@app.callback([Output('output-data-upload', 'children'),
               Output('graph-output', 'figure')],
              [Input('upload-data', 'contents')],
              [dash.dependencies.State('upload-data', 'filename')])
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)
        ]

        # Extraer el DataFrame del resultado de la función parse_contents
        df = pd.read_json(children[0][0], orient='split')

        # Generar un gráfico simple con Plotly Express (puedes personalizar según tus necesidades)
        fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title='Gráfico de Ejemplo')

        return children, fig

# Iniciar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
