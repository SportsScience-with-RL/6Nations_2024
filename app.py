import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
import time

##############################
########## SETTINGS ##########
##############################

st.set_page_config(layout='wide', page_icon='Logo_Six_Nations.png', page_title='Application - Séquences de jeu 6 Nations 2024')

##################################
######### AUTHENTICATION #########
##################################

# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days']
# )

# name, authentication_status, username = authenticator.login('Login', 'main')

# if authentication_status:

####################################
########## SESSION STATES ##########
####################################

if 'data_game' not in st.session_state:
    st.session_state['data_game'] = pd.DataFrame()
if 'last_play' not in st.session_state:
    st.session_state['last_play'] = pd.DataFrame()

if 'start_time' not in st.session_state:
    st.session_state['start_time'] = 0
if 'end_time' not in st.session_state:
    st.session_state['end_time'] = 0

if 'start_type' not in st.session_state:
    st.session_state['start_type'] = ''
if 'last_action' not in st.session_state:
    st.session_state['last_action'] = ''

if 'start_zone' not in st.session_state:
    st.session_state['start_zone'] = ''
if 'end_zone' not in st.session_state:
    st.session_state['end_zone'] = ''
if 'start_zone_value' not in st.session_state:
    st.session_state['start_zone_value'] = 0
if 'end_zone_value' not in st.session_state:
    st.session_state['end_zone_value'] = 0

if 'stat_count' not in st.session_state:
    st.session_state['stat_count'] = {'Passe': 0,
                                      'Ruck': 0,
                                      'Ruck +': 0,
                                      'Offload': 0,
                                      'Offload +': 0,
                                      'Jeu au pied': 0,
                                      'Maul': 0,
                                      'Relâché': 0,
                                      'Départ ruck': 0,
                                      'Dégagement': 0}

if 'score_team1' not in st.session_state:
    st.session_state['score_team1'] = 0
if 'score_team2' not in st.session_state:
    st.session_state['score_team2'] = 0

if 'correction_state' not in st.session_state:
    st.session_state['correction_state'] = False
    
###############################
########## FUNCTIONS ##########
###############################

def counter(action, type_):
    if type_ == '+':
        st.session_state['stat_count'][action] += 1
    elif type_ == '-':
        st.session_state['stat_count'][action] -= 1
    st.session_state['last_action'] = action

def start_zone(zone_, zone_value, time_):
    st.session_state['start_zone'] = zone_
    st.session_state['start_zone_value'] = zone_value
    if st.session_state['start_time'] == 0:
        st.session_state['start_time'] = time_

def start_seq(type_, time_):
    if st.session_state['start_time'] == 0:
        st.session_state['start_time'] = time_
    st.session_state['start_type'] = type_

def end_zone(zone_, zone_value, time_):
    st.session_state['end_time'] = time_
    st.session_state['end_zone'] = zone_
    st.session_state['end_zone_value'] = zone_value

def previous_seq():
    st.session_state['last_play'] = st.session_state['data_game'].iloc[-1].to_frame().T

    st.session_state['start_zone'] = st.session_state['last_play']['Start_zone'].values[0]
    st.session_state['start_type'] = st.session_state['last_play']['Start_type'].values[0]
    st.session_state['end_zone'] = st.session_state['last_play']['End_zone'].values[0]
    st.session_state['last_action'] = st.session_state['last_play']['Dernière action'].values[0]
    st.session_state['start_zone_value'] = st.session_state['last_play']['Start_zone_value'].values[0]
    st.session_state['end_zone_value'] = st.session_state['last_play']['End_zone_value'].values[0]
    st.session_state['stat_count']['Passe'] = st.session_state['last_play']['Passe'].values[0]
    st.session_state['stat_count']['Ruck'] = st.session_state['last_play']['Ruck'].values[0]
    st.session_state['stat_count']['Ruck +'] = st.session_state['last_play']['Ruck +'].values[0]
    st.session_state['stat_count']['Offload'] = st.session_state['last_play']['Offload'].values[0]
    st.session_state['stat_count']['Offload +'] = st.session_state['last_play']['Offload +'].values[0]
    st.session_state['stat_count']['Jeu au pied'] = st.session_state['last_play']['Jeu au pied'].values[0]
    st.session_state['stat_count']['Maul'] = st.session_state['last_play']['Maul'].values[0]
    st.session_state['stat_count']['Relâché'] = st.session_state['last_play']['Relâché'].values[0]
    st.session_state['stat_count']['Départ ruck'] = st.session_state['last_play']['Départ ruck'].values[0]
    st.session_state['stat_count']['Dégagement'] = st.session_state['last_play']['Dégagement'].values[0]
    st.session_state['correction_state'] = True

