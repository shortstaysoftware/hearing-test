import streamlit as st
import pandas as pd
import plotly.graph_objects as pl
import plotly.express as px

# Set Streamlit page config
st.set_page_config(page_title="Hearing Test Results", page_icon="🦻", initial_sidebar_state="expanded")
st.subheader("🦻 " + "Hearing Test Results")

# Get the state of the current session
state = st.session_state

# Initialize the variables for each frequency

frequencies = [500, 1000, 2000, 3000, 4000, 6000, 8000]
for freq in frequencies:
    for ear in ['l', 'r']:
        key = f"{ear}{freq}"
        if key not in state:
            state[key] = -10

with st.sidebar:

    st.subheader("Patient Information")

    # Input for age
    age = st.number_input("Age", min_value=18, max_value=65, value=45, step=1)

    # Radio to select Male/Female
    gender = st.radio(
    "Gender",
    ["Female", "Male"],
    )
    
hearing_loss_criteria = {18: {'Male': (51, 95), 'Female': (46, 78)}, 19: {'Male': (51, 95), 'Female': (46, 78)}, 20: {'Male': (51, 95), 'Female': (46, 78)}, 21: {'Male': (51, 95), 'Female': (46, 78)}, 22: {'Male': (54, 98), 'Female': (48, 80)}, 23: {'Male': (56, 101), 'Female': (49, 82)}, 24: {'Male': (59, 104), 'Female': (50, 84)}, 25: {'Male': (62, 107), 'Female': (52, 87)}, 26: {'Male': (64, 110), 'Female': (54, 89)}, 27: {'Male': (67, 113), 'Female': (55, 91)}, 28: {'Male': (70, 117), 'Female': (57, 94)}, 29: {'Male': (73, 121), 'Female': (58, 97)}, 30: {'Male': (76, 124), 'Female': (60, 99)}, 31: {'Male': (79, 128), 'Female': (61, 102)}, 32: {'Male': (82, 132), 'Female': (63, 105)}, 33: {'Male': (86, 136), 'Female': (65, 108)}, 34: {'Male': (89, 141), 'Female': (66, 111)}, 35: {'Male': (93, 145), 'Female': (68, 113)}, 36: {'Male': (96, 150), 'Female': (69, 116)}, 37: {'Male': (100, 154), 'Female': (71, 119)}, 38: {'Male': (104, 160), 'Female': (73, 122)}, 39: {'Male': (108, 166), 'Female': (75, 125)}, 40: {'Male': (113, 171), 'Female': (76, 128)}, 41: {'Male': (117, 177), 'Female': (78, 131)}, 42: {'Male': (121, 183), 'Female': (80, 134)}, 43: {'Male': (125, 189), 'Female': (83, 138)}, 44: {'Male': (129, 194), 'Female': (85, 142)}, 45: {'Male': (134, 200), 'Female': (88, 145)}, 46: {'Male': (138, 205), 'Female': (90, 149)}, 47: {'Male': (142, 211), 'Female': (93, 153)}, 48: {'Male': (147, 217), 'Female': (97, 158)}, 49: {'Male': (151, 223), 'Female': (100, 162)}, 50: {'Male': (156, 228), 'Female': (104, 167)}, 51: {'Male': (160, 234), 'Female': (107, 171)}, 52: {'Male': (165, 240), 'Female': (111, 176)}, 53: {'Male': (170, 246), 'Female': (115, 182)}, 54: {'Male': (175, 252), 'Female': (119, 187)}, 55: {'Male': (180, 257), 'Female': (123, 193)}, 56: {'Male': (185, 263), 'Female': (127, 198)}, 57: {'Male': (190, 269), 'Female': (131, 204)}, 58: {'Male': (195, 274), 'Female': (136, 210)}, 59: {'Male': (201, 280), 'Female': (141, 216)}, 60: {'Male': (206, 285), 'Female': (147, 223)}, 61: {'Male': (212, 291), 'Female': (152, 229)}, 62: {'Male': (217, 296), 'Female': (157, 235)}, 63: {'Male': (223, 301), 'Female': (163, 242)}, 64: {'Male': (229, 306), 'Female': (169, 248)}, 65: {'Male': (235, 311), 'Female': (175, 255)}}

