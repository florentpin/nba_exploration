import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import functions.py


# Charger les données avec cache pour rapidité
@st.cache_data
def load_data():
    df = pd.read_csv('data/game.csv')
    df['game_date'] = pd.to_datetime(df['game_date'])
    return df

df_game_nba = load_data()

# --- Fonctions graphiques ---

# def create_fta_graph(df):
#     df_filtered = df.dropna(subset=['fta_home', 'fta_away']).copy()
#     offsets = df_filtered.groupby('game_date').cumcount()
#     df_filtered['game_date_adjusted'] = df_filtered['game_date'] + pd.to_timedelta(offsets, unit='h')
#     fig = px.scatter(df_filtered, x='game_date_adjusted', y=['fta_home', 'fta_away'],
#                     labels={'value': 'Nombre de lancers francs', 'variable': 'Type d’équipe', 'game_date_adjusted': 'Date'},
#                     color_discrete_map={'fta_home': 'blue', 'fta_away': 'red'},
#                     hover_data={'game_id': True, 'team_name_home': True, 'team_name_away': True})
#     fig.update_traces(
#         hovertemplate="<b>%{hovertext}</b><br>" +
#                       "Date: %{x}<br>" +
#                       "Lancers francs: %{y}<br>" +
#                       "Match ID: %{customdata[0]}<br>" +
#                       "Home Team: %{customdata[1]}<br>" +
#                       "Away Team: %{customdata[2]}<br>" +
#                       "<extra></extra>")
#     return fig

# def create_avg_matches_graph(df):
#     df = df.copy()
#     df['season_start_year'] = df['game_date'].dt.year
#     df['season_end_year'] = df['season_start_year'] + 1
#     df['season_name'] = df['season_start_year'].astype(str) + '-' + df['season_end_year'].astype(str)
#     matches_per_team_per_season = df.groupby(['season_name', 'team_id_home']).size().reset_index(name='matches_count')
#     avg_matches = matches_per_team_per_season.groupby('season_name')['matches_count'].mean().reset_index()
#     fig = px.bar(avg_matches, x='season_name', y='matches_count',
#                  labels={'season_name': 'Saison', 'matches_count': 'Moyenne du nombre de matchs'})
#     fig.update_layout(title='Moyenne du nombre de matchs par équipe et par saison', xaxis_tickangle=45)
#     return fig

# def create_shots_evolution_graph(df):
#     df_filtered = df[(df['game_date'].dt.year >= 1990) & (df['game_date'].dt.year <= 2023)].copy()
#     df_filtered['season_start_year'] = df_filtered['game_date'].dt.year
#     df_filtered['season_name'] = df_filtered['season_start_year'].astype(str) + '-' + (df_filtered['season_start_year'] + 1).astype(str)
#     season_stats = df_filtered.groupby('season_name').agg({
#         'fg3a_home': 'mean', 'fg3m_home': 'mean',
#         'fga_home': 'mean', 'fgm_home': 'mean',
#         'fta_home': 'mean', 'ftm_home': 'mean'
#     }).reset_index()
#     season_stats.columns = [
#         'season_name', 'avg_fg3a', 'avg_fg3m',
#         'avg_fga', 'avg_fgm', 'avg_fta', 'avg_ftm'
#     ]
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=season_stats['season_name'], y=season_stats['avg_fg3a'], mode='lines', name='3PA', line=dict(color='blue')))
#     fig.add_trace(go.Scatter(x=season_stats['season_name'], y=season_stats['avg_fg3m'], mode='lines', name='3PM', line=dict(color='blue', dash='dash')))
#     fig.add_trace(go.Scatter(x=season_stats['season_name'], y=season_stats['avg_fga'], mode='lines', name='2PA', line=dict(color='green')))
#     fig.add_trace(go.Scatter(x=season_stats['season_name'], y=season_stats['avg_fgm'], mode='lines', name='2PM', line=dict(color='green', dash='dash')))
#     fig.add_trace(go.Scatter(x=season_stats['season_name'], y=season_stats['avg_fta'], mode='lines', name='FTA', line=dict(color='red')))
#     fig.add_trace(go.Scatter(x=season_stats['season_name'], y=season_stats['avg_ftm'], mode='lines', name='FTM', line=dict(color='red', dash='dash')))
#     fig.update_layout(
#         title='Évolution moyenne des tentatives et réussites de tirs (1990-2023)',
#         xaxis_title='Saison',
#         yaxis_title='Moyenne des tentatives et réussites',
#         legend_title='Type de tir',
#         xaxis_tickangle=45
#     )
#     return fig

