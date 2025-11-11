import streamlit as st
from loaddata import load_data
from load_overview import load_data_overview

# Define the page navigation
def navigate_to(page_name):
    st.session_state.current_page = page_name

# Define the main page content
def main_page():
    st.title('Welcome Knoed!')
    st.header('How do you want to improve your office?')

    # Create three columns for the options
    col1, col2, col3 = st.columns(3)

    # First column with image and button
    with col1:
        #st.image("path_to_your_image.jpg")  # Replace with your image path
        if st.button('Get insight in your rooms/spaces and its usage.'):
            navigate_to('room_insights')

    # Second column with image and button
    with col2:
        #st.image("path_to_your_image.jpg")  # Replace with your image path
        if st.button('Get instant tailor-made advices and analysis for your office.'):
            navigate_to('tailor_made_advices')

    # Third column with text
    with col3:
         st.markdown('Take a look at your meeting rooms and office within your digital twin. Click [here](https://oder.entweder.vc/).')

    # Footer
    #st.markdown('---')
    #st.markdown('Footer Officemanager')

    # Add a link to the Calendly page (replace '#' with your actual Calendly link)
    st.markdown('[Plan your free office consultancy session via this bullet.](#)')

# Define the room insights page content
def room_insights_page():
    st.title('Welcome Knoed!')
    st.write('Below you can find the usage of your space over the last < period > months.')
    month = st.selectbox(
        'Select a period:',
        range(1, 13)  # This creates a list of months from 1 to 12
    )

    st.subheader(f"Usage-table Entweder over the last {month} months.")
    uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)
    include_weekends = st.checkbox("Include weekends in analysis")
    if st.button("Process Data"):
        # Call load_data with the uploaded files and the include_weekends option
        if uploaded_files:
            load_data_overview(uploaded_files, month, include_weekends)
    st.button('Go back', on_click=navigate_to, args=('main',))

# Define the tailor-made advice page content
def tailor_made_advices_page():
    st.title('Welcome Knoed!')
    st.write('Below you can find the tailor-made advices for your office:')
    month = st.selectbox(
        'Select a period:',
        range(1, 13)  # This creates a list of months from 1 to 12
    )

    st.write(f"We recommend a period of at least 3 months to get highly accurate advices.")
    uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)
    include_weekends = st.checkbox("Include weekends in analysis")

    if st.button("Process Data"):
        # Call load_data with the uploaded files and the include_weekends option
        if uploaded_files:
            load_data(uploaded_files, month, include_weekends)
    st.button('Go back', on_click=navigate_to, args=('main',))
    
    if st.button("Overview per config"):
            st.session_state.current_page = "room_insights"

# Initialize the current_page if it doesn't exist
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'

# Display the current page based on session state
if st.session_state.current_page == 'main':
    main_page()
elif st.session_state.current_page == 'room_insights':
    room_insights_page()
elif st.session_state.current_page == 'tailor_made_advices':
    tailor_made_advices_page()
