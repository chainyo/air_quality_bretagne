import pandas as pd 
import seaborn as sns 
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots

# Import des données
df = pd.read_csv('ind_bretagne_agglo.csv')

# Reformmatage des colonnes des dates
date = []
for col, row in df['date_ech'].iteritems():
    row = row.split('T')[0]
    date.append(row)
df.insert(2, "date", date, True)

df = df.drop(['FID', 'date_ech', 'code_zone', 'source'], axis=1)

# Dataframe pour les graphs subplots scatter
data = [df['date'], df['valeur'], df['lib_zone']]
headers = ['Date', 'Qualité de l\'air', 'Zone']
df_qualif_zone = pd.concat(data, axis=1, keys=headers)

# Séparation des dataframes pour graph subplots en fonction des zones
df_quali_saint_brieuc = df_qualif_zone.loc[df_qualif_zone['Zone'] == 'CA Saint-Brieuc Armor']
df_quali_morbi = df_qualif_zone.loc[df_qualif_zone['Zone'] == 'CA Golfe du Morbihan - Vannes']
df_quali_quimper = df_qualif_zone.loc[df_qualif_zone['Zone'] == 'CA Quimper Bretagne Occidentale']
df_quali_rennes = df_qualif_zone.loc[df_qualif_zone['Zone'] == 'Rennes Métropole']
df_quali_brest = df_qualif_zone.loc[df_qualif_zone['Zone'] == 'Brest Métropole']
df_quali_lorient = df_qualif_zone.loc[df_qualif_zone['Zone'] == 'CA Lorient']
df_quali_malo = df_qualif_zone.loc[df_qualif_zone['Zone'] == 'CA du Pays de Saint-Malo (Saint-Malo Agglomération)']

# Subplots sur l'évolution de la qualité de l'air
fig1 = make_subplots(rows=7, cols=1, shared_xaxes=True, shared_yaxes=True)

# Traces
fig1.add_trace(go.Scatter(x=df_quali_brest['Date'], y=df_quali_brest['Qualité de l\'air'], name='Brest Métropole'), row=1, col=1)
fig1.add_trace(go.Scatter(x=df_quali_rennes['Date'], y=df_quali_rennes['Qualité de l\'air'], name='Rennes Métropole'), row=2, col=1)
fig1.add_trace(go.Scatter(x=df_quali_lorient['Date'], y=df_quali_lorient['Qualité de l\'air'], name='CA Lorient'), row=3, col=1)
fig1.add_trace(go.Scatter(x=df_quali_quimper['Date'], y=df_quali_quimper['Qualité de l\'air'], name='CA Quimper Bretagne Occidentale'), row=4, col=1)
fig1.add_trace(go.Scatter(x=df_quali_morbi['Date'], y=df_quali_morbi['Qualité de l\'air'], name='CA Golfe du Morbihan - Vannes'), row=5, col=1)
fig1.add_trace(go.Scatter(x=df_quali_malo['Date'], y=df_quali_malo['Qualité de l\'air'], name='CA du Pays de Saint-Malo (Saint-Malo Agglomération)'), row=6, col=1)
fig1.add_trace(go.Scatter(x=df_quali_saint_brieuc['Date'], y=df_quali_saint_brieuc['Qualité de l\'air'], name='CA Saint-Brieuc Armor'), row=7, col=1)

# X axis
fig1.update_xaxes(title_text='Dates', row=7)

# Y axis
fig1.update_yaxes(title_text='Qualité de l\'air', row=4)

# Subplots layout
fig1.update_layout(title='Evolution de la qualité de l\'air dans les différentes zones de Bretagne', width=1200, height=800)


# Dataframe pour les graphs subplots pie
data_pie = [df['qualif'], df['lib_zone']]
headers_pie = ['Qualité', 'Zone']
df_pie = pd.concat(data_pie, axis=1, keys=headers_pie)

zones_cnt = df_pie.groupby('Zone')['Qualité'].apply(lambda x: x.value_counts())

# Subplots sur l'évolution de la qualité de l'air
specs=[[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}]]
fig2 = make_subplots(rows=4, cols=2, specs=specs)

# Traces
fig2.add_trace(go.Pie(labels=zones_cnt['Brest Métropole'].index, values=zones_cnt['Brest Métropole'].values, name='Brest Métropole', title='Brest'), 1, 1)
fig2.add_trace(go.Pie(labels=zones_cnt['Rennes Métropole'].index, values=zones_cnt['Rennes Métropole'].values, name='Rennes Métropole', title='Rennes'), 1, 2)
fig2.add_trace(go.Pie(labels=zones_cnt['CA Lorient'].index, values=zones_cnt['CA Lorient'].values, name='CA Lorient', title='Lorient'), 2, 1)
fig2.add_trace(go.Pie(labels=zones_cnt['CA Quimper Bretagne Occidentale'].index, values=zones_cnt['CA Quimper Bretagne Occidentale'].values, name='CA Quimper Bretagne Occidentale', title='Quimper'), 2, 2)
fig2.add_trace(go.Pie(labels=zones_cnt['CA Golfe du Morbihan - Vannes'].index, values=zones_cnt['CA Golfe du Morbihan - Vannes'].values, name='CA Golfe du Morbihan - Vannes', title='Vannes'), 3, 1)
fig2.add_trace(go.Pie(labels=zones_cnt['CA Saint-Brieuc Armor'].index, values=zones_cnt['CA Saint-Brieuc Armor'].values, name='CA Saint-Brieuc Armor', title='St-Brieuc'), 3, 2)
fig2.add_trace(go.Pie(labels=zones_cnt['CA du Pays de Saint-Malo (Saint-Malo Agglomération)'].index, values=zones_cnt['CA du Pays de Saint-Malo (Saint-Malo Agglomération)'].values, name='CA du Pays de Saint-Malo (Saint-Malo Agglomération)', title='St-Malo'), 4, 1)