# def create_efficiency_graph(df):
#     df = df.copy()
#     df['season_start_year'] = df['game_date'].apply(lambda d: d.year if d.month < 8 else d.year)
#     df['season_name'] = df['season_start_year'].astype(str) + '-' + (df['season_start_year'] + 1).astype(str)
#     df_filtered = df[(df['season_start_year'] >= 1980) & (df['season_start_year'] <= 2023)].copy()
#     season_stats = df_filtered.groupby('season_name').agg({
#         'fg3m_home': 'sum',
#         'fg3a_home': 'sum',
#         'fgm_home': 'sum',
#         'fga_home': 'sum'
#     }).reset_index()
#     season_stats['fg2m'] = season_stats['fgm_home'] - season_stats['fg3m_home']
#     season_stats['fg2a'] = season_stats['fga_home'] - season_stats['fg3a_home']
#     season_stats['eff_2pt'] = season_stats['fg2m'] * 2 / season_stats['fg2a']
#     season_stats['eff_3pt'] = season_stats['fg3m_home'] * 3 / season_stats['fg3a_home']
#     season_stats['pct_2pt'] = season_stats['fg2m'] / season_stats['fg2a']
#     season_stats['pct_3pt'] = season_stats['fg3m_home'] / season_stats['fg3a_home']
#     season_stats['vol_2pt'] = season_stats['fg2a']
#     season_stats['vol_3pt'] = season_stats['fg3a_home']

#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=season_stats['season_name'], y=season_stats['eff_2pt'],
#                              name='Rentabilité 2 pts (points/tir)', line=dict(color='green', width=2), yaxis='y1'))
#     fig.add_trace(go.Scatter(x=season_stats['season_name'], y=season_stats['eff_3pt'],
#                              name='Rentabilité 3 pts (points/tir)', line=dict(color='blue', width=2), yaxis='y1'))
#     fig.add_trace(go.Scatter(x=season_stats['season_name'], y=season_stats['pct_2pt'],
#                              name='% réussite 2 pts', line=dict(color='green', dash='dot', width=2), yaxis='y2'))
#     fig.add_trace(go.Scatter(x=season_stats['season_name'], y=season_stats['pct_3pt'],
#                              name='% réussite 3 pts', line=dict(color='blue', dash='dot', width=2), yaxis='y2'))
#     fig.add_trace(go.Scatter(x=season_stats['season_name'].shift(-1).fillna(season_stats['season_name'].iloc[-1]), y=season_stats['vol_2pt'],
#                              name='Volume 2 pts', line=dict(color='green', dash='dash', width=2), yaxis='y3'))
#     fig.add_trace(go.Scatter(x=season_stats['season_name'].shift(-1).fillna(season_stats['season_name'].iloc[-1]), y=season_stats['vol_3pt'],
#                              name='Volume 3 pts', line=dict(color='blue', dash='dash', width=2), yaxis='y3'))

#     fig.update_layout(
#         title='Évolution comparée : tirs à 2 points vs tirs à 3 points (1980–2023)',
#         title_x=0.5,
#         xaxis=dict(title='Saison', tickangle=45, showgrid=False, zeroline=False),
#         yaxis=dict(title='Rentabilité (points par tir)', titlefont=dict(color='black'), tickfont=dict(color='black'),
#                    side='left', range=[0.5, 2.2], showgrid=True, gridwidth=1, gridcolor='lightgray'),
#         yaxis2=dict(title='% de réussite', titlefont=dict(color='gray'), tickfont=dict(color='gray'),
#                     overlaying='y', side='right', range=[0.3, 0.7], position=1.0, showgrid=False),
#         yaxis3=dict(title='Volume de tirs', titlefont=dict(color='purple'), tickfont=dict(color='purple'),
#                     overlaying='y', side='right', anchor='free', position=0.85,
#                     range=[season_stats[['vol_2pt', 'vol_3pt']].min().min() * 0.8,
#                            season_stats[['vol_2pt', 'vol_3pt']].max().max() * 1.1], showgrid=False),
#         legend=dict(x=0.5, y=1.15, orientation='h', xanchor='center')
#     )
#     return fig


