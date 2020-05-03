import streamlit as st
from real_example import main as real_example_main

SIMPLE_EXAMPLE = "Synthetic"
REAL_EXAMPLE = "European cities"


def main():
    st.sidebar.title("Ant colony optimisation")
    real_example_main()

    # exemple = st.sidebar.radio("Choose an exemple", [SIMPLE_EXAMPLE, REAL_EXAMPLE])

    # if exemple == SIMPLE_EXAMPLE:
    #     from simple_example import main as main_simple_example
    #     main_simple_example()
    # elif exemple == REAL_EXAMPLE:
    #     from real_example import main as
    #     pass


if __name__ == '__main__':
    main()