# Hole to donut
fig2.update_traces(hole=0.5, hoverinfo="label+percent+name")

# Subplots layout
fig2.update_layout(title='Différentes proportions de la qualité de l\'air en Bretagne', width=1180, height=1400, font=dict(size=22, color="RebeccaPurple"))

# Formattage des mois pour graphs PM10 et 25
mois = []
for col, row in df['date'].iteritems():
    row = row.split('-')
    mois.append(f'{row[0]}-{row[1]}')
df.insert(2, "mois", mois, True)

# Dataframe pour les graphs particules PM10
data_particules = [df['mois'], df['lib_zone'], df['val_pm10']]
headers_particules = ['Date', 'Zone', 'Valeur PM10']
df_particules_pm10 = pd.concat(data_particules, axis=1, keys=headers_particules)

# Graph fines particules pm10
fig_particules_pm10 = px.histogram(df_particules_pm10, x='Date', y='Valeur PM10', color='Zone', histfunc='avg')
fig_particules_pm10.update_layout(width=1200, height=400, title_text='Moyenne du sous-indice de particules fines de diamètre inférieur à 10 μm en fonction du mois de l\'année', yaxis_title_text='Valeur du sous-indice PM10', barmode='group')
fig_particules_pm10.update_xaxes(dtick='M1', tickformat='%b')

# Dataframe pour les graphs O3
data_O3 = [df['mois'], df['lib_zone'], df['val_o3']]
headers_O3 = ['Date', 'Zone', 'Sous-indice O3']
df_o3 = pd.concat(data_O3, axis=1, keys=headers_O3)

# Graph fines particules pm10
fig_o3 = px.histogram(df_o3, x='Date', y='Sous-indice O3', color='Zone', histfunc='avg')
fig_o3.update_layout(width=1200, height=400, title_text='Moyenne du sous-indice de O3 en fonction du mois de l\'année', yaxis_title_text='Valeur du sous-indice O3', barmode='group')
fig_o3.update_xaxes(dtick='M1', tickformat='%b')

# Dataframe for tabs
data_tab = [df['lib_zone'], df['valeur'], df['val_no2'], df['val_so2'], df['val_o3'], df['val_pm10']]
headers_tab = ['Zone', 'Moyenne valeur', 'Moyenne valeur NO2', 'Moyenne valeur SO2', 'Moyenne valeur O3', 'Moyenne valeur PM10']
df_tabs = pd.concat(data_tab, axis=1, keys=headers_tab)
df_tabs = df_tabs.groupby('Zone', as_index=False).apply(lambda x: x.mean().round(2))

tables = go.Figure(data=[go.Table(
    header=dict(values=df_tabs.columns, font=dict(size=15), align='left', fill_color='palegreen'),
    cells=dict(values=[df_tabs['Zone'], df_tabs['Moyenne valeur'], df_tabs['Moyenne valeur NO2'], df_tabs['Moyenne valeur SO2'], 
    df_tabs['Moyenne valeur O3'], df_tabs['Moyenne valeur PM10']], align='left', fill_color='lavender'))])
tables.update_layout(width=900, height=600)

# Matrice de confusion des différents relevés
fig_conf_matrix = sns.heatmap(df.drop('val_so2', axis=1).corr())

# Préparation des coordonnées pour la cartographie
data_coord = [df['lib_zone'], df['geom']]
headers_coord = ['Zone', 'Coordonnées']
df_coord = pd.concat(data_coord, axis=1, keys=headers_coord)

longitude, latitude = [], []
for col, row, in df_coord['Coordonnées'].iteritems():
    long = row.split('(')[1].split(' ')[0]
    lat = row.split('(')[1].split(' ')[1].split(')')[0]
    longitude.append(long)
    latitude.append(lat)

df_coord.insert(2, 'Longitude', longitude, True)
df_coord.insert(3, 'Latitude', latitude, True)

df_coord.drop('Coordonnées', axis=1, inplace=True)

df_coord['Longitude'] = df_coord['Longitude'].astype('float32')
df_coord['Latitude'] = df_coord['Latitude'].astype('float32')

# Agrégation des coordonnées
df_coord = df_coord.groupby(by=['Zone']).mean()

# Tableau des coordonnées
table_coord = go.Figure(data=[go.Table(
    header=dict(values=['Zone', 'Longitude', 'Latitude'], font=dict(size=15), align='left', fill_color='palegreen'),
    cells=dict(values=[df_coord.index, df_coord['Longitude'], df_coord['Latitude']], align='left', fill_color='lavender')
)])
table_coord.update_layout(width=900, height=400)