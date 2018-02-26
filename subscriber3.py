import paho.mqtt.client as mqtt
import datetime
import sqlite3 as sql

DB = 'danielnodedb.db'

def on_connect( client, userdata, flags, rc ):
#""" callback function for client connection """
    client.subscribe( "davedata/outside/temp")
    client.subscribe( "davedata/outside/humidity")

def on_message( client, userdata, msg ):
#""" callback function for messages received """
    print( "Topic: {}, Message: {}".format(msg.topic, msg.payload) )
    
    sensor = None
    if "temp" in msg.topic:
        sensor = "temp"
    elif "humidity" in msg.topic:
        sensor = "humidity"
        
    value = float(msg.payload)
    now = datetime.datetime.now()
        
    if sensor:
        with sql.connect(DB) as cur:
            cur.execute("""INSERT INTO sensordata VALUES(?, ?, ?);""", (sensor,value,now) )
          
    
    
def value(self):
    with sql.connect(DB) as cur:
        cur = con.cursor(DB)
        cur.execute("""INSERT INTO sensordata VALUES(?, ?, ?);""", (sensor,value,now) )
        
        if "light" in topic:
            sensor = "light"
    now = datetime.dateime.now().timetuple()
    #f = open("results.txt", "a")
    #print( "Topic: {}, Message: {}".format(msg.topic, msg.payload), file=f )
    #file.write("results.txt", "Danielnode/#")
   # f.close()
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect( "iot.eclipse.org" ) # test broker
client.loop_forever()