def sequence_stat(type_, time_):
    if st.session_state['correction_state']:
        st.session_state['last_play']['Start_zone'] = st.session_state['start_zone']
        st.session_state['last_play']['Start_type'] = st.session_state['start_type']
        st.session_state['last_play']['Start_zone_value'] = st.session_state['start_zone_value']
        st.session_state['last_play']['End_zone'] = st.session_state['end_zone']
        st.session_state['last_play']['End_zone_value'] = st.session_state['end_zone_value']
        st.session_state['last_play']['Passe'] = st.session_state['stat_count']['Passe']
        st.session_state['last_play']['Ruck'] = st.session_state['stat_count']['Ruck']
        st.session_state['last_play']['Ruck +'] = st.session_state['stat_count']['Ruck +']
        st.session_state['last_play']['Offload'] = st.session_state['stat_count']['Offload']
        st.session_state['last_play']['Offload +'] = st.session_state['stat_count']['Offload +']
        st.session_state['last_play']['Jeu au pied'] = st.session_state['stat_count']['Jeu au pied']
        st.session_state['last_play']['Maul'] = st.session_state['stat_count']['Maul']
        st.session_state['last_play']['Relâché'] = st.session_state['stat_count']['Relâché']
        st.session_state['last_play']['Départ ruck'] = st.session_state['stat_count']['Départ ruck']
        st.session_state['last_play']['Dégagement'] = st.session_state['stat_count']['Dégagement']
        st.session_state['last_play']['Résultat'] = type_
        st.session_state['correction_state'] = False

        st.session_state['data_game'] = st.session_state['data_game'][:-1]
        st.session_state['data_game'] = pd.concat([st.session_state['data_game'],
                                                    st.session_state['last_play']], ignore_index=True)

    elif not st.session_state['correction_state']:
        if type_ == 'Essai':
            st.session_state['end_zone'] = 'En-but'
            st.session_state['end_zone_value'] = 13
        
        if st.session_state['end_time'] == 0:
            st.session_state['end_time'] = time_

        data_seq = {'Match': team_1+' - '+team_2,
                    'Chrono': st.session_state['stopwatch'],
                    'Score_team1': st.session_state['score_team1'],
                    'Score_team2': st.session_state['score_team2'],
                    'Possession': st.session_state['possession'],
                    'Start_type': st.session_state['start_type'],
                    'Start_time': st.session_state['start_time'],
                    'End_time': st.session_state['end_time'],
                    'Start_zone': st.session_state['start_zone'],
                    'Start_zone_value': st.session_state['start_zone_value'],
                    'End_zone': st.session_state['end_zone'],
                    'End_zone_value': st.session_state['end_zone_value'],
                    'Résultat': type_,
                    'Dernière action': st.session_state['last_action']
                    }
        
        data_seq.update(st.session_state['stat_count'])

        st.session_state['data_game'] = pd.concat([st.session_state['data_game'],
                                                    pd.DataFrame([data_seq])], ignore_index=True)
    
    st.session_state['start_time'] = 0
    st.session_state['end_time'] = 0
    st.session_state['start_type'] = ''
    st.session_state['start_zone'] = ''
    st.session_state['end_zone'] = ''
    st.session_state['start_zone_value'] = 0
    st.session_state['end_zone_value'] = 0
    st.session_state['last_action'] = ''
    st.session_state['stat_count'] = dict.fromkeys(st.session_state['stat_count'], 0)

def score_game(team_, type_):
    if (team_ == 'team1') and (type_ == '+'):
        st.session_state['score_team1'] += 1
    elif (team_ == 'team1') and (type_ == '-'):
        st.session_state['score_team1'] -= 1
    elif (team_ == 'team2') and (type_ == '+'):
        st.session_state['score_team2'] += 1
    elif (team_ == 'team2') and (type_ == '-'):
        st.session_state['score_team2'] -= 1
    
