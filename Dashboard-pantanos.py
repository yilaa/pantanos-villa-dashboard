#Dashboard Pantanos de Villa
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.write("""
# Aves en los Pantanos de Villa
Data del portal de Datos abiertos de la Municipalidad de Lima
""")

num_especies = pd.read_csv('numero-especies.csv')
total_aves = pd.read_csv('total_aves_por_zona_por_mes.csv')  

#Familias y tipos de aves

# aves1= aves.iloc[:,0:16]

# print(aves1.groupby(['STATUS']).count())


#Graficos
#Preparando data para que esté lista para gráficos
months = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
          "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
num_especies['mes'] = pd.Categorical(num_especies['mes'], categories=months, ordered=True)
total_aves['mes'] = pd.Categorical(total_aves['mes'], categories=months, ordered=True)
data1 = num_especies.sort_values(by="mes")
data2 = total_aves.sort_values(by="mes")
data1.columns = data1.columns.get_level_values(0)
data1['año']=data1['año'].astype('Int64')
cols = data1.select_dtypes(include=['object']).columns
data1[cols] = data1[cols].apply(pd.to_numeric, downcast='float', errors='coerce')
print(data1.info())

"""
## Total de aves por mes (2019 y 2020) """
data2['TOTAL']= data2.iloc[:,2:].sum(axis=1)
AvesMes2019 = data2['mes'][data2['año']==2019].values
AvesMes2020 = data2['mes'][data2['año']==2020].values
AvesTotal2019 = data2['TOTAL'][data2['año']==2019].values
AvesTotal2020 = data2['TOTAL'][data2['año']==2020].values
fig1,ax1 = plt.subplots(figsize=(14,5))
plt.plot(AvesMes2019,AvesTotal2019, marker='.',label ='2019')
plt.plot(AvesMes2020,AvesTotal2020, marker='.',label ='2020')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
ax1.set_title('Total de aves por mes')
ax1.set_ylabel('Total aves')
ax1.set_xlabel('Mes')
plt.grid()
st.pyplot(fig1)


"""
## Número de especies de aves por mes (2019 y 2020) """
data1['TOTAL']= data1.iloc[:,2:].sum(axis=1)
EspeciesMes2019 = data1['mes'][data1['año']==2019].values
EspeciesMes2020 = data1['mes'][data1['año']==2020].values
EspeciesTotal2019 = data1['TOTAL'][data1['año']==2019].values
EspeciesTotal2020 = data1['TOTAL'][data1['año']==2020].values
fig2, ax2 = plt.subplots(figsize=(14,5))
plt.plot(EspeciesMes2019,EspeciesTotal2019, marker='.',label = '2019')
plt.plot(EspeciesMes2020,EspeciesTotal2020, marker='.',label = '2020')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
#Definir título y nombres de ejes
ax2.set_title('Número de especies de aves por zona y mes')
ax2.set_ylabel('Total especies por zona')
ax2.set_xlabel('Mes')
plt.grid()
st.pyplot(fig2)

import streamlit.components.v1 as components
components.iframe("https://bitsviajeros.com/mapas/pantanos/",height=600)
