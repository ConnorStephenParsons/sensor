import cherrypy
import sqlite3 as sql
import datetime, pygal


import jinja2, os
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')),extensions=['jinja2.ext.autoescape'])

DB = 'danielnodedb.db'

class Website(object):
    @cherrypy.expose    # this line means that the following function is a page on the site that can be visited
    def index(self):
        """ index is the default page that you get if you just enter the url and nothing else """
        page = '''
       <!DOCTYPE html>
<html>
    <head>
       <title>ALL Project</title>
       <link href="static/home.css" type="text/css" rel="stylesheet">
    </head>
    <body>
    <div id="Title">
        <h1>ALL Project</h1>
    </div>
    <table id="Nav">
        <tr>
           <td onclick="document.location='home2';">Home</td>
            <td onclick="document.location='gravity';">Gravity</td>
            <td onclick="document.location='light';">Light Intesity</td>
            <td onclick="document.location='pressure';">Pressure</td>
            <td onclick="document.location='lineara';">Linear Acceleration</td>
            <td onclick="document.location='gyroscope';">Gyroscope</td>
        </tr>
        
       
    </table>
    <h1 id="sensor">Home>></h1>
    <p style = "padding: 0px 0px 0px 80px">On each of the pages above are readings obtained by the Sensor Node Free App available on the Google Play Store. The data is being streamed from a Samsing Galaxy S7 Edge.</p>
    <p style = "padding: 0px 0px 0px 80px">Data on each graph is displayed based on the most recent readings. Five sensors are available and one can be viewed on each of the pages on this website.</p>
  
  </body>
</html>'''
        return page
    
    @cherrypy.expose
    def chart(self):
        from math import cos
        import pygal
        xy_chart = pygal.XY()
        xy_chart.title = 'XY Cosinus'
        xy_chart.add('x = cos(y)', [(cos(x / 10.), x / 10.) for x in range(-50, 50, 5)])
        xy_chart.add('y = cos(x)', [(x / 10., cos(x / 10.)) for x in range(-50, 50, 5)])
        xy_chart.add('x = 1',  [(1, -5), (1, 5)])
        xy_chart.add('x = -1', [(-1, -5), (-1, 5)])
        xy_chart.add('y = 1',  [(-5, 1), (5, 1)])
        xy_chart.add('y = -1', [(-5, -1), (5, -1)])
        return xy_chart.render().decode()

    @cherrypy.expose
    def home2(self):
        """ the home page """

        template = JINJA_ENVIRONMENT.get_template('home2.html')
        template_values = { }
        return template.render(template_values)
      
    @cherrypy.expose
    def gravity(self):
        """ the gravity page """

        from datetime import datetime, timedelta
        date_chart = pygal.DateTimeLine(x_label_rotation=20)
        mydata = self.get_data("gravity")
        print(mydata)
        date_chart.add("Gravity", mydata)
        output = date_chart.render().decode()
              
        template = JINJA_ENVIRONMENT.get_template('gravity.html')
        template_values = {"graph":output }
        return template.render(template_values)
      
    def get_data(self,sensor):
      data = []
      with sql.connect(DB) as cur:
            results = cur.execute('''SELECT datetime, value FROM sensordata WHERE lower(name) = ?''', (sensor,))
           
            week = datetime.datetime.now()-datetime.timedelta(days=7)
            temp = [(datetime.datetime.strptime(row[0],"%Y-%m-%d %H:%M:%S.%f"),float(row[1])) for row in results]
            for row in temp:
              if row[0] > week:
                data.append(row)
             
      return data
    
    def get_data_upper(self,sensor):
      data = []
      with sql.connect(DB) as cur:
          results = cur.execute('''SELECT datetime, value FROM sensordata WHERE name = ?''', (sensor,))
           
          week = datetime.datetime.now()-datetime.timedelta(days=7)
          temp = [(datetime.datetime.strptime(row[0],"%Y-%m-%d %H:%M:%S.%f"),float(row[1])) for row in results]
          for row in temp:
              if row[0] > week:
                data.append(row)
             
      return data
      
    def get_gravity(self):
        """ returns gravity data """
        gravity_data = []
        with sql.connect(DB) as cur:
            results = cur.execute('''SELECT datetime, value FROM sensordata WHERE lower(name) = "gravity"''')
           
            week = datetime.datetime.now()-datetime.timedelta(days=7)
            temp = [(datetime.datetime.strptime(row[0],"%Y-%m-%d %H:%M:%S.%f"),float(row[1])) for row in results]
            for row in temp:
              if row[0] > week:
                gravity_data.append(row)
             

            

            
        return gravity_data
     
    def get_light(self):
        """ returns light data """
        light_data = []
        with sql.connect(DB) as cur:
            results = cur.execute('''SELECT value , datetime FROM sensordata WHERE name = "light"''') #Correct other functions to this syntaxgravity_data = [row for row in results]
            light_data = [row for row in results]
            
        return gravity_data
      
    def get_lineara(self):
        """ returns linear acceleration data """
        lineara_data = []
        with sql.connect(DB) as cur:
            results = cur.execute('''SELECT value, datetime FROM sensordata WHERE name = "LinearAcceleration"''')
            lineara_data = [row for row in results]
        
        return lineara_data
      
    def get_percentage(self):
        """ returns battery percentage data """
        percentage_data = []
        with sql.connect(DB) as cur:
            results = cur.execute('''SELECT value, datetime FROM sensordata WHERE name = "percentage"''')
            percentage_data = [row for row in results]
        
        return percentage_data
    
    def accelerometer(self):
        """ return accelerometer data """
        accelerometer_data = []
        with sql.connect(DB) as cur:
            results = cur.execute('''SELECT value, datetime FROM sensordata WHERE name = "accelerometer"''')
            accelerometer_data = [row for row in results]
        
        return accelerometer_data
    
    def get_percentage(self):
        """ returns battery percentage data """
        percentage_data = []
        with sql.connect(DB) as cur:
            results = cur.execute('''SELECT value, datetime FROM sensordata WHERE name = "percentage"''')
            percentage_data = [row for row in results]
        
        return percentage_data
    
    def get_percentage(self):
        """ returns noise data """
        noise_data = []
        with sql.connect(DB) as cur:
            results = cur.execute('''SELECT value, datetime FROM sensordata WHERE name = "noise"''')
            noise_data = [row for row in results]
        
        return noise_data
    
    @cherrypy.expose
    
    def light(self):
        """ the gravity page """
        from datetime import datetime, timedelta
        date_chart = pygal.DateTimeLine(x_label_rotation=20)
        mydata = self.get_data_upper("LightIntensity")
        print(mydata)
        date_chart.add("LightIntensity", mydata)
        output = date_chart.render().decode()
              
        template = JINJA_ENVIRONMENT.get_template('light.html')
        template_values = {"graph":output }
        return template.render(template_values)
     
    @cherrypy.expose
    def gyroscope(self):
        """ the gravity page """
        from datetime import datetime, timedelta
        date_chart = pygal.DateTimeLine(x_label_rotation=20)
        mydata = self.get_data_upper("Gyroscope")
        print(mydata)
        date_chart.add("Gyroscope", mydata)
        output = date_chart.render().decode()
              
        template = JINJA_ENVIRONMENT.get_template('gyroscope.html')
        template_values = {"graph":output }
        return template.render(template_values)
     
    @cherrypy.expose
    def lineara(self):
        """ the Linear Acceleration page """

        from datetime import datetime, timedelta
        date_chart = pygal.DateTimeLine(x_label_rotation=20)
        mydata = self.get_data_upper("Accelerometer")
        print(mydata)
        date_chart.add("Linear Acceleration", mydata)
        output = date_chart.render().decode()
              
        template = JINJA_ENVIRONMENT.get_template('lineara.html')
        template_values = {"graph":output }
        return template.render(template_values)
 
    @cherrypy.expose
    def pressure(self):
        """ the pressure page """

        from datetime import datetime, timedelta
        date_chart = pygal.DateTimeLine(x_label_rotation=20)
        mydata = self.get_data_upper("Pressure")
        print(mydata)
        date_chart.add("Pressure", mydata)
        output = date_chart.render().decode()
              
        template = JINJA_ENVIRONMENT.get_template('pressure.html')
        template_values = {"graph":output }
        return template.render(template_values)

    def get_timestamp(self):
        """ function to get the names of the pokemon from a specific generation
            takes integer gen parameter for the generation which should be used
            returns list of pokemon names """
        timestamp = []
        with sql.connect(DB) as cur:
            results = cur.execute( '''SELECT * FROM sensordata''' )
            timestamp = [ row for row in results ]    

        return timestamp

    def get_value(self):
        """ function to get a list of pokemon generations
            returns list of ints """
        
        #return [[10,1],[20,2],[30,3],[40,4],[50,5]]

        value = []
        with sql.connect(DB) as cur:
            results = cur.execute( '''SELECT * FROM sensordata''' )
            value = [ row[0] for row in results ]

        return value

    
if __name__ == '__main__':
    w = Website()
    print(w.get_gravity()) 
    
    cherrypy.config.update( {'server.socket_host': '0.0.0.0' } )
    conf = {'/static':{'tools.staticdir.on':True,
                      'tools.staticdir.dir':"/home/codio/workspace/static"}} # make it accesible from other machines 
    cherrypy.quickstart( Website(), '/', config=conf )
