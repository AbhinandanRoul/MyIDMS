import streamlit as st,os,mysql.connector, datetime
import pandas as pd
st.title('Admin Dashboard')
# dustbinID=[]; weight=[]; reports_number=[]; AvgWt=[];
cleanID=st.number_input('Enter ID of cleaned dustbin')
k=st.button('Clean')
placeholder = st.empty()
def showDustbinlist():
    dustbinID = []; weight = []; reports_number = []; AvgWt = [];
    mydb = mysql.connector.connect(host='localhost', database='myidms', user='root', password='1234')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM dustbinlist")
    myresult = cursor.fetchall()
    #st.write('DustbinID,','Weight,','Reports,','Avg. Wt')
    for x in myresult:
        #st.write(x[0],x[1],x[2],x[3])
        dustbinID.append(x[0])
        weight.append(x[1])
        reports_number.append(x[2])
        AvgWt.append(x[3])
    dict = {'DustbinID': dustbinID, 'Weighted Score': weight, 'No. of Reports': reports_number,'Average Weighted Score':AvgWt}
    df = pd.DataFrame(dict)
    df = df.sort_values(by='Average Weighted Score', ascending=False)
    placeholder.write(df)

def cleanDustbin(cleanID):
    connection = mysql.connector.connect(host='localhost', database='myidms', user='root', password='1234')
    cursor = connection.cursor()
    sql = "update dustbinlist set weight={weight}, reports_number={reports_number},AvgWt={AvgWt} where dustbinID={dustbinID}".format(weight=0, reports_number=0, AvgWt=0, dustbinID=cleanID)
    cursor.execute(sql)
    connection.commit()
showDustbinlist()

if(k==True):
    st.success('Dustbin {} is cleaned, UPDATED'.format(cleanID))
    cleanDustbin(cleanID)
    showDustbinlist()