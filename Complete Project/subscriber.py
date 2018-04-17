import paho.mqtt.client as mqtt
import datetime
import sqlite3 as sql

DB = 'danielnodedb.db'

def on_connect( client, userdata, flags, rc ):
#""" callback function for client connection """
    client.subscribe( "Danielnode/livestream/LinearAcceleration")
    client.subscribe( "Danielnode/livestream/Gravity/z")
    client.subscribe( "Danielnode/livestream/Gyroscope/y")
    client.subscribe( "Danielnode/livestream/Accelerometer/z")     
    client.subscribe( "Danielnode/livestream/LightIntensity/#")
    client.subscribe( "Danielnode/livestream/Pressure/x")
     

def on_message( client, userdata, msg ):
#""" callback function for messages received """
    print( "Topic: {}, Value: {}".format(msg.topic, msg.payload) )
    
    sensor = None
    if "LinearAcceleration" in msg.topic: 
        sensor = "LinearAcceleration"
    elif "Gyroscope" in msg.topic:
        sensor = "Gyroscope" 
    elif "Accelerometer" in msg.topic:
        sensor = "Accelerometer" 
    elif "Pressure" in msg.topic:
        sensor = "Pressure"
    elif "LightIntensity" in msg.topic:
        sensor = "LightIntensity" 
    elif "Gravity" in msg.topic:
        sensor = "Gravity"
    # LinearAcceleration, Gravity, Accelerometer, LightIntensity, noise need to be changd to the sensor nodes in the DB.     
        
    value = float(msg.payload)
    now = datetime.datetime.now()
        
    if sensor:
        with sql.connect(DB) as cur:
            cur.execute("""INSERT INTO sensordata VALUES(?, ?, ?);""", (sensor,value,now) )
          
    
#Need to work out if i actually need this    
def value(self):
    with sql.connect(DB) as cur:
        cur = con.cursor(DB)
        cur.execute("""INSERT INTO sensordata VALUES(?, ?, ?);""", (sensor,value,now) )
        
        #if "light" in topic:
            #sensor = "light"
    #now = datetime.dateime.now().timetuple()
    #f = open("results.txt", "a")
    #print( "Topic: {}, Message: {}".format(msg.topic, msg.payload), file=f )
    #file.write("results.txt", "Danielnode/#")
   # f.close()
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect( "iot.eclipse.org" ) # test broker
client.loop_forever()

#git status
#git add sunscriber3