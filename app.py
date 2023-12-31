from contextlib import contextmanager

import streamlit as st
from streamlit_javascript import st_javascript as st_js

if 'text' not in st.session_state:
    st.session_state.text = ''
if 'braille' not in st.session_state:
    st.session_state.braille = ''
if 'speech' not in st.session_state:
    st.session_state.speech = None

char_dict = {"a": u"\u2801",
             "b": u"\u2803",
             "c": u"\u2809",
             "d": u"\u2819",
             "e": u"\u2811",
             "f": u"\u280b",
             "g": u"\u281b",
             "h": u"\u2813",
             "i": u"\u280a",
             "j": u"\u281a",
             "k": u"\u2805",
             "l": u"\u2807",
             "m": u"\u280d",
             "n": u"\u281d",
             "o": u"\u2815",
             "p": u"\u280f",
             "q": u"\u281f",
             "r": u"\u2817",
             "s": u"\u280e",
             "t": u"\u281e",
             "u": u"\u2825",
             "v": u"\u2827",
             "w": u"\u283a",
             "x": u"\u282d",
             "y": u"\u283d",
             "z": u"\u2835",
             }

num_dict = {
    "1": u"\u2802",
    "2": u"\u2806",
    "3": u"\u2812",
    "4": u"\u2832",
    "5": u"\u2822",
    "6": u"\u2816",
    "7": u"\u2836",
    "8": u"\u2826",
    "9": u"\u2814",
    "0": u"\u2834",
}

extra_dict = {
    " ": "SPACE",
    "\n": "ENTER",
}

st.markdown("""
<style>
@media only screen and (max-width: 600px) {
    [data-testid="column"] {
        width: calc(25% - 1rem) !important;
        flex: 1 1 calc(25% - 1rem) !important;
        min-width: calc(20% - 1rem) !important;
    }
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Configuration")
    with st.expander("About this app"):
        st.markdown("It's about cats :cat:!")

if int(st_js('screen.width')) >= 600:
    n_cols = 7
else:
    n_cols = 4


@contextmanager
def gen_cols(odict):
    n_rows = 1 + (len(odict)) // int(n_cols)
    rows = [st.container() for _ in range(n_rows)]
    cols_per_row = [r.columns(n_cols) for r in rows]
    cols = [column for row in cols_per_row for column in row]

    yield cols


def state_append_char(letter: str):
    st.session_state.text += letter


def state_append_braille(letter: str, braille: str):
    state_append_char(letter)
    st.session_state.braille += braille


def state_append_num(num: str | int, braille: str):
    state_append_char(str(num))
    st.session_state.braille += (u"\u283c" + braille)


with st.expander(label="Letters", expanded=True):
    with gen_cols(char_dict) as cols:
        for i, clm in enumerate(char_dict):
            cols[i].button(
                label=char_dict[clm],
                help=clm.upper(),
                on_click=state_append_braille,
                args=[clm, char_dict[clm]]
            )

with st.expander(label="Numbers", expanded=True):
    with gen_cols(num_dict) as cols:
        for i, clm in enumerate(num_dict):
            cols[i].button(
                label=num_dict[clm],
                help=clm,
                on_click=state_append_num,
                args=[clm, num_dict[clm]]
            )

with st.expander(label="", expanded=True):
    with gen_cols(extra_dict) as cols:
        for i, clm in enumerate(extra_dict):
            cols[i].button(
                label=extra_dict[clm],
                on_click=state_append_char,
                args=[clm]
            )

st.text_area(label="Inputted Braille", value=st.session_state.braille)
st.text_area(label="Converted Text", value=st.session_state.text)
