import streamlit as st
import cv2
import numpy as np
from object_detection_module import realtime  # Replace with the correct import

st.title("Melanoma Detection")

upload_button_key = "upload_button"
stop_stream_button_key = "stop_stream_button"
method_selection_key = "method_selection"

processing_method = st.selectbox("Choose Processing Method", ("File Upload", "Real-time Detection"), key=method_selection_key)

if processing_method == "File Upload":
    uploaded_image = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"], key=upload_button_key)

    if uploaded_image is not None:
        image = cv2.imdecode(np.frombuffer(uploaded_image.read(), np.uint8), cv2.IMREAD_COLOR)
        processed_image = realtime(image)

        st.image(processed_image, caption="Processed Image")

elif processing_method == "Real-time Detection":
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Error: Unable to access the webcam")
    else:
        stop_button_placeholder = st.empty()
        stop_button = stop_button_placeholder.button("Stop Stream", key=stop_stream_button_key)
        frame_placeholder = st.empty()
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("Error: Unable to capture frame from webcam")
                break
            processed_frame = realtime(frame)
            frame_placeholder.image(processed_frame, channels="BGR", caption="Real-time Detection")
            if stop_button:
                break
        cap.release()

else:
    st.warning("Please select a processing method.")
