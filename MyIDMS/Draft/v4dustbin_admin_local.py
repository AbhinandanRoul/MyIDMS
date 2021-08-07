import streamlit as st,os,mysql.connector, datetime, geocoder

hostname='localhost'
database='myidms'
username='root'
password='1234'

add_selectbox = st.sidebar.selectbox(
    "NAVIGATION",  # Title of sidebar
    (
        "Reporting Tool", 'Service Portal',"Admin Dashboard")
    # List of all options in sidebar
)

if add_selectbox=='Reporting Tool':

    st.title("MyIDMS")
    st.header("Intelligent Dustbin Management System")
    email=st.text_input('Enter your email')
    dustbinID=st.number_input('Enter dustbin ID')
    #st.selectbox('Select area', area)

    st.write("Upto which colour is the dustbin filled?")
    c=st.selectbox('Which colour do you see?', ('Black','Red','Blue','Grey','White'))
    colour=['Black','Red','Blue','Grey','White']
    comment=['FULL-URGENT','Nearly FULL','HALF-FULL','Nearly EMPTY','EMPTY']
    i=colour.index(c);
    dustbin_status=comment[i]

    weight_list=[10,8,5,2,1]
    dustbin_weight=weight_list[i]

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

        # -------------------------------------------- SQL Code to insert data ------------------------------------------
        def insertBLOB(email, dustbin_status, photo, date, time, loc, dustbinID):
            mydb = mysql.connector.connect(host=hostname, database=database, user=username, password=password)
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

        def addDustbin(dustbinID):
            mydb = mysql.connector.connect(host=hostname, database=database, user=username, password=password)
            mycursor = mydb.cursor()
            mydb.commit()
            try:
                # To insert a row into the table with reg no. as primary key
                sql_insert = "INSERT INTO dustbinlist (dustbinID,weight,reports_number,AvgWt) VALUES ({dustbinID},0,0,0)".format(dustbinID=dustbinID)
                mycursor.execute(sql_insert)
                mydb.commit()
            except:
                print("Already present")

        def updateDustbin(dustbinID, dustbin_weight):
            # Increase report count by 1
            connection = mysql.connector.connect(host=hostname, database=database, user=username, password=password)
            cursor = connection.cursor()
            sqlfind = "select weight, reports_number from dustbinlist where dustbinID={}".format(dustbinID)
            cursor.execute(sqlfind)
            result = cursor.fetchall()
            for x in result:
                weight = x[0]
                report_number = x[1]
            report_number = report_number + 1
            weight = weight + dustbin_weight
            AvgWt = round((weight / report_number),2)
            print(weight, report_number, AvgWt)
            sql2 = "update dustbinlist set weight={weight}, reports_number={reports_number},AvgWt={AvgWt} where dustbinID={dustbinID}".format(
                weight=weight, reports_number=report_number, AvgWt=AvgWt, dustbinID=dustbinID)
            cursor.execute(sql2)
            connection.commit()

        # addDustbin(dustbinID)
        updateDustbin(dustbinID, dustbin_weight)
# -------------------------------------------------------------------------------------------------------------------
elif add_selectbox=='Admin Dashboard':
    import streamlit as st, os, mysql.connector, datetime
    import pandas as pd

    st.title('Admin Dashboard')
    arealist = ['SHOW ALL', 'Rasulgarh', 'Jagamara', 'Khandagiri', 'chandrasekharpur', 'rail vihar', 'Patia',
                'Infocity', 'Mancheswar', 'Jaydev Vihar', 'Dumduma', 'Kalinga Vihar', 'Patrapada', 'Pokhariput',
                'IRC Village', 'Neyapalli', 'Bapuji nagar', 'Ashok nagar', 'Kharabela nagar', 'Acharya vihar',
                'Bapuji nagar', 'Jharpada', 'Kalpana Square', 'BJB nagar']
    # arealist.sort() ## Uncomment this to sort the area list
    localtiy = st.selectbox('Select Area', arealist)
    cleanID = st.number_input('Enter ID of cleaned dustbin')
    k = st.button('Clean')
    placeholder = st.empty()


    def showDustbinlist():
        dustbinID = [];area = [];weight = []; reports_number = []; AvgWt = [];
        mydb = mysql.connector.connect(host=hostname, database=database, user=username, password=password)
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM dustbinlist")
        myresult = cursor.fetchall()
        for x in myresult:
            # st.write(x[0],x[1],x[2],x[3])
            dustbinID.append(x[0])
            area.append(x[1])
            weight.append(x[2])
            reports_number.append(x[3])
            AvgWt.append(x[4])
        dict = {'DustbinID': dustbinID, 'Locality': area, 'Weighted Score': weight, 'No. of Reports': reports_number,
                'Average Weighted Score': AvgWt}
        df = pd.DataFrame(dict)
        df = df.sort_values(by='Average Weighted Score', ascending=False)
        placeholder.table(df)


    def cleanDustbin(cleanID):
        connection = mysql.connector.connect(host=hostname, database=database, user=username, password=password)
        cursor = connection.cursor()
        sql = "update dustbinlist set weight={weight}, reports_number={reports_number},AvgWt={AvgWt} where dustbinID={dustbinID}".format(
            weight=0, reports_number=0, AvgWt=0, dustbinID=cleanID)
        cursor.execute(sql)
        connection.commit()


    def showDustbinlistbylocality(locality):
        dustbinID = [];
        area = [];
        weight = [];
        reports_number = [];
        AvgWt = [];
        mydb = mysql.connector.connect(host=hostname, database=database, user=username, password=password)
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM dustbinlist")
        myresult = cursor.fetchall()
        for x in myresult:
            # st.write(x[0],x[1],x[2],x[3])
            if (x[1] == locality):
                dustbinID.append(x[0])
                area.append(x[1])
                weight.append(x[2])
                reports_number.append(x[3])
                AvgWt.append(x[4])
        dict = {'DustbinID': dustbinID, 'Locality': area, 'Weighted Score': weight, 'No. of Reports': reports_number,
                'Average Weighted Score': AvgWt}
        df = pd.DataFrame(dict)
        df = df.sort_values(by='Average Weighted Score', ascending=False)
        placeholder.table(df)  # placeholder.write(df)


    # showDustbinlist()
    if (localtiy == 'SHOW ALL'):
        showDustbinlist()
    else:
        showDustbinlistbylocality(localtiy)

    if (k == True):
        st.success('Dustbin {} is cleaned, UPDATED'.format(cleanID))
        cleanDustbin(cleanID)
        showDustbinlistbylocality(localtiy)


