import streamlit as st,os,mysql.connector, datetime, geocoder
st.title("MyIDMS")
st.header("Intelligent Dustbin Management System")

email=st.text_input('Enter your email')
dustbinID=st.text_input('Enter dustbin ID')
st.write("Upto which colour is the dustbin filled?")
c=st.selectbox('Which colour do you see?', ('Black','Red','Blue','Grey','White'))
colour=['Black','Red','Blue','Grey','White']
comment=['FULL-URGENT','Nearly FULL','HALF-FULL','Nearly EMPTY','EMPTY']
i=colour.index(c);
dustbin_status=comment[i]
st.write('Dustbin is:',dustbin_status)
dustbin_photo=st.file_uploader("Pic of inside dustbin",  type=["png", "jpg", "jpeg"])
k1=st.button('Submit')
if(k1==True):
    x = datetime.datetime.now()
    today_date = str(x.strftime("%d-%m-%Y"))
    current_time = x.strftime("%H:%M:%S")
    g = geocoder.ip('me')
    loc=str(g.latlng)
    #print(email, dustbin_status, today_date, current_time, loc)
    def CreateTempDir():
        k = os.path.exists("temp")
        if not k:
            os.mkdir("temp")
    CreateTempDir()
    # ---------------------------------------------------
    def convertToBinaryData(filename):
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
    # ------------------------------------------------------

    # --------------------------------------------SQL Code to insert data------------------------------------------
    def insertBLOB(email, dustbin_status, photo, date, time, loc, dustbinID):
        mydb = mysql.connector.connect(host="localhost", database="myidms", user="root", password="1234")
        my_cursor = mydb.cursor()
        sql_insert_blob_query = "INSERT INTO reports (email, dustbin_status, photo, date, time, loc, dustbinID) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        converted_picture = convertToBinaryData(photo)
        # Convert data into tuple format
        insert_blob_tuple = (email, dustbin_status, converted_picture, date, time,loc, dustbinID)
        result = my_cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        mydb.commit()
        print("Image inserted successfully as a BLOB into report table", result)
    # ------------------------------------------SQL Code to Insert Data--------------------------------------------

    # --------- Pass the uploaded file through streamlit to SQL----------------
    def save_uploadedfile(uploadedfile):
        with open(os.path.join("temp", uploadedfile.name), "wb") as f:
            f.write(uploadedfile.getbuffer())  # Writes the file to directory Local
        # Calls function to insert the photo and details into SQL
        insertBLOB(email, dustbin_status, 'temp/{}'.format(uploadedfile.name), today_date, current_time, loc, dustbinID)
        return st.success("Successfully Submitted")

    if (dustbin_photo != None):
        save_uploadedfile(dustbin_photo)
