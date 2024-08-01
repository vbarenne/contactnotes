#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 09:53:19 2024

@author: victoriawork
"""

import streamlit as st

st.set_page_config(
        page_title="ClientNotes.ai",
        page_icon="👋",
    )

st.write("# Welcome to ClientNotes.ai! 👋")

st.markdown(
"""

**ClientNotes.ai** harnesses AI and data to deliver services and experiences tailored to the customer's current and future expectations and requirements.
""")
# st.sidebar.success("Select a demo above.")


st.write("---")
# st.markdown(
# """
# ### How It Works

# 1. **Upload**: With ClientNotes.ai, relationship managers can capture their notes via voice recording. A transcription is then generated using the Global Innovation team's voice-to-text model, Joice. 

# 2. **Validate**: Improve quality of the data through validation, ensuring that the all best practices have been followed based on different client interaction situations. 

# 3. **Analytics**: Leverage of the content of the contact notes to help RMs better advise their clients. In particular, by providing action items for RMs and content/products to recommend to clients. 

# 4. **Search**: Enable RMs to quickly find the information they are looking for from contact notes. This could potentially go beyond a simple search engine and be a chatbot. 
# """
# )

st.markdown("""
### Features           
            
1. **Validate**: Leverage GenAI to improve quality of data through cross-checking and validation of contact notes against compliance requirements. 

2. **Action Items/Meeting Minutes**: Automatically generate action items/minutes based on client contact notes. 

3. **Contextual Search**: Utilizes GenAI to understand context, making it easier for relationship managers to locate specific details and insights. 

4. **Recommendations**: Personalized AI-driven recommendations of in-house research articles, products and actions tailored to individual customer needs.

"""
    )










