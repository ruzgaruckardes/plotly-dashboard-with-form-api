
import JotformClient
import DataProcessing

import pandas as pd
import geopandas as gpd
import plotly.express as px
import dash_mantine_components as dmc
from dash import Dash, html, dash_table, dcc, Output, Input
from dotenv import load_dotenv
import os

load_dotenv()

# you can put here your private API_Key
api_key = os.getenv("API_KEY")
form_id = "240577213808963"

clint_inst = JotformClient.JotFormClient(api_key)
data_processing_inst = DataProcessing.DataProcessing(clint_inst, form_id)
submissions_df, crop_counts, irrigation_time = data_processing_inst.get_all_df()

canakkale_districts_geojson = gpd.read_file('canakkale_districts.geojson')

districts = {'District': ['Biga', 'Yenice', 'Can', 'Bayramic'],
             'id': [5, 8, 7, 9]}
districts_df = pd.DataFrame(districts)

external_stylesheets = [dmc.theme.DEFAULT_COLORS]

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dmc.Container([
    html.Br(),
    html.H1('IRRIGATION BEHAVIOURS', style={"color": "#008080", "textAlign": "center"}),
    html.Br(),

    dcc.Tabs([
        dcc.Tab(label='General Situation', children=[
            html.Br(),

            dmc.Group(
                dmc.Grid([
                    dmc.Col([
                        html.H3("Dashboard Results Disclaimer", style={"color": "#025043"}),
                        html.P([
                            dcc.Markdown('''The dashboard displays results generated from synthetic data and does not reflect actual metrics on related area. The project's objective encompasses automating data acquisition through the JotForm API, conducting automated data analysis 
and making an interactive dashboard. **Interactive dashboards** serve as indispensable tools for gaining a holistic overview 
and monitoring key performance indicators (KPIs) relevant to the project's progress.

[Please find the **questionnaire** by clicking here](https://form.jotform.com/240577213808963)
''')],
                            style={"display": "flex", "justify-content": "center", "align-items": "center", })],
                        span=9),
                    dmc.Col([
                        dmc.Card([
                            html.H3('Total Submission', style={"color": "#025043"}),
                            html.H3('Number', style={"color": "#025043"}),
                            html.H3(f'{int(len(submissions_df))}',
                                    style={'font-weight': 'normal'})
                        ],
                            withBorder=True,
                            style={"textAlign": "center", "justify-content": "center", "align-items": "center"}),
                    ], style={"textAlign": "right", "height": "100%"}, span=3),
                ])
            ),

            html.Br(),
            dmc.Grid([
                dmc.Col([
                    dcc.Graph(
                        figure=px.pie(submissions_df,
                                      names='Gender',
                                      title='Gender',
                                      color_discrete_sequence=px.colors.sequential.Teal).update_traces(
                            textposition='inside',
                            textinfo='percent+label').update_layout(showlegend=False,
                                                                    title=dict(text='Gender',
                                                                               x=0.5)),
                        id='general-gender')
                ], span=4),
                dmc.Col([
                    dcc.Graph(
                        figure=px.pie(submissions_df,
                                      names='District',
                                      title='District',
                                      color_discrete_sequence=px.colors.sequential.Teal).update_traces(
                            textposition='inside',
                            textinfo='percent+label').update_layout(showlegend=False,
                                                                    title=dict(text='District',
                                                                               x=0.5)),
                        id='general-district')
                ], span=4),
                dmc.Col([
                    dcc.Graph(
                        figure=px.pie(submissions_df,
                                      names='EducationLevel',
                                      title='EducationLevel',
                                      color_discrete_sequence=px.colors.sequential.Teal).update_traces(
                            textposition='inside',
                            textinfo='percent+label').update_layout(showlegend=False,
                                                                    title=dict(text='Gender',
                                                                               x=0.5)),
                        id='general-education')
                ], span=4)]),

            html.Br(),
            dmc.Grid([
                dmc.Col([
                    dcc.Graph(
                        figure=px.bar(submissions_df.groupby(['District', 'ProductionPurpose']).size().reset_index(name='Count'),
                                      x='District',
                                      y='Count',
                                      color='ProductionPurpose',
                                      text='ProductionPurpose',
                                      color_discrete_sequence=px.colors.sequential.Teal_r)
                        .update_traces(
                            textposition='inside',
                            textangle=0,
                            texttemplate='%{text}').update_layout(showlegend=False),
                        id='general-district-prod',
                        config={'displayModeBar': False},
                        style={'height': '100%'}
                    )
                ], span=6),
                dmc.Col([
                    dcc.Graph(figure=px.bar(crop_counts, x='CropCultivated', y='Count', facet_row='District',
                                            text='CropCultivated',
                                            color_discrete_sequence=px.colors.sequential.Teal_r).update_yaxes(
                        title_text='').update_layout(
                        annotations=[dict(text=ann.text.split('=')[1].strip())
                                     for ann in px.bar(
                                crop_counts, x='CropCultivated', y='Count', facet_row='District',
                                text='CropCultivated',
                                color_discrete_sequence=px.colors.sequential.Teal_r).layout.annotations]),
                        id='general-crop-district',
                        config={'displayModeBar': False},
                        style={'height': '100%'}
                    )
                ], span=6)
            ]),
            html.Br(),
            dmc.Grid([
                dmc.Col([
                    dcc.Graph(figure=px.bar(
                        submissions_df.groupby(['IrrigationFrequency']).size().reset_index(name='Count').sort_values(by='Count',
                                                                                                           ascending=False),
                        x='IrrigationFrequency',
                        y='Count',
                        text='Count',
                        color_discrete_sequence=px.colors.sequential.Teal_r).update_traces(
                        textposition='inside').update_layout(
                        showlegend=False,
                        title=dict(x=0.5),
                        xaxis=dict(tickmode='array',
                                   tickangle=0,
                                   tickvals=submissions_df['IrrigationFrequency'].tolist(),
                                   ticktext=[label[:9] + '<br>' + label[9:22] + '<br>' + label[22:] if len(label) > 28
                                             else (label[:9] + '<br>' + label[9:18] + '<br>' + label[18:]) if len(
                                       label) > 22
                                   else (label[:9] + '<br>' + label[9:12] + '<br>' + label[12:]) if len(label) > 20
                                   else label for label in submissions_df['IrrigationFrequency'].tolist()]))),

                ], span=6),
                dmc.Col([
                    dcc.Graph(figure=px.bar(
                        irrigation_time.groupby(['IrrigationTime']).size().reset_index(name='Count').sort_values(
                            by='Count',
                            ascending=False),
                        x='IrrigationTime',
                        y='Count',
                        text='Count',
                        color_discrete_sequence=px.colors.sequential.Teal_r).update_traces(
                        textposition='inside').update_layout(
                        showlegend=False,
                        title=dict(x=0.5),
                        xaxis=dict(tickmode='array',
                                   tickangle=0,
                                   tickvals=irrigation_time['IrrigationTime'].tolist(),
                                   ticktext=[label[:9] + '<br>' + label[9:16] + '<br>' + label[16:] if len(label) > 26
                                             else (label[:9] + '<br>' + label[9:12] + '<br>' + label[12:]) if len(
                                       label) > 20
                                   else (label[:5] + '<br>' + label[5:]) if len(label) > 11
                                   else label for label in irrigation_time['IrrigationTime'].tolist()]))),

                ], span=6)
            ])
        ]),

        dcc.Tab(label='District-Based Analysis', children=[
            html.Br(),
            html.H3('Please select a district to see the specific results.',
                    style={"color": "#008080", "textAlign": "left"}),
            dcc.Dropdown(
                id="Distinct_Dropdown",
                options=sorted(submissions_df["District"].unique())),
            html.Br(),
            dmc.Grid([
                dmc.Col([dmc.Col([
                    dmc.Card([html.H3(id='total_submission_text', style={'color': '#025043'})], withBorder=True)],
                    span=12),

                ])
            ]),
            dmc.Grid([
                dmc.Col([dcc.Graph(id='plot-district',
                                  style={'height': '100%', 'width': '100%', 'object-fit': 'contain'})], span=6),
                dmc.Col([dcc.Graph(id='top-crops-district',
                                   style={'height': '100%', 'width': '100%'})], span=6)


            ]),
            html.Br(),
            dmc.Grid([
                dmc.Col([dcc.Graph(id='difficulty-district')], span=6),
                dmc.Col([dcc.Graph(id='scarcity-district')], span=6)
            ]),

        ]),
        dcc.Tab(label='Submissions',
                children=[
                    html.Br(),
                    dmc.Grid([
                        dmc.Col([
                            dash_table.DataTable(
                                data=submissions_df.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in
                                         (submissions_df.drop(["id", "created_at"], axis=1)).columns],
                                filter_action='native',
                                sort_action="native",
                                page_size=5,
                                style_data={'whiteSpace': 'normal',
                                            'overflow': 'hidden',
                                            'textOverflow': 'ellipsis',
                                            'maxWidth': 0},
                                style_header={'whiteSpace': 'normal',
                                              'height': 'auto',
                                              'fontWeight': 'bold',
                                              'color': '#008080'},
                                style_table={'overflowX': 'auto'})], span=12)
                    ])
                ]),
    ]),
], style={'backgroundColor': '#edf5f4',
          'font-family': '-apple-system'}, fluid=True)  # Background color light orange


