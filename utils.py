from contextlib import contextmanager

import streamlit as st


def mobile_markdown():
    st.markdown("""
    <style>
    @media only screen and (max-width: 600px) {
        [data-testid="column"] {
            width: calc(25% - 1rem) !important;
            flex: 1 1 calc(25% - 1rem) !important;
            min-width: calc(20% - 1rem) !important;
        }
    }
    viewerBadge_link__qRIco {
        display: none;
        visibility: hidden;
    }
    [data-testid="stToolbarActions"] {
        display: none;
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)


@contextmanager
def gen_cols(odict, n_cols):
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


def state_append_num(num: str | int, braille: str, ttb):
    state_append_char(str(num))
    st.session_state.braille += (ttb['special_conversion'][0]['braille'] + braille)