def end_game():
    st.session_state['score_team1'] = 0
    st.session_state['score_team2'] = 0
    st.session_state['stopwatch'] = "0'-20'"
    st.session_state['data_game'] = pd.DataFrame()
    st.session_state['last_play'] = pd.DataFrame()
    st.session_state['stat_count'] = dict.fromkeys(st.session_state['stat_count'], 0)

################################
########## GAME INFOS ##########
################################

teams_list = ['England', 'France', 'Ireland', 'Italia', 'Scotland', 'Wales']

teams_img = {team: f'img/{team}.png' for team in teams_list}

c1, c2, c3, c4, c5 = st.columns([.3, .15, .15, .1, .3])
with c1:
    team_1 = st.selectbox('', options=teams_list, key='team_1')
    c11, c12, _, _ = st.columns(4)
    c11.button('Pts +', on_click=score_game, args=['team1', '+'])
    c12.button('Pts -', on_click=score_game, args=['team1', '-'])
with c2:
    ''
    ''
    ''
    ''
    st.image(teams_img[st.session_state['team_1']])

with c3:
    ''
    ''
    ''
    ''
    st.title(f"{st.session_state['score_team1']} - {st.session_state['score_team2']}")

with c5:
    team_2 = st.selectbox(' ', options=teams_list, key='team_2')
    _, _, c51, c52 = st.columns(4)
    c51.button('Pts + ', on_click=score_game, args=['team2', '+'])
    c52.button('Pts - ', on_click=score_game, args=['team2', '-'])
with c4:
    ''
    ''
    ''
    ''
    st.image(teams_img[st.session_state['team_2']])

c1, _, _ = st.columns([.3, .5, .2])
c1.radio('Quelle équipe joue de gauche à droite en 1ère mi-temps ?', options=[team_1, team_2], horizontal=True, key='first_half')

st.radio(':stopwatch: Chrono', options=["0'-20'", "20'-40'", "40'-60'", "60'-80'"], horizontal=True, key='stopwatch')
with st.expander('Procédure de saisie'):
    st.write('(1) - Appuyer soit sur le bouton de zone de départ (vert au-dessus du terrain) soit du type de départ de séquence.')
    st.write('(2) - Appuyer sur le bouton de zone de départ ou du type de départ de la séquence (selon celui appuyé en (1)).')
    st.write("(3) - Appuyer sur les boutons d'actions correspondant à celles de la séquence.")
    st.write('(4) - Appuyer sur le bouton de zone de fin de séquence (jaune au-dessus du terrain).')
    st.write('(5) - Appuyer sur le bouton correpondant au résultat de la séquence.')
'---'

##################################
########## STATISTIQUES ##########
##################################

c1, c2, c3 = st.columns([.18, .7, .12])
c1.radio(':rugby_football: Possession', options=[team_1, team_2], horizontal=True, key='possession')
with c2:
    dict_to_show = {'Zone départ': st.session_state['start_zone'],
                    'Type départ': st.session_state['start_type'],
                    'Zone de fin': st.session_state['end_zone']}
    dict_to_show.update(st.session_state['stat_count'])
    st.dataframe(pd.DataFrame([dict_to_show]), hide_index=True)
c3.button("Séquence précédente", on_click=previous_seq)
''

############################ Zones départ et fin ############################
zones_ = ['En-but1', '22m1', '22m2', '40m1', '40m2', '10m1', '10m2', '40m3', '40m4', '22m3', '22m4', 'En-but2']

if (st.session_state['stopwatch'] in ["0'-20'", "20'-40'"]) and (st.session_state['first_half'] == st.session_state['possession']):
    zone_values = list(range(1, 13))
    zone_labels = zones_
elif (st.session_state['stopwatch'] in ["0'-20'", "20'-40'"]) and (st.session_state['first_half'] != st.session_state['possession']):
    zone_values = list(reversed(range(1, 13)))
    zone_labels = list(reversed(zones_))
elif (st.session_state['stopwatch'] in ["40'-60'", "60'-80'"]) and (st.session_state['first_half'] == st.session_state['possession']):
    zone_values = list(reversed(range(1, 13)))
    zone_labels = list(reversed(zones_))
elif (st.session_state['stopwatch'] in ["40'-60'", "60'-80'"]) and (st.session_state['first_half'] != st.session_state['possession']):
    zone_values = list(range(1, 13))
    zone_labels = zones_