# def create_stats_per_team(df_game_nba):
    

#     return fig


# --- Interface Streamlit ---

st.title("Analyse des données NBA")

tabs = st.tabs([
    "Lancers francs par match",
    "Moyenne matchs par saison",
    "Évolution tirs et réussites",
    "Statistiques par équipe"
])

with tabs[0]:
    st.header("Lancers francs par match")
    fig = functions.create_fta_graph(df_game_nba)
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.header("Moyenne du nombre de matchs par équipe et par saison")
    fig = functions.create_avg_matches_graph(df_game_nba)
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.header("Évolution moyenne des tirs et réussites (1990-2023)")
    fig = functions.create_shots_evolution_graph(df_game_nba)
    st.plotly_chart(fig, use_container_width=True)

with tabs[3]:

    st.header("Statistiques par équipe")

    equipe_selectionnee = st.selectbox(
        "Quelle équipe veux-tu analyser?",
        ('Detroit Pistons', 'Los Angeles Lakers',
         'Golden State Warriors', 'Philadelphia 76ers',
         'Chicago Bulls', 'Boston Celtics', 'Cleveland Cavaliers',
         'Atlanta Hawks', 'Portland Trail Blazers',
         'Sacramento Kings', 'Charlotte Hornets', 
        'Miami Heat',  'Orlando Magic', 'Minnesota Timberwolves', 'Toronto Raptors', 
        'Oklahoma City Thunder', 'New York Knicks', 'Denver Nuggets', 'Milwaukee Bucks', 'Phoenix Suns',
           'San Antonio Spurs', 'Indiana Pacers', 'Utah Jazz', 'Dallas Mavericks',
        'Los Angeles Clippers' , 'Washington Wizards', 'Memphis Grizzlies', 
        'Oklahoma City Thunder','Brooklyn Nets', 'New Orleans Pelicans',
     ),
    )

    # Filter only home games for selected team
    df_team_home = df_game_nba[df_game_nba['team_name_home'] == equipe_selectionnee].copy()

    # Convert game_date to datetime
    df_team_home['game_date'] = pd.to_datetime(df_team_home['game_date'])

    # Extract year
    df_team_home['year'] = df_team_home['game_date'].dt.year

    # Compute win flag
    df_team_home['win'] = df_team_home['wl_home'] == 'W'

    # Group by year and calculate win percentage
    win_stats = df_team_home.groupby('year')['win'].mean().reset_index()
    win_stats['win_percent'] = win_stats['win'] * 100

    # Plot
    fig_win_pct = px.line(
        win_stats,
        x='year',
        y='win_percent',
        title=f"% de victoires à domicile par saison : {equipe_selectionnee}",
        markers=True,
        labels={'year': 'Année', 'win_percent': 'Pourcentage de victoires (%)'}
    )

    # Update layout with y-axis range and add 50% reference line
    fig_win_pct.update_layout(
        yaxis=dict(range=[0, 110]),
        shapes=[
            dict(
                type='line',
                x0=win_stats['year'].min(),
                x1=win_stats['year'].max(),
                y0=50,
                y1=50,
                line=dict(color='gray', width=2, dash='dash')
            )
        ]
    )

    st.plotly_chart(fig_win_pct, use_container_width=True)


# with tabs[3]:
#     st.header("Comparaison de la rentabilité et du volume des tirs 2 pts vs 3 pts")
#     fig = create_efficiency_graph(df_game_nba)
#     st.plotly_chart(fig, use_container_width=True)

