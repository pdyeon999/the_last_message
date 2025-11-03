import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI()

st.title("🛰 Project AURORA")
st.subheader("AI Memory Restoration Log")