c_zone_d = st.columns([.15] + [.7/12]*12 + [.15])
with c_zone_d[0]:
    _, c1 = st.columns([.4, .6])
    with c1:
        st.markdown(':gray[**ZONE DEPART**]')
        st.markdown(':gray[**ZONE FIN**]')
with c_zone_d[1]:
    st.button('Goal', on_click=start_zone, args=[zone_labels[0], zone_values[0], time.time()])
    st.button('Goal ', on_click=end_zone, args=[zone_labels[0], zone_values[0], time.time()])
with c_zone_d[2]:
    with stylable_container(
        key='button_d22m1', css_styles="""button {
            background-color: #90e4a3; color: black;}
            """): st.button('22m', on_click=start_zone, args=[zone_labels[1], zone_values[1], time.time()])
    with stylable_container(
        key='button_f22m1', css_styles="""button {
            background-color: #fea; color: black;}
            """): st.button(' 22m', on_click=end_zone, args=[zone_labels[1], zone_values[1], time.time()])
with c_zone_d[3]:
    with stylable_container(
        key='button_d22m2', css_styles="""
        button {background-color: #90e4a3; color: black;}
        """): st.button('22m ', on_click=start_zone, args=[zone_labels[2], zone_values[2], time.time()])
    with stylable_container(
        key='button_f22m2', css_styles="""
        button {background-color: #fea; color: black;}
        """): st.button(' 22m ', on_click=end_zone, args=[zone_labels[2], zone_values[2], time.time()])
with c_zone_d[4]:
    with stylable_container(
        key='button_d40m1', css_styles="""
        button {background-color: #4bd46a; color: black;}
        """): st.button('40m', on_click=start_zone, args=[zone_labels[3], zone_values[3], time.time()])
    with stylable_container(
        key='button_f40m1', css_styles="""
        button {background-color: #fd5; color: black;}
        """): st.button(' 40m', on_click=end_zone, args=[zone_labels[3], zone_values[3], time.time()])
with c_zone_d[5]:
    with stylable_container(
        key='button_d40m2', css_styles="""
        button {background-color: #4bd46a; color: black;}
        """): st.button('40m ', on_click=start_zone, args=[zone_labels[4], zone_values[4], time.time()])
    with stylable_container(
        key='button_f40m2', css_styles="""
        button {background-color: #fd5; color: black;}
        """): st.button(' 40m ', on_click=end_zone, args=[zone_labels[4], zone_values[4], time.time()])
with c_zone_d[6]:
    with stylable_container(
        key='button_d10m1', css_styles="""
        button {background-color: #175e27; color: black;}
        """): st.button('10m', on_click=start_zone, args=[zone_labels[5], zone_values[5], time.time()])
    with stylable_container(
        key='button_f10m1', css_styles="""
        button {background-color: #a80; color: black;}
        """): st.button(' 10m', on_click=end_zone, args=[zone_labels[5], zone_values[5], time.time()])
with c_zone_d[7]:
    with stylable_container(
        key='button_d10m2', css_styles="""
        button {background-color: #175e27; color: black;}
        """): st.button('10m ', on_click=start_zone, args=[zone_labels[6], zone_values[6], time.time()])
    with stylable_container(
        key='button_f10m2', css_styles="""
        button {background-color: #a80; color: black;}
        """): st.button(' 10m ', on_click=end_zone, args=[zone_labels[6], zone_values[6], time.time()])
with c_zone_d[8]:
    with stylable_container(
        key='button_d40m3', css_styles="""
        button {background-color: #4bd46a; color: black;}
        """): st.button('40m  ', on_click=start_zone, args=[zone_labels[7], zone_values[7], time.time()])
    with stylable_container(
        key='button_f40m3', css_styles="""
        button {background-color: #fd5; color: black;}
        """): st.button(' 40m  ', on_click=end_zone, args=[zone_labels[7], zone_values[7], time.time()])
with c_zone_d[9]:
    with stylable_container(
        key='button_d40m4', css_styles="""
        button {background-color: #4bd46a; color: black;}
        """): st.button('40m   ', on_click=start_zone, args=[zone_labels[8], zone_values[8], time.time()])
    with stylable_container(
        key='button_f40m4', css_styles="""
        button {background-color: #fd5; color: black;}
        """): st.button(' 40m   ', on_click=end_zone, args=[zone_labels[8], zone_values[8], time.time()])
