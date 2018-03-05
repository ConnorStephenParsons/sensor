import cherrypy
import sqlite3 as sql
import datetime

import jinja2, os
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')),extensions=['jinja2.ext.autoescape'])

DB = 'danielnodedb.db'

class Website(object):
    @cherrypy.expose    # this line means that the following function is a page on the site that can be visited
    def index(self):
        """ index is the default page that you get if you just enter the url and nothing else """
        page = '''
            <html>
                <title>Simple pokemon</title>
                <body>
                    Welcome to the very simple pokemon webpage<br/>
                    <br>
                    <a href="generation">Generations</a><br/>
                    <a href="about">About</a>
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
        return "<html>"+xy_chart.render().decode()+"</html>"

    @cherrypy.expose
    def about(self):
        """ the about page """

        template = JINJA_ENVIRONMENT.get_template('about.html')
        template_values = {
            'copyright': datetime.datetime.now().year }

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

    @cherrypy.expose
    def generation(self,gen=1):
        """ generation page
            takes integer gen parameter for the generation which should be used """
        
        template = JINJA_ENVIRONMENT.get_template('generationTest.html')
        template_values = {
            'gen': int(gen), 
            'names': self.get_timestamp() }

        # get a list of names from that generation and break it into chunks so it's easer to display
        names = self.get_value()
        columns = 8

        template_values['value'] = [ names[i:i+columns] for i in range(0,len(names),columns) ] # chunk the list
         
        return template.render(template_values)

if __name__ == '__main__':
    cherrypy.config.update( {'server.socket_host': '0.0.0.0'} ) # make it accesible from other machines 
    cherrypy.quickstart( Website() )