@app.callback(Output('plot-district', 'figure'),
              Output('top-crops-district', 'figure'),

              Output('difficulty-district', 'figure'),
              Output('scarcity-district', 'figure'),
              Output('total_submission_text', 'children'),
              Input('Distinct_Dropdown', 'value'))
def chart_by_district(district):
    if district is None:
        district = 'Bayramic'

    query_string = f"District == '{district}'"

    dataset1 = submissions_df.query(query_string)
    dataset2 = crop_counts.query(query_string)
    dataset3 = districts_df.query(query_string)
    top_three_crops = dataset2.sort_values(by='Count', ascending=False).head(3)

    plot_district_on_map = px.choropleth_mapbox(dataset3, geojson=canakkale_districts_geojson, color="District",
                                                locations="id",
                                                center={"lat": 39.960701, "lon": 27.217379},
                                                mapbox_style="carto-positron", zoom=7,
                                                color_discrete_sequence=px.colors.sequential.Teal_r).update_traces(showlegend=False)

    access_to_water = px.pie(dataset1,
                           names='DifficultyAccessingWater',
                           title=f'Difficulty in Water Access in {district}',
                           color_discrete_sequence=px.colors.sequential.Teal_r).update_traces(textposition='inside',
                                                                                              textinfo='percent+label').update_layout(
        showlegend=False,
        title=dict(x=0.5))

    future_water_scarcity = px.pie(dataset1,
                                 names='ConcernFutureWaterScarcity',
                                 title=f'Concern About Future Water Scarcity in {district}',
                                 color_discrete_sequence=px.colors.sequential.Teal_r).update_traces(
        textposition='inside',
        textinfo='percent+label').update_layout(
        showlegend=False,
        title=dict(x=0.5))

    top_crops = px.bar(top_three_crops,
                      x='CropCultivated',
                      y='Count',
                      color_discrete_sequence=px.colors.sequential.Teal_r,
                      text='Count',
                      title=f'Top Three Cultivated Crops in {district}').update_layout(title_x=0.5)

    receive_training = px.pie(dataset1,
                             names='WillingToReceiveIrrigationPracticesTraining',
                             title=f'Willing To Receive Training on Irrigation',
                             color_discrete_sequence=px.colors.sequential.Teal_r).update_traces(textposition='inside',
                                                                                                textinfo='percent+label').update_layout(
        showlegend=False,
        title=dict(x=0.5))

    total_submission_count = len(dataset1)

    total_submission_count_text = f"Total submission: {total_submission_count}"

    return plot_district_on_map, top_crops, access_to_water, future_water_scarcity, total_submission_count_text if district else None


if __name__ == '__main__':
    app.run(port=8060, debug=True)