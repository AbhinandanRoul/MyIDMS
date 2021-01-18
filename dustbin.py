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

file=st.file_uploader("Pic of inside dustbin")
k1=st.button('SEND')
if(k1==True):
    st.success("Successfully Submitted")

