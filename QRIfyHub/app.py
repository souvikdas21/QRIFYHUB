import cv2
import streamlit as st
import numpy as np
import qrcode
import os
import time
from PIL import Image

timestr = time.strftime("%Y%m%d-%H%M%S")

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4  # Adjust border for padding
)

def load_image(img):
    try:
        im = Image.open(img)
        return im
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

def main():
    # Set Streamlit page configuration
    st.set_page_config(page_title="QRifyHub", page_icon=":barcode:")

    # Main title and tagline
    st.title("QRifyHub")
    st.write("Your Gateway to Seamless QR Experiences")

    # Menu options for the sidebar
    menu_options = ["Generate QR Code", "Decode QR Code"]

    # Adjusted sidebar layout
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Select an option", menu_options)

    if choice == "Generate QR Code":
        # Generate QR Code Section
        st.subheader("Generate QR Code")

        # Form for entering text
        with st.form(key='myqr_form'):
            raw_text = st.text_area("Enter Text Here")
            submit_button = st.form_submit_button("Generate QR Code", help="Click this button to generate the QR code.")

        if submit_button:
            col1, col2 = st.columns(2)

            with col1:
                try:
                    # Generate QR code
                    qr.clear()
                    qr.add_data(raw_text)
                    qr.make(fit=True)

                    img = qr.make_image(fill_color='black', back_color='white')

                    # Save the generated QR code image
                    img_filename = 'generate_image_{}.png'.format(timestr)
                    path_for_images = os.path.join('image_folder', img_filename)
                    img.save(path_for_images)

                    final_img = load_image(path_for_images)
                    if final_img:
                        st.image(final_img, caption="Generated QR Code", use_column_width=True)
                except Exception as e:
                    st.error(f"Error generating QR code: {e}")

            with col2:
                st.info("Original Text")
                st.write(raw_text)

        # How to Use for Generate QR Code
        st.sidebar.markdown("""
        #### How to Use - Generate QR Code
        1. Enter the text you want to encode in the 'Enter Text Here' text area.
        2. Click the 'Generate QR Code' button to create the QR code.
        """)

    elif choice == "Decode QR Code":
        # Decode QR Code Section
        st.subheader("Decode QR Code")

        # Upload image for decoding
        image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
        if image_file is not None:
            try:
                file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
                opencv_image = cv2.imdecode(file_bytes, 1)
                c1, c2 = st.columns(2)
                with c1:
                    st.image(opencv_image, caption="Uploaded Image")

                with c2:
                    st.info("Decoded QR code")
                    det = cv2.QRCodeDetector()

                    retval, points, straight_qrcode = det.detectAndDecode(opencv_image)

                    if retval:
                        st.write(f"Decoded text: {retval}")
                    else:
                        st.warning("No QR code found in the image.")
            except Exception as e:
                st.error(f"Error decoding QR code: {e}")

        # How to Use for Decode QR Code
        st.sidebar.markdown("""
        #### How to Use - Decode QR Code
        1. Upload an image containing a QR code using the 'Upload Image' button.
        2. The decoded text will be displayed in the 'Decoded QR code' section.
        """)

if __name__ == "__main__":
    main()