# Function to determine hearing loss level based on hearing level sum, age, and gender
def evaluate_hearing_loss(age, gender, hearing_level_sum):
    result = {
        'Result': None,
        'Mild': None,
        'Significant': None,
        'Label': None,
        'Color': None,
    }
    
    # Check if the age is in the dictionary
    if age in hearing_loss_criteria:
        gender_thresholds = hearing_loss_criteria[age][gender]
        result['Mild'] = gender_thresholds[0]
        result['Significant'] = gender_thresholds[1]

        # Compare hearing level sum against the mild and significant thresholds
        if hearing_level_sum < gender_thresholds[0]:
            result['Result'] = 'None'
            result['Label'] = 'No Hearing Loss'
            result['Color'] = '#309143'
        elif gender_thresholds[0] <= hearing_level_sum < gender_thresholds[1]:
            result['Result'] = 'Mild'
            result['Label'] = 'Mild Hearing Loss'
            result['Color'] = '#e39802'
        else:
            result['Result'] = 'Significant'
            result['Label'] = 'Significant Hearing Loss'
            result['Color'] = '#b60a1c'
        
        return result

    result['Result'] = 'Age out of range'
    return result

# Calculate the hearing level sum
l_sum = state.l1000 + state.l2000 + state.l3000 + state.l4000 + state.l6000
r_sum = state.r1000 + state.r2000 + state.r3000 + state.r4000 + state.r6000

# Evaluate the hearing loss level
evaluation_left = evaluate_hearing_loss(age, gender, l_sum)
evaluation_right = evaluate_hearing_loss(age, gender, r_sum)

# Create 2 columns for the evaluation
left, right = st.columns(2)

