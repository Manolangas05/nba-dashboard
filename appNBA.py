import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="NBA Dashboard", layout="wide")
st.title("NBA Dashboard - Analisis de Temporadas")

@st.cache_data
def load_data():
    df = pd.read_csv('nba_all_elo.csv')
    df['date_game'] = pd.to_datetime(df['date_game'])
    return df

df = load_data()

st.sidebar.title("Filtros")
años_disponibles = sorted(df['year_id'].unique())
año_seleccionado = st.sidebar.selectbox(
    "Selecciona un año:",
    años_disponibles,
    index=len(años_disponibles)-1
)

df_año = df[df['year_id'] == año_seleccionado]

equipos = sorted(df_año['team_id'].unique())
equipo_seleccionado = st.sidebar.selectbox(
    "Selecciona un equipo:",
    equipos
)

tipo_juego = st.sidebar.radio(
    "Tipo de juego:",
    options=["Temporada Regular", "Playoffs", "Ambos"],
    horizontal=True
)

df_filtrado = df_año[df_año['team_id'] == equipo_seleccionado].copy()

if tipo_juego == "Temporada Regular":
    df_filtrado = df_filtrado[df_filtrado['is_playoffs'] == 0]
elif tipo_juego == "Playoffs":
    df_filtrado = df_filtrado[df_filtrado['is_playoffs'] == 1]

df_filtrado = df_filtrado.sort_values('date_game').reset_index(drop=True)
df_filtrado['wins_cumsum'] = (df_filtrado['game_result'] == 'W').cumsum()
df_filtrado['losses_cumsum'] = (df_filtrado['game_result'] == 'L').cumsum()

col1, col2, col3 = st.columns(3)
with col1:
    total_games = len(df_filtrado)
    st.metric("Total de Juegos", total_games)
with col2:
    total_wins = (df_filtrado['game_result'] == 'W').sum()
    st.metric("Juegos Ganados", total_wins)
with col3:
    total_losses = (df_filtrado['game_result'] == 'L').sum()
    st.metric("Juegos Perdidos", total_losses)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Acumulado de Juegos Ganados y Perdidos")
    fig, ax = plt.subplots(figsize=(10, 6))
    x_values = range(1, len(df_filtrado) + 1)
    ax.plot(x_values, df_filtrado['wins_cumsum'], 
            label='Juegos Ganados', color='#2ecc71', linewidth=2.5, marker='o', markersize=4)
    ax.plot(x_values, df_filtrado['losses_cumsum'], 
            label='Juegos Perdidos', color='#e74c3c', linewidth=2.5, marker='o', markersize=4)
    ax.set_xlabel('Numero de Juego', fontsize=12)
    ax.set_ylabel('Acumulado', fontsize=12)
    ax.set_title(f'{equipo_seleccionado} - Año {año_seleccionado} - {tipo_juego}', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

with col2:
    st.subheader("Distribucion de Resultados")
    sizes = [total_wins, total_losses]
    labels = [f'Ganados\n{total_wins}', f'Perdidos\n{total_losses}']
    colors = ['#2ecc71', '#e74c3c']
    explode = (0.05, 0.05)
    
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax2.pie(
        sizes, 
        labels=labels, 
        autopct='%1.1f%%',
        colors=colors,
        explode=explode,
        startangle=90,
        textprops={'fontsize': 11, 'weight': 'bold'}
    )
    
    ax2.set_title(f'Porcentaje de W/L - {equipo_seleccionado} {año_seleccionado}', 
                  fontsize=12, fontweight='bold', pad=20)
    
    st.pyplot(fig2)
