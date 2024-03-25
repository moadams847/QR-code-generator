import streamlit as st
import qrcode
import os
from pathlib import Path
import uuid
from datetime import datetime
import time

# Get the current date and time
now = datetime.now()

# Format the date and time
formatted_now = now.strftime("%d-%m-%Y %H-%M")

def ensure_session_id():
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

def get_session_directory(): 
    ensure_session_id()
    session_dir = Path('artifacts') / st.session_state.session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir

st.title('QR Code Generator')

user_url = st.text_input('Input your link')

submit_button = st.button('Generate QR Code')
       
if submit_button: 

    if len(user_url) > 0:

        qr = qrcode.QRCode(version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L, 
                        box_size=10, border=4)
        
        qr.add_data(user_url)
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image to a file
        session_dir = get_session_directory()  # Use session-specific directory

        img.save(session_dir / "qr_code.png")

        success_message = st.empty()  # Create an empty element for dynamic success message

        success_message.success("QR code generated successfully.")

        image_filename = "qr_code.png" 

        file_name = f"{image_filename}"

        image_path = session_dir / image_filename

        st.image(str(image_path))

        st.download_button(
        label="Download QR code",
        data=open(image_path, 'rb').read(),
        file_name=file_name,
        mime='application/octet-stream'
        )

        # Sleep for 5 seconds and then remove the success message
        time.sleep(5)
        success_message.empty()  # Remove the success message after 5 seconds


    else:
        st.error("Input an appropriate Link")