with c_zone_d[10]:
    with stylable_container(
        key='button_d22m3', css_styles="""
        button {background-color: #90e4a3; color: black;}
        """): st.button('22m   ', on_click=start_zone, args=[zone_labels[9], zone_values[9], time.time()])
    with stylable_container(
        key='button_f22m3', css_styles="""
        button {background-color: #fea; color: black;}
        """): st.button(' 22m   ', on_click=end_zone, args=[zone_labels[9], zone_values[9], time.time()])
with c_zone_d[11]:
    with stylable_container(
        key='button_d22m4', css_styles="""
        button {background-color: #90e4a3; color: black;}
        """): st.button('22m    ', on_click=start_zone, args=[zone_labels[10], zone_values[10], time.time()])
    with stylable_container(
        key='button_f22m4', css_styles="""
        button {background-color: #fea; color: black;}
        """): st.button(' 22m    ', on_click=end_zone, args=[zone_labels[10], zone_values[10], time.time()])
with c_zone_d[12]:
    st.button(' Goal', on_click=start_zone, args=[zone_labels[11], zone_values[11], time.time()])
    st.button(' Goal ', on_click=end_zone, args=[zone_labels[11], zone_values[11], time.time()])

'---'

c1, _, c2, _, c3 = st.columns([.2, .025, .55, .025, .2])
############################ Départ ############################
with c1:
    st.markdown(':gray[**SEQUENCE**]')
    st.markdown('**Départ**')
    c11, c12 = st.columns(2)
    with c11:
        with stylable_container(
            key='button_dtouche', css_styles="""button {
                background-color: #4267dd; color: white;}
                """): st.button('Touche', on_click=start_seq, args=['Touche', time.time()])
        with stylable_container(
            key='button_dtouchep', css_styles="""button {
                background-color: #4267dd; color: white;}
                """): st.button('Touche +', on_click=start_seq, args=['Touche +', time.time()])
        with stylable_container(
            key='button_dmelee', css_styles="""button {
                background-color: #4267dd; color: white;}
                """): st.button('Mêlée', on_click=start_seq, args=['Mêlée', time.time()])
        with stylable_container(
            key='button_dmeleep', css_styles="""button {
                background-color: #4267dd; color: white;}
                """): st.button('Mêlée +', on_click=start_seq, args=['Mêlée +', time.time()])
    with c12:
        with stylable_container(
            key='button_dcdp', css_styles="""button {
                background-color: #4267dd; color: white;}
                """): st.button('Coup de pied', on_click=start_seq, args=['Coup de pied', time.time()])
        with stylable_container(
        key='button_dcontre', css_styles="""button {
            background-color: #4267dd; color: white;}
            """): st.button('Turnover', on_click=start_seq, args=['Turnover', time.time()]) 
        with stylable_container(
            key='button_drapide', css_styles="""button {
                background-color: #4267dd; color: white;}
                """): st.button('Jeux rapide', on_click=start_seq, args=['Jeux rapide', time.time()])
    