elif add_selectbox=='Service Portal':
    import pandas as pd
    st.title('Service Portal')

    BMC_ID = st.number_input('Enter your BMC ID')
    pwd = st.text_input('Enter your password')

    # Search only Rasulgarh dustbins
    placeholder1  = st.empty()
    placeholder2 = st.empty()
    placeholder3 =st.empty()


    def showDustbinlist(locality):
        dustbinID = [];
        area = [];
        weight = [];
        reports_number = [];
        AvgWt = [];
        mydb = mysql.connector.connect(host=hostname, database=database, user=username, password=password)
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM dustbinlist")
        myresult = cursor.fetchall()
        for x in myresult:
            # st.write(x[0],x[1],x[2],x[3])
            if (x[1] == locality):
                dustbinID.append(x[0])
                area.append(x[1])
                weight.append(x[2])
                reports_number.append(x[3])
                AvgWt.append(x[4])
        dict = {'DustbinID': dustbinID, 'Locality': area, 'Weighted Score': weight, 'No. of Reports': reports_number,
                'Average Weighted Score': AvgWt}
        df = pd.DataFrame(dict)
        df = df.sort_values(by='Average Weighted Score', ascending=False)
        placeholder3.table(df)  # placeholder.write(df)


    def passwordvalidation():
        mydb = mysql.connector.connect(host=hostname, database=database, user=username, password=password)
        cursor = mydb.cursor()
        sqlfind = "select password from workerlogin where BMC_ID={}".format(BMC_ID)
        cursor.execute(sqlfind)
        result = cursor.fetchall()
        return (result[0][0])


    def login():
        mydb = mysql.connector.connect(host=hostname, database=database, user=username, password=password)
        cursor = mydb.cursor()
        sqlfind = "select BMC_ID, password, area, name from workerlogin where BMC_ID={}".format(BMC_ID)
        cursor.execute(sqlfind)
        result = cursor.fetchall()
        for x in result:
            placeholder1.header("Hello {}".format(x[3]))
            placeholder2.subheader("You are in charge of {} area ".format(x[2]))


    def locality():
        mydb = mysql.connector.connect(host=hostname, database=database, user=username, password=password)
        cursor = mydb.cursor()
        sqlfind = "select area from workerlogin where BMC_ID={}".format(BMC_ID)
        cursor.execute(sqlfind)
        result = cursor.fetchall()
        return result[0][0]


    def cleanDustbin(cleanID):
        connection = mysql.connector.connect(host=hostname, database=database, user=username, password=password)
        cursor = connection.cursor()
        sql = "update dustbinlist set weight={weight}, reports_number={reports_number},AvgWt={AvgWt} where dustbinID={dustbinID}".format(
            weight=0, reports_number=0, AvgWt=0, dustbinID=cleanID)
        cursor.execute(sql)
        connection.commit()

    # showDustbinlist()
    # login()
    if (passwordvalidation() == pwd):
        login()
        showDustbinlist(locality())
        cleanID = st.number_input('Enter dustbinID to clean')
        if (st.button('CLEAN')):
            cleanDustbin(cleanID)
            showDustbinlist(locality())
