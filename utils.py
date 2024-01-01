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
    </style>
    """, unsafe_allow_html=True)


@contextmanager
def gen_cols(odict, n_cols):
    n_rows = 1 + (len(odict)) // int(n_cols)
    rows = [st.container() for _ in range(n_rows)]
    cols_per_row = [r.columns(n_cols) for r in rows]
    cols = [column for row in cols_per_row for column in row]

    yield cols