############################ Statistiques ############################
with c2:
    st.markdown(':gray[**SEQUENCE**]')
    st.markdown('**Actions**')
    c_seq_act = st.columns(5)
    with c_seq_act[0]:
        with stylable_container(
            key='button_passe', css_styles="""button {
                background-color: #dccb9b; color: #303207;}
                """): st.button('Passe', on_click=counter, args=['Passe', '+'])
        st.button('-1 Passe', on_click=counter, args=['Passe', '-'])
        with stylable_container(
            key='button_pied', css_styles="""button {
                background-color: #dccb9b; color: #303207;}
                """): st.button('Jeu au pied', on_click=counter, args=['Jeu au pied', '+'])
        st.button('-1 Jeu au pied', on_click=counter, args=['Jeu au pied', '-'])
    with c_seq_act[1]:
        with stylable_container(
            key='button_ruckp', css_styles="""button {
                background-color: #dccb9b; color: #303207;}
                """): st.button('Ruck +', on_click=counter, args=['Ruck +', '+'])
        st.button('-1 Ruck +', on_click=counter, args=['Ruck +', '-'])
        with stylable_container(
            key='button_ruck', css_styles="""button {
                background-color: #dccb9b; color: #303207;}
                """): st.button('Ruck', on_click=counter, args=['Ruck', '+'])
        st.button('-1 Ruck', on_click=counter, args=['Ruck', '-'])
    with c_seq_act[2]:
        with stylable_container(
            key='button_maul', css_styles="""button {
                background-color: #dccb9b; color: #303207;}
                """): st.button('Maul', on_click=counter, args=['Maul', '+'])
        st.button('-1 Maul', on_click=counter, args=['Maul', '-'])
        with stylable_container(
            key='button_relache', css_styles="""button {
                background-color: #dccb9b; color: #303207;}
                """): st.button('Relâché', on_click=counter, args=['Relâché', '+'])
        st.button('-1 Relâché', on_click=counter, args=['Relâché', '-'])
    with c_seq_act[3]:
        with stylable_container(
            key='button_offload', css_styles="""button {
                background-color: #dccb9b; color: #303207;}
                """): st.button('Offload', on_click=counter, args=['Offload', '+'])
        st.button('-1 Offload', on_click=counter, args=['Offload', '-'])
        with stylable_container(
            key='button_offloadp', css_styles="""button {
                background-color: #dccb9b; color: #303207;}
                """): st.button('Offload +', on_click=counter, args=['Offload +', '+'])
        st.button('-1 Offload +', on_click=counter, args=['Offload +', '-'])
    with c_seq_act[4]:
        with stylable_container(
            key='button_ras', css_styles="""button {
                background-color: #dccb9b; color: #303207;}
                """): st.button('Départ ruck', on_click=counter, args=['Départ ruck', '+'])
        st.button('-1 Départ ruck', on_click=counter, args=['Départ ruck', '-'])
        with stylable_container(
            key='button_degagement', css_styles="""button {
                background-color: #dccb9b; color: #303207;}
                """): st.button('Dégagement', on_click=counter, args=['Dégagement', '+'])
        st.button('-1 Dégagement', on_click=counter, args=['Dégagement', '-'])

with c3:
    st.markdown(':gray[**SEQUENCE**]')
    st.markdown('**Résultat**')
    c11, c12 = st.columns(2)
    with c11:    
        with stylable_container(
            key='button_fautep', css_styles="""button {
                background-color: #8fff8f; color: green;}
                """): st.button('Faute +', on_click=sequence_stat, args=['Faute +', time.time()])
        with stylable_container(
            key='button_fauten', css_styles="""button {
                background-color: #f77; color: #661200;}
                """): st.button('Faute -', on_click=sequence_stat, args=['Faute -', time.time()])
        with stylable_container(
            key='button_touche', css_styles="""button {
                background-color: #c3cdff; color: blue;}
                """): st.button('Touche ', on_click=sequence_stat, args=['Touche', time.time()])
        with stylable_container(
            key='button_essai', css_styles="""button {
                background-color: #8fff8f; color: green;}
                """): st.button('Essai', on_click=sequence_stat, args=['Essai', time.time()])
    with c12:
        with stylable_container(
            key='button_perte', css_styles="""button {
                background-color: #f77; color: #661200;}
                """): st.button('Perte', on_click=sequence_stat, args=['Perte', time.time()])
        with stylable_container(
            key='button_dropplus', css_styles="""button {
                background-color: #8fff8f; color: green;}
                """): st.button('Drop +', on_click=sequence_stat, args=['Drop +', time.time()])
        with stylable_container(
            key='button_dropmoins', css_styles="""button {
                background-color: #f77; color: #661200;}
                """): st.button('Drop -', on_click=sequence_stat, args=['Drop -', time.time()])
        with stylable_container(
            key='button_supp', css_styles="""button {
                background-color: white; color: #ff3f11; border: 3px solid #ff3f11;}
                """): st.button('SUPP.', on_click=sequence_stat, args=['Supprimer', time.time()])

'---'
data_download = st.session_state['data_game'].to_csv(index=False).encode('latin1')
_, c1, c2 = st.columns([.7, .15, .15])
with c1:
    with stylable_container(
        key='endgame_button', css_styles="""button {
            background-color: red; color: white; border-radius: 20px;}
            """,): st.button(':white_large_square: Fin de match', on_click=end_game)
with c2:
    with stylable_container(
        key='download_button', css_styles="""button {
            background-color: #36c26d; color: white;}
            """,): st.download_button(label=':inbox_tray: Télécharger données',
                                        data=data_download,
                                        file_name=f"Match_{st.session_state['team_1']}_{st.session_state['team_2']}.csv")

# elif authentication_status == False:
#     st.error('Username/password incorrect(s)')
# elif authentication_status == None:
#     st.warning('Saisir username et password')