# Column for left ear
with left:
    barcolor = evaluation_left["Color"]
    fig = pl.Figure(pl.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = l_sum,
        mode = "gauge+number",
        gauge = {'axis': {'range': [None, 350],
                      'tickvals': [evaluation_left["Mild"], evaluation_left["Significant"]],
                      'ticktext': [evaluation_left["Mild"], evaluation_left["Significant"]]},
                'bar': {'color': barcolor},
                'steps' : [
                    {'range': [0, evaluation_left["Mild"]], 'color': "#8ace7e"},
                    {'range': [evaluation_left["Mild"], evaluation_left["Significant"]], 'color': "#ffda66"},
                    {'range': [evaluation_left["Significant"], 350], 'color': "#ff684c"}],
                'threshold' : {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': l_sum}}))
    fig.update_layout(
        width=340,  # Set the width of the figure
        height=260,  # Set the height of the figure
        margin=dict(
            l=10,  # left margin
            r=10,  # right margin
            b=10,  # bottom margin
            t=20,  # top margin
            pad=20  # padding
        ),
        title_text="Left Ear: "+evaluation_left["Label"],  # Sets title text
        title_x=0.5,               # Centers the title horizontally
        title_y=0.95,              # Set the title in the top part of the plot
        title_xanchor='center',    # Ensures the title's x-position is centered
        title_yanchor='top',       # Ensures the title's y-position is at the top
        title_font=dict(
            family="Open Sans, verdana, arial, sans-serif",
            size=18,
            color="gray"
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

# Column for right ear
with right:
    barcolor = evaluation_right["Color"]
    fig = pl.Figure(pl.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = r_sum,
        mode = "gauge+number",
        gauge = {'axis': {'range': [None, 350],
                      'tickvals': [evaluation_right["Mild"], evaluation_right["Significant"]],
                      'ticktext': [evaluation_right["Mild"], evaluation_right["Significant"]]},
                'bar': {'color': barcolor},
                'steps' : [
                    {'range': [0, evaluation_right["Mild"]], 'color': "#8ace7e"},
                    {'range': [evaluation_right["Mild"], evaluation_right["Significant"]], 'color': "#ffda66"},
                    {'range': [evaluation_right["Significant"], 350], 'color': "#ff684c"}],
                'threshold' : {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': r_sum}}))
    fig.update_layout(
        autosize=False,
        width=340,  # Set the width of the figure
        height=260,  # Set the height of the figure
        margin=dict(
            l=10,  # left margin
            r=10,  # right margin
            b=10,  # bottom margin
            t=20,  # top margin
            pad=20  # padding
        ),
        title_text="Right Ear: "+evaluation_right["Label"],  # Sets title text
        title_x=0.5,               # Centers the title horizontally
        title_y=0.95,              # Set the title in the top part of the plot
        title_xanchor='center',    # Ensures the title's x-position is centered
        title_yanchor='top',       # Ensures the title's y-position is at the top
        title_font=dict(
            family="Open Sans, verdana, arial, sans-serif",
            size=18,
            color="gray"
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

# Show manual input
with st.expander("Manual Input", expanded=True):

    # Create 8 columns for the manual data entry
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    # Column for 500Hz
    with col1:
        st.selectbox("500Hz", list(range(-10, 71, 5)), key="l500")
        st.selectbox("500Hz", list(range(-10, 71, 5)), key="r500")

    # Column for 1000Hz
    with col2:
        st.selectbox("1000Hz", list(range(-10, 71, 5)), key="l1000")
        st.selectbox("1000Hz", list(range(-10, 71, 5)), key="r1000")

    # Column for 2000Hz
    with col3:
        st.selectbox("2000Hz", list(range(-10, 71, 5)), key="l2000")
        st.selectbox("2000Hz", list(range(-10, 71, 5)), key="r2000")

    # Column for 3000Hz
    with col4:
        st.selectbox("3000Hz", list(range(-10, 71, 5)), key="l3000")
        st.selectbox("3000Hz", list(range(-10, 71, 5)), key="r3000")

    # Column for 4000Hz
    with col5:
        st.selectbox("4000Hz", list(range(-10, 71, 5)), key="l4000")
        st.selectbox("4000Hz", list(range(-10, 71, 5)), key="r4000")

    # Column for 6000Hz
    with col6:
        st.selectbox("6000Hz", list(range(-10, 71, 5)), key="l6000")
        st.selectbox("6000Hz", list(range(-10, 71, 5)), key="r6000")

    # Column for 8000Hz
    with col7:
        st.selectbox("8000Hz", list(range(-10, 71, 5)), key="l8000")
        st.selectbox("8000Hz", list(range(-10, 71, 5)), key="r8000")

    # Create a dataframe from the manual input
    df = pd.DataFrame({
        "Frequency": [500, 1000, 2000, 3000, 4000, 6000, 8000],
        "Left": [state.l500, state.l1000, state.l2000, state.l3000, state.l4000, state.l6000, state.l8000],
        "Right": [state.r500, state.r1000, state.r2000, state.r3000, state.r4000, state.r6000, state.r8000]
    })

    # Create the plot
    fig = px.line(df, x='Frequency', y=['Left', 'Right'])

    # Invert the y-axis and set the range
    fig.update_yaxes(
        autorange=False, 
        range=[70, -10], 
        tickvals=[i for i in range(-10, 71, 10)], 
        ticktext=[f"{i} dB" for i in range(-10, 71, 10)]
    )

    fig.update_xaxes(
        # Set tickvals and ticktext to show only the frequencies that were tested
        tickvals=[i for i in frequencies],
        ticktext=[f"{i} Hz" for i in frequencies],
        # Show gridlines
        showgrid=True,
    )
    fig.update_layout(
        yaxis_title="Threshold",
        height=400,
        showlegend=True,
        legend_title_text=None
    )

    # Set the line color for the "Left" series to blue
    fig.update_traces(line_color="blue", selector=dict(name="Left"))

    # Set the line color for the "Right" series to red
    fig.update_traces(line_color="red", selector=dict(name="Right"))

    st.plotly_chart(fig, use_container_width=True)

