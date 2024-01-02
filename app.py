import argparse

import streamlit as st
from streamlit_javascript import st_javascript as st_js

import tts
from lang.en import ttb
from utils import gen_cols, mobile_markdown, state_append_braille, state_append_num, state_pop

parser = argparse.ArgumentParser()
parser.add_argument('--dev', action='store_true')
args = parser.parse_args()

if 'text' not in st.session_state:
    st.session_state.text = ''
if 'braille' not in st.session_state:
    st.session_state.braille = ''
if 'speech' not in st.session_state:
    st.session_state.speech = 'male'
if 'cols' not in st.session_state:
    st.session_state.cols = 1

with st.sidebar:
    st.header("DotBraille GP1 Demo")
    with st.expander("About this app"):
        st.markdown("This is a proof of concept demo that demonstrates how braille to text conversion works, "
                    "and converting text to speech")
    with st.expander("Configuration", expanded=True):
        disp_letters = st.checkbox("Display Letters", value=True)
        st.session_state.speech = st.selectbox("Voice", options=['male', 'female'])
    if args.dev:
        with st.expander('dev'):
            st.json(st.session_state)

mobile_markdown()
if st_js('screen.width') >= 600:
    st.session_state.cols = 7
else:
    st.session_state.cols = 4

st.write("##### Inputted Braille")
st.code(st.session_state.braille)
st.write("##### Converted Text")
st.code(st.session_state.text)

col1, col2 = st.columns(2)
if col1.button('convert to speech', disabled=(st.session_state.text == '')):
    col2.audio(tts.convert(st.session_state.text), format='audio/mpeg')

st.write("##### Input")
with st.expander(label="Letters", expanded=True):
    with gen_cols(ttb['letter_conversion'], st.session_state.cols) as column:
        for i, di in enumerate(ttb['letter_conversion']):
            column[i].button(
                label=f"{di['braille']}{di['display'] if disp_letters else ''}",
                help=di['display'],
                on_click=state_append_braille,
                args=[di['letter'], di['braille']],
            )

with st.expander(label="Numbers", expanded=True):
    with gen_cols(ttb['number_conversion'], st.session_state.cols) as column:
        for i, di in enumerate(ttb['number_conversion']):
            column[i].button(
                label=f"{di['braille']}{di['display'] if disp_letters else ''}",
                help=di['display'],
                on_click=state_append_num,
                args=[di['num'], di['braille'], ttb],
            )

with st.expander(label="Miscellaneous", expanded=True):
    with gen_cols(ttb['special_conversion'], st.session_state.cols) as column:
        for i, di in enumerate(ttb['special_conversion']):
            if 'hidden' in di:
                continue
            if 'callback' in di:
                column[i - 1].button(
                    label=di['display'],
                    on_click=di['callback'],
                )
            else:
                column[i - 1].button(
                    label=di['display'],
                    on_click=state_append_braille,
                    args=[di['letter'], di['braille']],
                )
