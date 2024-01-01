import argparse

import streamlit as st
from streamlit_javascript import st_javascript as st_js

from lang.en import ttb
from utils import gen_cols, mobile_markdown

parser = argparse.ArgumentParser()
parser.add_argument('--dev', action='store_true')
args = parser.parse_args()

if 'text' not in st.session_state:
    st.session_state.text = ''
if 'braille' not in st.session_state:
    st.session_state.braille = ''
if 'speech' not in st.session_state:
    st.session_state.speech = None
if 'cols' not in st.session_state:
    st.session_state.cols = 1

with st.sidebar:
    st.header("DotBraille GP1 Demo")
    with st.expander("About this app"):
        st.markdown("This is a proof of concept demo that demonstrates how braille to text conversion works, "
                    "and converting text to speech")
    with st.expander("Configuration", expanded=True):
        st.checkbox("Display Letters", value=True)
    if args.dev:
        with st.expander('dev'):
            st.code(st.session_state)

mobile_markdown()
if st_js('screen.width') >= 600:
    st.session_state.cols = 7
else:
    st.session_state.cols = 4


def state_append_char(letter: str):
    st.session_state.text += letter


def state_append_braille(letter: str, braille: str):
    state_append_char(letter)
    st.session_state.braille += braille


def state_append_num(num: str | int, braille: str):
    state_append_char(str(num))
    st.session_state.braille += (ttb['special_conversion'][0]['braille'] + braille)


st.write("##### Inputted Braille")
st.code(st.session_state.braille)
st.write("##### Converted Text")
st.code(st.session_state.text)

st.write("##### Input")
with st.expander(label="Letters", expanded=True):
    with gen_cols(ttb['letter_conversion'], st.session_state.cols) as column:
        for i, di in enumerate(ttb['letter_conversion']):
            column[i].button(
                label=di['braille'],
                help=di['display'],
                on_click=state_append_braille,
                args=[di['letter'], di['braille']]
            )

with st.expander(label="Numbers", expanded=True):
    with gen_cols(ttb['number_conversion'], st.session_state.cols) as column:
        for i, di in enumerate(ttb['number_conversion']):
            column[i].button(
                label=di['braille'],
                help=di['display'],
                on_click=state_append_num,
                args=[di['num'], di['braille']]
            )

with st.expander(label="Miscellaneous", expanded=True):
    with gen_cols(ttb['special_conversion'], st.session_state.cols) as column:
        for i, di in enumerate(ttb['special_conversion']):
            if 'hidden' in di:
                continue

            column[i - 1].button(
                label=di['display'],
                on_click=state_append_braille,
                args=[di['letter'], di['braille']]
            )
