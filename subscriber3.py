import paho.mqtt.client as mqtt
import datetime
import sqlite3 as sql

DB = 'danielnodedb.db'

def on_connect( client, userdata, flags, rc ):
#""" callback function for client connection """
    client.subscribe( "Danielnode/livestream/LinearAcceleration")
    client.subscribe( "Danielnode/livestream/Gravity/z")
    client.subscribe( "Danielnode/livestream/Accelerometer/z")     
    client.subscribe( "Danielnode/livestream/LightIntensity/z")
    client.subscribe( "Danielnode/livestream/noise/decibels/z") 
     

def on_message( client, userdata, msg ):
#""" callback function for messages received """
    print( "Topic: {}, Message: {}".format(msg.topic, msg.payload) )
    
    sensor = None
    if "LinearAcceleration" in msg.topic: 
        sensor = "LinearAcceleration"
        
  
    elif "Accelerometer" in msg.topic:
        sensor = "Accelerometer" 
    elif "LightIntensity" in msg.topic:
        sensor = "LightIntensity" 
    elif "noise" in msg.topic:
        sensor = "noise"
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
