import streamlit as st
import pyperclip
from PIL import Image, ImageOps
import io
import pyperclip
import win32clipboard

def get_image_from_clipboard():
    win32clipboard.OpenClipboard()
    try:
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
            img = Image.open(io.BytesIO(data))
            return img
    except Exception as e:
        st.error(f"Error getting image from clipboard: {e}")
    finally:
        win32clipboard.CloseClipboard()
    return None

def copy_image_to_clipboard(img):
    output = io.BytesIO()
    img.convert("RGB").save(output, format='BMP')
    data = output.getvalue()[14:]
    output.close()
    
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

st.title("Image Color Inverter")

if st.button("Paste Image from Clipboard"):
    img = get_image_from_clipboard()
    if img:
        st.image(img, caption="Original Image", use_column_width=True)
        inverted_img = ImageOps.invert(img.convert("RGB"))
        st.image(inverted_img, caption="Inverted Image", use_column_width=True)
        
        if st.button("Copy Inverted Image to Clipboard"):
            copy_image_to_clipboard(inverted_img)
            st.success("Inverted image copied to clipboard!")
