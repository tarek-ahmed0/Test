# Used Libraries:
import pandas as pd
import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64

# Data Ingestion:
main = pd.read_csv(r"tourist_preferences_recommendations.csv", delimiter=';')

# Setup Our Application 
st.title(""" :blue[Travel Vision] Agent 🤖 """)
st.markdown("""
    **Travel Vision** :gray[delivers tailored travel recommendations, expertly curating destinations, activities, and accommodations to] 
    :violet[match your unique preferences and ensure a seamless travel experience.]
""")
st.divider()
st.subheader("User Preferences")

# User Preferences
nationality_selected = st.selectbox(":gray[What's Your Nationality?]", main['Nationality'].unique())
filtered_df_nat = main[main['Nationality'] == nationality_selected]

col1, col2 = st.columns(2)
with col1:
    environment_selected = st.selectbox(":gray[What Environment Type Do You Prefer?]", filtered_df_nat['Preferred Environment'].unique())
    filtered_df_env = filtered_df_nat[filtered_df_nat['Preferred Environment'] == environment_selected]

with col2:
    if not filtered_df_env.empty:
        min_val = filtered_df_env['Interest Level in Activities'].min()
        max_val = filtered_df_env['Interest Level in Activities'].max()

        activities_num = st.number_input(
            ":gray[How Many Activities Are You Interested In?]", 
            min_value=min_val, 
            max_value=max_val
        )
    else:
        st.warning("No data available for the selected environment.")

filtered_df_act = filtered_df_env[filtered_df_env['Interest Level in Activities'] == activities_num]    

col1, col2 = st.columns(2)
with col1:
    activity_type = st.selectbox(":gray[What Activity Type Do You Prefer?]", filtered_df_act['Preferred Activity Type'].unique())
    filtered_df_act_type = filtered_df_act[filtered_df_act['Preferred Activity Type'] == activity_type]

with col2:
    food_type = st.selectbox(":gray[What Kind Of Food Do You Like To Eat?]", filtered_df_act_type['Favorite Type of Food'].unique())
    filtered_df_food = filtered_df_act_type[filtered_df_act_type['Favorite Type of Food'] == food_type]    

col1, col2 = st.columns(2)
with col1:
    travel_type = st.radio(":gray[What Travel Type Do You Want?]", filtered_df_food['Travel Companion'].unique())
    filtered_df_travel_type = filtered_df_food[filtered_df_food['Travel Companion'] == travel_type]

with col2:
    budget = st.radio(":gray[Select Budget Range]", filtered_df_travel_type['Budget Range'].unique())
    filtered_df_budget = filtered_df_travel_type[filtered_df_travel_type['Budget Range'] == budget]

st.divider()
st.subheader(":orange[Recommendations]🧩")

# Recommendations
recomm_df = main[(main['Nationality'] == nationality_selected) & 
                 (main['Preferred Environment'] == environment_selected) & 
                 (main['Interest Level in Activities'] == activities_num) & 
                 (main['Preferred Activity Type'] == activity_type) & 
                 (main['Favorite Type of Food'] == food_type) & 
                 (main['Travel Companion'] == travel_type) & 
                 (main['Budget Range'] == budget)]

# Display recommendations in a compact expandable container
with st.expander(":green[Travel Vision Suggestions 🎯]", expanded=True):
    if not recomm_df.empty:
        recommended_hotel = recomm_df.sample(n=1)['Hotel Recommendations'].values[0]
        recommended_rest = recomm_df.sample(n=1)['Restaurant Recommendations'].values[0]
        recommended_act = recomm_df.sample(n=1)['Activity Recommendations'].values[0]
        st.write(
            f"Hello! Welcome to Egypt. Firstly, we suggest going to :violet[**{recommended_hotel}**], "
            f"which is suitable for **{travel_type}** journeys. "
            f"We all know that **{food_type}** food is very delicious, so we suggest having a meal at :violet[**{recommended_rest}**]. "
            f"To avoid boredom, what’s your opinion about going for :violet[**{recommended_act}**]? "
            f"I know you like **{activity_type}**."
        )
        recommende_speech = (
            f"Hello! Welcome to Egypt. Firstly, we suggest going to :violet[**{recommended_hotel}**], "
            f"which is suitable for **{travel_type}** journeys. "
            f"We all know that **{food_type}** food is very delicious, so we suggest having a meal at :violet[**{recommended_rest}**]. "
            f"To avoid boredom, what’s your opinion about going for :violet[**{recommended_act}**]? "
            f"I know you like **{activity_type}**."
        )

        # Text-to-Speech
        def play_tts(text):
            tts = gTTS(text, lang='en')
            audio_data = BytesIO()
            tts.write_to_fp(audio_data)
            audio_data.seek(0)
            return audio_data

        tts_audio = play_tts(recommende_speech)
        audio_base64 = base64.b64encode(tts_audio.read()).decode()
        audio_url = f"data:audio/mp3;base64,{audio_base64}"

        # Embeded
        st.markdown(f"""
            <audio controls style="width: 100%; height: 30px; border: none;">
                <source src="{audio_url}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        """, unsafe_allow_html=True)
    else:
        st.warning("No recommendations available for the selected criteria.")
