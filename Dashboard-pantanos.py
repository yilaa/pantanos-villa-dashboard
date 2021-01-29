#Dashboard Pantanos de Villa
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

st.write("""
# Aves en los Pantanos de Villa
Data del portal de Datos abiertos de la Municipalidad de Lima
""")
st.sidebar.markdown('🦠 **Dashboard Pantanos de Villa** 🦠 ')
st.sidebar.markdown(''' 
Esta aplicación está hecha para dar información sobre el monitoreo de aves en los Pantanos de Villa.
Todos los datos son del portal de Datos abiertos de la Municipalidad de Lima.
                    
Diseñado por: 
**Indira Palomino**  ''')  

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
## Total de aves por mes (2019 y 2020) con altair"""

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
## Número de especies de aves por mes (2019 y 2020) """
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
## Número de especies por estado (2019 y 2020) """
aves_status= aves.groupby(['año','STATUS']).count()
aves_status.reset_index(inplace=True)

Status = alt.Chart(aves_status).mark_bar().encode(
  x=alt.X('año:O', axis=None),
  y=alt.Y('TOTALES', axis=alt.Axis(title='Total de Especies')),
  column = alt.Column('STATUS', title= 'Aves por Tipo de Estacionalidad', sort = ['R','Mb','Ml','Ma','Acc','S','H','MI']),
  color = alt.Color('año:O', scale=alt.Scale(range=['#fcba03', '#fc3103'])),
  tooltip = ['TOTALES','año']   
).properties(width=30).configure_header(
    labelOrient='bottom',
    titleOrient='bottom',
).configure_view(strokeWidth=0.0)

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
  y='TOTALES',
  color=alt.Color('año:O', scale=alt.Scale(range=['#fcba03', '#fc3103'])),
  tooltip = ['TOTALES','año', 'mes']
)
if st.checkbox('Mostrar gráfico', True, key=1):
  st.markdown("### Monitoreo de %s " % (select_aves))
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