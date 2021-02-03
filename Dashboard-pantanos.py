#Dashboard Pantanos de Villa
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

"""
# ¿Qué aves podemos ver en los Pantanos de Villa?
Con data del monitoreo de aves publicado en el portal de **Datos abiertos de la Municipalidad de Lima**, he elaborado esta aplicación para difundir:  
- Cuál es la población de aves
- Cómo se clasifican
- Buscador de aves que muestra sus avistamientos.  
  
Espero sea útil y todos sus comentarios para mejorar a **indira@viajaporperu.com**  
Saludos  
Indira
"""

#Preparación de data
st.cache(persist=True)
def load_data():
  aves = pd.read_csv('aves.csv')
  total_aves = aves.groupby(['mes','año']).sum()
  total_aves.reset_index(inplace=True)
  numero_especies = aves.groupby(['mes','año']).count()
  numero_especies.reset_index(inplace=True)
  return aves, total_aves, numero_especies

aves, total_aves, numero_especies = load_data()

"""
## ¿Cuántas aves viven en los Pantanos de Villa?
**Diciembre y Enero** son buenos meses para ver aves, más de 10 mil aves  
¿Por qué tanta diferencia entre Febrero 2019 y 2020?  

Gráfico 1:  **Total de Aves por mes** """

AvesTotalMes = alt.Chart(total_aves).mark_line(point=True).encode(
  x=alt.X('mes:O', sort = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
  "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"],
  axis=alt.Axis(title='Mes')),
  y=alt.Y('TOTALES:Q', axis=alt.Axis(title='Total de Aves')),
  color=alt.Color('año:N', scale=alt.Scale(range=['#fcba03', '#fc3103'])),
  tooltip = ['TOTALES','año', 'mes']
)
st.altair_chart(AvesTotalMes, use_container_width=True)


"""
##  Y en cuanto a diversidad, ¿cuántas especies de aves hay?
Entre 54 y 77 especies de aves por mes.  
Gráfico 2: **Total de especies por mes**
"""
EspeciesTotalMes = alt.Chart(numero_especies).mark_line(point=True).encode(
  x=alt.X('mes:O', sort = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
  "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"],
  axis=alt.Axis(title='Mes')),
  y=alt.Y('TOTALES', axis=alt.Axis(title='Total de Especies')),
  color=alt.Color('año:N',scale=alt.Scale(range=['#fcba03', '#fc3103'])),
  tooltip = ['TOTALES','año', 'mes']   
).interactive()
st.altair_chart(EspeciesTotalMes, use_container_width=True)

"""
## ¿Cómo se clasifican las aves por estacionalidad?
Clasificación brindada por Pantanos de Villa  
** Las Migratorias Boreales ** son la mayoría en Diciembre, Enero y Febrero.
"""

# Estacionalidad = alt.Chart(aves).mark_circle().encode(
#     alt.X('mes', scale=alt.Scale(zero=False)),
#     alt.Y('TOTALES', scale=alt.Scale(zero=False, padding=1)),
#     color='STATUS',
#     tooltip = ['STATUS','TOTALES']  
# )
# st.altair_chart(Estacionalidad, use_container_width=True)

aves_status= aves.groupby(['año','mes','STATUS']).sum()
aves_status.reset_index(inplace=True)

Status = alt.Chart(aves_status).mark_bar().encode(
  x=alt.X('año:N'),
  y=alt.Y('TOTALES'),
  color= alt.Color('STATUS', sort = ['Residente','Migratorio Boreal', 'Migratorio Local','Migratorio Autral', 'Migratorio Andino','Raro', 'H', 'MI']),
  column=alt.Column('mes:O', sort = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
  "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]),
  tooltip = ['STATUS','TOTALES']   
).interactive()
st.altair_chart(Status)

"""
## Busca tu ave y mira su monitoreo """
listaAves = sorted(aves['NOMBRE COMUN'].unique())
select_aves = st.selectbox('Selecciona Ave', listaAves)
#st.checkbox("Mostrar gráfico", False, key=1)

grafico = alt.Chart(aves[aves['NOMBRE COMUN']== select_aves]).mark_line(point=True).encode(
  x=alt.X('mes:O', sort = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
  "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"],
  axis=alt.Axis(title='Mes')),
  y=alt.Y('TOTALES', axis=alt.Axis(title='Total')),
  color=alt.Color('año:O', scale=alt.Scale(range=['#fcba03', '#fc3103'])),
  tooltip = ['TOTALES','año', 'mes']
)
tipoAve = aves[aves['NOMBRE COMUN']== select_aves].STATUS.unique()
if st.checkbox('Mostrar gráfico', True, key=1):
  st.markdown("### Monitoreo de %s " % (select_aves))
  st.markdown("Está clasificada como %s " % (tipoAve[0]))
  st.altair_chart(grafico, use_container_width=True)


"""
## Mapa de Aves por zonas"""
import streamlit.components.v1 as components
components.iframe("https://bitsviajeros.com/mapas/pantanos/",height=700)

# VISITANTES A PANTANOS DE VILLA 2019

# visitantes = pd.read_csv('Visitantes-2019.csv')

# visitantes.set_index('MES', inplace= True)

# visitantes_tipo = visitantes.T

# visitantes_tipo.loc['Visitantes_por_mes']= visitantes_tipo.sum()

# visitantes_tipo['Total_año'] = visitantes_tipo.sum(axis=1)

# visitantes_tipo.columns

# visitantes_totalmes =visitantes_tipo.iloc[6:,:]

# visitantes_totalmes