import streamlit as st
st.title("MyIDMS")
st.header("Intelligent Dustbin Management System")

st.write("Upto which colour is the dustbin filled?")
c=st.selectbox('Which colour do you see?', ('Black','Red','Blue','Grey','White'))
#st.write('You selected:',c)
colour=['Black','Red','Blue','Grey','White']
comment=['FULL-URGENT','Nearly FULL','HALF-FULL','Nearly EMPTY','EMPTY']
i=colour.index(c);
st.write('Dustbin is:',comment[i])
k1=st.button('SEND')
st.success("Successfully Submitted")


import streamlit as st
from webcam import webcam

captured_image = webcam()
if captured_image is None:
    st.write("Waiting for capture...")
else:
    st.write("Got an image from the webcam:")
    st.image(captured_image)