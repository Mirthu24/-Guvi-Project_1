#importing Libraries
import streamlit as st
import pandas as pd
import pymysql

Route_name= pd.read_csv("Redbus Details.csv")
Busname_1 = Route_name.iloc[:,2]
# Get unique values and convert to list
States = Busname_1.unique().tolist()

# Setting webpage
st.set_page_config(layout="wide")
st.sidebar.image("C:/Users/new/Desktop/Redbus_Project/bus-30603_1280.webp",width=250)
web = st.sidebar.selectbox('Select the Page',("Home Page","Ticket Booking"))
st.sidebar.image("C:/Users/new/Desktop/Redbus_Project/buss.jpg",width=250)

# Home page setting
if web == "Home Page": 
    st.title(":red[WELCOME TO REDBUS HOMEPAGE]")
    
    st.header(":red[REDBUS TRANSPORTATION SERVICE]")
    
    st.subheader(":orange[_Start booking your tickets and enjoy your travel_]")
    
    Option = st.selectbox('Bus Bookings available for the States',("KERALA", "ANDHRA PRADESH", "TELANGANA",
                "RAJASTHAN","SOUTH BENGAL", "HIMACHAL PRADESH", "ASSAM", "WEST BENGAL", "PUNJAB","CHANDIGARH"))
    
    if st.button('Click'):
        st.write('You have selected',Option)
        st.write('Now go to the Ticket Booking Page to book your tickets') 
        st.balloons()
    
    st.image("C:/Users/new/Desktop/Redbus_Project/primoHomeBannerComp.webp")
    
    st.subheader("We are providing a Safe and secured Journey for all the citiziens of our nation")
    
# States and Routes page setting
if web == "Ticket Booking":
    st.title(":red[Online Ticket Booking]")

    Redbus = st.selectbox("**List of routes**",States)
    Bus_type = st.selectbox("**Select Bus Type**", ("Sleeper", "Seater", "Others"))
    
    col1,col2 = st.columns(2,gap = 'medium')
    with col1:
        Bus_fare = st.radio("**Select Bus Fare**",("100-500","500-1000","1000-3000","3000-6000"))
    with col2:
        Bus_rating = st.radio("**Select Bus Rating**",("1-3","3-4","4-5"),index=1)

    def filter_for_bus(Bustype,Price,Star_rating):
        con = pymysql.connect(host="localhost", user="root", password="Mirthu@243", database="REDBUS_DETAILS")
        mycursor = con.cursor()
        mycursor.execute("USE REDBUS_DETAILS")
        
        #type selection
        if Bustype == "Sleeper":
            Seat = "Bustype LIKE '%Sleeper%'"
        elif Bustype == "Seater":
            Seat = "Bustype LIKE '%Seater%'"
        else:
            Seat = "Bustype NOT LIKE '%Sleeper%' AND Bustype NOT LIKE '%Seater%'"
            
        #Price selection
        if Price == "100-500":
            Cost_min,Cost_max = 100,500
        elif Price == "500-1000":
            Cost_min,Cost_max = 500,1000
        elif Price == "1000-3000":
            Cost_min,Cost_max = 1000,3000
        else:
            Cost_min,Cost_max = 3000,6000
            
        # Star-Rating Selection    
        if Star_rating == "1-3":
            Star_min,Star_max = 1,3
        elif Star_rating == "3-4":
            Star_min,Star_max = 3,4
        else:
            Star_min,Star_max = 4,5
        
        #Applying filter    
        fliter = f'''SELECT*FROM redbus_details.bus_routes
            WHERE Busroutes = "{Redbus}"
            HAVING Price BETWEEN {Cost_min} AND {Cost_max}
            AND Star_rating BETWEEN {Star_min} and {Star_max}
            AND {Seat} ORDER BY Price 
         
            '''
        
        mycursor.execute(fliter)
        get_info = mycursor.fetchall()
        con.close()
        
        Information = pd.DataFrame(get_info, columns=["ID","Busname","Bustype","Busroutes","Departing_time",
                  "Duration","Reaching_time","Star_rating","Price","Seats_available","buslink"])
        
        return Information
    
    Calling_Information = filter_for_bus(Bus_type,Bus_fare,Bus_rating)
    st.dataframe(Calling_Information)    
    
    st.subheader('By seeing the available bus details kindly Enter the following Details to Book your tickets ')

    Name = st.text_input("Enter the Bus Name:")
    Type = st.text_input("Enter the Bus Type:")
    Route = st.text_input("Enter the Bus Route:")
    Time = st.time_input("Enter the Departing Time:")
    Passenger_Name = st.text_input("Passenger Name")

    if st.checkbox('Select here to confirm your tickets'):
        st.write('Your Ticket has been Confirmed,',Name,'bus,',Type,',Route:',Route,',Departing at',Time,',has been booked successfully by - ',Passenger_Name)
        if st.button('Submit'):
            st.image('C:/Users/new/Desktop/Redbus_Project/journey_1.jpg')
            st.balloons()  