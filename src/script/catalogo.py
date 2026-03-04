import pandas as pd
import os
import re
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def limpiar_id(texto):
    return re.sub(r'\W+', '_', texto.lower())

raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

archivos_excel = [
    'LISTA BUDAS -50 CM.xlsx',
    'LISTA BUDAS +50 CM.xlsx'
]
productos_por_hoja = 9

dataframes = []

for archivo in archivos_excel:
    ruta_completa = os.path.join(raiz, 'data', archivo)

    if not os.path.exists(ruta_completa):
        continue

    nombre_categoria = archivo.replace('.xlsx', '')

    df_temp = pd.read_excel(ruta_completa, skiprows=1)
    df_temp.columns = ['ID_TIPO', 'PRODUCTO', 'MEDIDAS', 'PRECIO', 'ML']
    df_temp = df_temp.dropna(subset=['PRODUCTO'])

    df_temp['CATEGORIA'] = nombre_categoria
    df_temp['ID_CATEGORIA'] = limpiar_id(nombre_categoria)

    dataframes.append(df_temp)

df_completo = pd.concat(dataframes, ignore_index=True)

df_completo['PRECIO_MOSTRAR'] = df_completo['PRECIO'].apply(
    lambda x: f"${int(x):,}".replace(",", ".") if pd.notnull(x) and str(x).isnumeric() else "Sin stock"
)

df_completo['IMAGEN'] = 'imagenes/mockup_universal.jpg'

agrupado = {}
categorias = []

for cat, df_grupo in df_completo.groupby('CATEGORIA', sort=False):
    id_cat = df_grupo['ID_CATEGORIA'].iloc[0]
    agrupado[cat] = {'id': id_cat, 'productos': df_grupo.to_dict('records')}
    categorias.append({'nombre': cat, 'id': id_cat})

env = Environment(loader=FileSystemLoader(os.path.join(raiz, 'src', 'components')))
template = env.get_template('main.html')

html_renderizado = template.render(
    categorias=categorias,
    agrupado=agrupado,
    items_per_page=productos_por_hoja,
    fondo_portada='imagenes/fondo_portada.jpg',
    logo='imagenes/logo.png',
    telefono='+54 9 11 6532-8554',
    instagram='@ViveroFlorDeAzahar',
    direccion='Los Arces 2063, La Lonja'
)

HTML(string=html_renderizado, base_url=raiz).write_pdf(os.path.join(raiz, 'Catalogo_Modular.pdf'))

HTML(string=html_renderizado, base_url=raiz).write_pdf(os.path.join(raiz, 'Catalogo_Modular.pdf'))