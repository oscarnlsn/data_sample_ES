# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 16:10:27 2020

@author: ADMIN
"""
#import textwrap as d
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import dash_table

#Direccion de trabajo
#folder_input = 'C:/Users/agos9001/Documents/ES Sample size analisis/'
folder_input = 'G:/My Drive/ES 2020 Sample Size/es_sample_size_an/'


# Base con los parámetros estimados
# nom_base_estimaciones = 'muestras_prueba_790.csv'
data_par = pd.read_csv('muestras_prueba_790.csv')


data_par['e'] = data_par['ic_sup']-data_par['proporcion']
data_par0_filt = data_par[data_par.Muestra == 0].copy()
data_table_resum_col = ['Categoría','Parámetro','Promedio','Mínimo','Máximo']

n_muestra = data_par[data_par.Muestra == 1].tm.reset_index().loc[0,'tm']
min_muestra = data_par.Muestra.min() + 1
max_muestra = data_par.Muestra.max()


#Base tasa de respuesta
nom_base_tasas = 'tasas_790_parte1_cm1000.csv'
data_tasa_resp = pd.read_csv(nom_base_tasas)
data_tasa_resp_0 = data_tasa_resp[data_tasa_resp.muestra == 0].copy()
data_table_tp_col = ['Muestra','Promedio','SD','Mínimo','Máximo']

min_muestra_tp = data_tasa_resp.muestra.min() + 1
max_muestra_tp = data_tasa_resp.muestra.max()


# Inicia la app
app = dash.Dash()
server = app.server

colors = {
    'text' : 'rgb(134, 7, 14)',
    'plot_color' : '#C0C0C0',
    'paper_color' : '#ff0000'    
    }

app.layout = html.Div([

        html.H1(children = 'Análisis de disminución de muestra para el ES',  #Título del dashboard
                style = {
                    'textAlign' : 'center',
                    'color' : colors['text']
                    }
                ),

                 html.Br(),
       
       html.Div(children = 'Muestra: '+ str(n_muestra)+' UPMs',
                 style = {
                    'textAlign' : 'center',
                    'color' : colors['text']
                    }
                 ),
                 
       html.Div(className = 'row',
                         children=[
                                 html.Div([
                                         dcc.Markdown('''
                                        **Datos para gráficar**
                                        
                                        Seleccionar la información que aparecerá en la gráfica:
                                        
                                        ''')
                                        ], className = 'three columns')
                                        ]),
        
            # Desplegar para elegir dominios
        html.Label('Escoge un dominio'),
            
            dcc.Dropdown(
                    id = 'dropdown1',
                    options = [
                              {'label' : 'AMCM', 'value' : 'AMCM'},
                              {'label' : 'Monterrey', 'value' : 'MTY'},
                              {'label' : 'Guadalajara', 'value' : 'GDL'},
                              {'label' : '25 Ciudades', 'value' : 'PROV'},
                              {'label' : '28 Ciudades', 'value' : '28 CDS'} 
                              ],
                    value = 'AMCM'),
            
            html.Br(),
            html.Br(),
            
     # Inicio de los Tabs       
     dcc.Tabs(
         colors={
        "border": "white",
        "primary": "gold",
        "background": "cornsilk"},
        children= [
             
         # Primer tab  
         dcc.Tab(label='Estimación de proporciones', 
                 
                 selected_style = {'fontWeight': 'bold'},
                 
                 children=[
                 
                 html.Br(),
       
                 html.Div(children = 'Estimación de proporciones por nivel socieconómico, televisión de paga y operadores de TV de paga',
                 style = {
                    'textAlign' : 'center',
                    'color' : colors['text']
                    }
                 ),
                 
                html.Br(),
                
                #Primer control deslizante para seleccionar el número de muestras
                html.Label('Elija el número de muestras'),
                
                dcc.RangeSlider(
                    id = 'Slider1',
                    min = min_muestra,
                    max = max_muestra,
                    step = 1,
                    value = [1,1],
                    marks = {i : i for i in range(max_muestra + 1)}
                    ),
                
                
                 html.Div([
                         dcc.Markdown('''
                                       
                                      **Resumen estadístico de la/las muestras seleccionadas**
                                        
                                        ''')
                         ]),
                
                #Primera gráfica: De puntos                        
                html.Div([
                    dcc.Graph(
                            id = 'scatter_chart')
                    ]),
    
                html.Br(),
                html.Br(),
                
                 #Segunda gráfica: Box-plot
                html.Div([
                    dcc.Graph(
                            id = 'box_plot')
                    ]),
                
                html.Br(),
                html.Br(),
            
                html.Label('Escoge un parámetro'),
                
                #Checklist para la tabla 1
                dcc.Checklist(
                    id = 'checklist1',
                    options = [
                              {'label' : 'Proporcion', 'value' : 'proporcion'},
                              {'label' : 'SD', 'value' : 'sd'},
                              {'label' : 'CV', 'value' : 'cv'},
                              {'label' : 'deff', 'value' : 'deff'},
                              {'label' : 'Número de hogares', 'value' : 'n'} 
                              ],
                    value = ['proporcion','sd']),
            
                html.Br(),
                html.Br(),
                
                #Tabla 1
                html.Div([
                    dash_table.DataTable(
                            id='table1',
                            columns=[{"name": i, "id": i} for i in data_table_resum_col],
                            style_as_list_view=True,
                            style_cell={'padding': '4px'},
                            style_header={
                                    'backgroundColor': 'rgb(210, 210, 210)',
                                    'fontWeight': 'bold'
                                    },
                            style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                    },
                            style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }
                                    ],
                            style_cell_conditional=[
                                    {'if': {'column_id': 'Categoría'},
                                     'width': '30%'},
                                    {'if': {'column_id': 'Parámetro'},
                                      'width': '30%'},
                                    {'textAlign': 'center'}
                                      ],
                            )
                    ]),
                    
                 html.Br(),
                 html.Br(),
            
            ]
        ),
     
        # Seundo tab          
        dcc.Tab(label='Tasa de participación', 
             
             selected_style = {'fontWeight': 'bold'},
             
             children=[
             
             html.Br(),
             html.Div(children = 'Cálculo de la tasa de participación del ES19-I',
                      style = {
                              'textAlign' : 'center',
                              'color' : colors['text']
                              }
                      ),
             
             html.Br(),
             
             #Segundo control deslizante para seleccionar el número de muestras
             html.Label('Elija el número de muestras'),
             
             dcc.RangeSlider(
                    id = 'Slider2',
                    min = min_muestra_tp,
                    max = max_muestra_tp,
                    step = 10,
                    value = [1,1],
                    marks = {i : i for i in [min_muestra_tp,max_muestra_tp]}
                    ),

             html.Br(), 
             
             #Tercera gráfica: Histograma
             html.Div([
                    dcc.Graph(
                            id = 'histogram')
                    ]),
            
             #Tabla 2
              html.Div([
                    dash_table.DataTable(
                            id='table2',
                            columns=[{"name": i, "id": i} for i in data_table_tp_col],
                            style_as_list_view=True,
                            style_cell={'padding': '4px'},
                            style_header={
                                    'backgroundColor': 'rgb(210, 210, 210)',
                                    'fontWeight': 'bold'
                                    },
                            style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                    },
                            style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }
                                    ],
                            style_cell_conditional=[
                                    {'if': {'column_id': 'Muestra'},
                                     'width': '60%'},
                                    {'textAlign': 'center'}
                                      ],
                            )
                    ]),
                    
                    html.Br(), 
                    html.Br()
            
            
                    ]
             ) #Fin del segundo Tab          
    ])  #Fin de los Tabs       
])#Fin de la app


#Primer callback: Para gráfica de puntos
@app.callback(
    dash.dependencies.Output("scatter_chart", "figure"),
    [dash.dependencies.Input("dropdown1", "value"),
     dash.dependencies.Input("Slider1", "value")]
              )
#Primera definicion de funcion: para el primer callback
def update_fig(drop_value,slide_value):
    slide_value = np.arange(slide_value[0],slide_value[1]+1,1)
    data_par_filt = data_par[data_par.Muestra.isin(slide_value)].copy()
    data_par_filt2 = data_par_filt[data_par_filt.DOMINIO == drop_value].copy()
    data_par0_filt2 = data_par0_filt[data_par0_filt.DOMINIO == drop_value].copy()

    
    
    
    data = []
    
    
    graf_dom = go.Scatter(name = 'ES 19-I',
            x = data_par0_filt2.categoria,
            y = data_par0_filt2.proporcion,
            mode = 'markers',
            error_y=dict(type='data', 
                         array=data_par0_filt2.e,
                         thickness=1.5,
                         width=10),
            marker_color = 'rgba(152,0,0,.8)',
            marker_line_width=2,marker_size=8)
    
    graf_dom2 = go.Scatter(name = 'Muestra',    
            x = data_par_filt2.categoria,
            y = data_par_filt2.proporcion,
            mode = 'markers',
            marker_size=4
            #marker_color = data_par_filt2.prop,
            #text = data_par_filt2.prop.round(1)
            )
    
    data.append(graf_dom)
    data.append(graf_dom2)
    
    layout = {'title' : 'Gráfica de dispersión de las proporciones estimadas',
              'xaxis' : {'title' : 'Categoría'},
              'yaxis' : {'title' : 'Proporción estimada',
                         'range': [0,1]}}
    
    return{
        'data' : data,
        'layout' : layout
        }


#Segundo callback: Para box-plot
@app.callback(
    dash.dependencies.Output("box_plot", "figure"),
    [dash.dependencies.Input("dropdown1", "value"),
     dash.dependencies.Input("Slider1", "value")]
              )
#Segunda definicion de funcion: para el segundo callback
def update_fig2(drop_value,slide_value):
    slide_value = np.arange(slide_value[0],slide_value[1]+1,1)
    data_par_filt_b = data_par[data_par.Muestra.isin(slide_value)].copy()
    data_par_filt2_b = data_par_filt_b[data_par_filt_b.DOMINIO == drop_value].copy()


    
    
    
    data2 = []
    
    
    graf_dom_box = go.Box(x = data_par_filt2_b.categoria,
                          y = data_par_filt2_b.proporcion,
                          boxpoints='all', # can also be outliers, or suspectedoutliers, or False
                          jitter=0.4, # add some jitter for a better separation between points
                          pointpos=-1.8,
                          marker_color = 'rgb(107,174,214)',
                          line_color='rgb(8,81,156)',
                          marker_size=3,
                          boxmean=True) # relative position of points wrt box)
    

    
    data2.append(graf_dom_box)
    
    layout2 = {'title' : 'Box-plot de las proporciones estimadas',
              'xaxis' : {'title' : 'Categoría'},
              'yaxis' : {'title' : 'Proporción estimada',
                         'range': [0,1]}}
    
    return{
        'data' : data2,
        'layout' : layout2
        }
   
    
#Tercer callback: Para tabla
@app.callback(
    dash.dependencies.Output("table1", "data"),
    [dash.dependencies.Input("dropdown1", "value"),
     dash.dependencies.Input("Slider1", "value"),
     dash.dependencies.Input("checklist1", "value")]
              )

#Tercera definicion de funcion: para el tercer callback
def update_fig3(drop_value_c,slide_value_c,check_value_c):
    slide_value_c = np.arange(slide_value_c[0],slide_value_c[1]+1,1)
    data_table = data_par[data_par.Muestra.isin(slide_value_c)].copy()
    columnas = ['Muestra','DOMINIO','categoria','proporcion','cv','sd','deff','n','tm']

    data_table = data_table[columnas]
    data_table = data_table[data_table.DOMINIO == drop_value_c]

    data_table_melt = data_table.melt(id_vars=['Muestra','DOMINIO','categoria'], value_vars=['proporcion','cv','sd','deff','n','tm'])

    data_table_resum = data_table_melt.groupby(["categoria","variable"])['value'].agg([
       ('promedio','mean'),
       ('minimo', min),
       ('maximo', max)
        ]).reset_index()
    data_table_resum['promedio'] = data_table_resum.promedio.round(4) 
    data_table_resum['minimo'] = data_table_resum.minimo.round(4) 
    data_table_resum['maximo'] = data_table_resum.maximo.round(4) 
    data_table_resum = data_table_resum[data_table_resum.variable.isin(check_value_c)]
    data_table_resum = data_table_resum.rename(columns = {'categoria':'Categoría','variable':'Parámetro','promedio':'Promedio','minimo':'Mínimo','maximo':'Máximo'})

    cleanup_nums = {"Categoría": {"NSE_1": "NSE 1", "NSE_2": "NSE 2","NSE_3": "NSE 3", "NSE_4": "NSE 4","tv_rest":"TV Paga","sky":"SKY","dish":"Dish","cable":"Cable"},
                    "Parámetro": {"proporcion": "Proporcion", "sd": 'SD', "cv": 'CV', "n": 'Número de hogares'}}
      
    data_table_resum.replace(cleanup_nums, inplace=True)
    
    data_table_update = data_table_resum.to_dict("rows")

    return data_table_update


#Cuarto callback: Para histograma
@app.callback(
    dash.dependencies.Output("histogram", "figure"),
    [dash.dependencies.Input("dropdown1", "value"),
     dash.dependencies.Input("Slider2", "value")]
              )

#Cuarta definicion de funcion: para el cuarto callback
def update_fig4(drop_value_d,slide_value_d):
    slide_value_d = np.arange(slide_value_d[0],slide_value_d[1]+1,1)
    data_tp_filt = data_tasa_resp[data_tasa_resp.muestra.isin(slide_value_d)].copy()
    data_tp_filt2 = data_tp_filt[drop_value_d].copy()
    
    data3 = []
    
    histo_dom = go.Histogram(
            x = data_tp_filt2,
            xbins=dict( # bins used for histogram
            start=.70,
            end=1,
            ),
            marker_color='#330C73',
            opacity=0.75
            )
            
    line = go.layout.Shape(
            type="line",
            x0=.8,
            y0=0,
            x1=.8,
            y1=50,
            line=dict(
                color="Orange",
                width=4,
                dash="dash")    
            ),
            
            
    data3.append(line)
    data3.append(histo_dom)
    

    return{'data':data3}


#Quinto callback: Para segunda tabla
@app.callback(
    dash.dependencies.Output("table2", "data"),
    [dash.dependencies.Input("dropdown1", "value"),
     dash.dependencies.Input("Slider2", "value")]
              )

def update_fig5(drop_value_d,slide_value_d):
    slide_value_d = np.arange(slide_value_d[0],slide_value_d[1]+1,1)
    data_table_tp = data_tasa_resp[data_tasa_resp.muestra.isin(slide_value_d)].copy()
    data_table_tp = data_table_tp[{'muestra',drop_value_d}]
    
    data_table_tp0 = data_tasa_resp_0[{'muestra',drop_value_d}].copy()
    data_table_tp0 = data_table_tp0.rename(columns = {drop_value_d:'Promedio'})
    data_table_tp0['Promedio'] = data_table_tp0.Promedio.round(4) 
    data_table_tp0['muestra'] = 'ES19-1'
    data_table_tp0['Mínimo'] = 0
    data_table_tp0['Máximo'] = 0
    data_table_tp0['SD'] = 0
    
    
    data_table_tp['muestra'] = 1
    data_table_tp_resum = data_table_tp.groupby(["muestra"])[drop_value_d].agg([
       ('promedio','mean'),
       ('SD', 'std'),
       ('minimo', min),
       ('maximo', max)
        ]).reset_index()
    data_table_tp_resum['promedio'] = data_table_tp_resum.promedio.round(4) 
    data_table_tp_resum['SD'] = data_table_tp_resum.SD.round(4) 
    data_table_tp_resum['minimo'] = data_table_tp_resum.minimo.round(4) 
    data_table_tp_resum['maximo'] = data_table_tp_resum.maximo.round(4) 
    data_table_tp_resum = data_table_tp_resum.rename(columns = {'promedio':'Promedio','minimo':'Mínimo','maximo':'Máximo'})
    data_table_tp_resum['muestra'] = 'Muestras'

    frame = [data_table_tp0,data_table_tp_resum]
    data_table_resum_muest = pd.concat(frame)
    data_table_resum_muest = data_table_resum_muest.rename(columns = {'muestra':'Muestra'})
    
    data_table_update2 = data_table_resum_muest.to_dict("rows")

    return data_table_update2


if __name__ == '__main__':
    app.run_server(debug = True)