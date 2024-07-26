import streamlit as st
import streamlit_and_components as sac
from pages_ import pages



def main() -> None:
    # if 'index' not in st.session_state:
    #     st.session_state['index'] = 0

    with st.sidebar.container():
        menu = sac.menu(
            items=list(pages.keys()),
            # index=st.session_state['index'],
            index=1,
            open_all=True,
            size='middle',
            format_func=lambda page: pages[page].title,
        )
        st.sidebar.info("Made with ❤ by the ikanam")

    with st.container():
        if menu in pages:
            pages[menu].method()


if __name__ == "__main__":
    main()
