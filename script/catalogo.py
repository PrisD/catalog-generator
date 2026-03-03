import pandas as pd
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

archivos_excel = [
    'LISTA BUDAS -50 CM.xlsx',
    'LISTA BUDAS +50 CM.xlsx'
]

dataframes = []

for archivo in archivos_excel:
    nombre_categoria = archivo.replace('.xlsx', '')

    df_temp = pd.read_excel(archivo, skiprows=1)
    df_temp.columns = ['ID_TIPO', 'PRODUCTO', 'MEDIDAS', 'PRECIO', 'ML']
    df_temp = df_temp.dropna(subset=['PRODUCTO'])

    df_temp['CATEGORIA'] = nombre_categoria
    dataframes.append(df_temp)

df_completo = pd.concat(dataframes, ignore_index=True)

df_completo['PRECIO_MOSTRAR'] = df_completo['PRECIO'].apply(
    lambda x: f"${int(x)}" if pd.notnull(x) and str(x).isnumeric() else "Sin stock"
)

df_completo['IMAGEN'] = df_completo['PRODUCTO'].apply(
    lambda x: f"imagenes/{str(x).replace(' ', '_').lower()}.jpg"
)

productos_por_hoja = 9

agrupado = {cat: df_grupo.to_dict('records') for cat, df_grupo in df_completo.groupby('CATEGORIA', sort=False)}

env = Environment(loader=FileSystemLoader('..'))
template = env.get_template('catalogo.html')

html_renderizado = template.render(
    agrupado=agrupado,
    items_per_page=productos_por_hoja
)

HTML(string=html_renderizado).write_pdf("Catalogo_Vivero.pdf")