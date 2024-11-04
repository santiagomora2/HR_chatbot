import streamlit as st
import streamlit.components.v1 as components

def main():
    st.set_page_config(
            page_title="Inicio",
            layout="centered"
        )

    # Remove Streamlit's default padding and margin
    st.markdown(
        """
        <style>
            /* Remove top margin and padding of the main Streamlit section */
            .stMain {
                padding-top: 0rem !important;
                margin-top: 0rem !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # Custom HTML with inline styling
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <style>
            /* Full-screen animated background */
            body {
                background-image: url('https://media.tenor.com/53I_s_sx9ncAAAAM/black-space-stars.gif'); /* Replace with your animated image URL */
                background-size: cover;
                background-attachment: fixed;
                height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            }

            /* Container for the title and divider */
            .container {
                position: relative;
                text-align: center;
                color: white;
                max-width: 800px;
                width: 100%;
            }

            /* Vertical divider line */
            .line {
                border-left: 2px solid white;
                height: 90vh; /* Adjust height as needed */
                position: absolute;
                left: 50%;
                transform: translateX(-50%);
            }

            /* Big title text on the left */
            .big-title {
                font-size: 50px;
                font-weight: bold;
                position: absolute;
                left: 25%; /* Adjust left alignment */
                transform: translateX(-50%);
                top: 15%;
            }

            /* Small title text on the right */
            .small-title {
                font-size: 24px;
                position: absolute;
                left: 75%; /* Adjust right alignment */
                transform: translateX(-50%);
                top: 15%;
            }

        </style>
    </head>
    <body>
        <div class="container">
            <div class="big-title">HR AI</div>
            <div class="line"></div>
            <div class="small-title">Eleva tu reclutamiento con AI</div>
        </div>
    </body>
    </html>
    """

    # Display the custom HTML in Streamlit
    components.html(html_code, height=350)

    cols = st.columns(4)
    with cols[0]:
        st.page_link("pages/ask.py", label="Pregunta a la IA", icon="🤖")
    with cols[3]:
        st.page_link("pages/explore.py", label="Explorar candidatos", icon="👤")


if __name__ == '__main__':
    main()