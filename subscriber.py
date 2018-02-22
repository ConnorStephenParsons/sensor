import paho.mqtt.client as mqtt

def on_connect( client, userdata, rc ):
#""" callback function for client connection """
    client.subscribe( "Danielnode")

def on_message( client, userdata, msg ):
#""" callback function for messages received """
    print( "Topic: {}, Message: {}".format(msg.topic, msg.payload) )
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect( "iot.eclipse.org" ) # test broker
    client.loop_forever()
