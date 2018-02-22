import cherrypy
import sqlite3 as sql
import datetime

import jinja2, os
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')),extensions=['jinja2.ext.autoescape'])

DB = 'pokedex.sqlite'

class Website(object):
	@cherrypy.expose	# this line means that the following function is a page on the site that can be visited
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
	def about(self):
		""" the about page """

		template = JINJA_ENVIRONMENT.get_template('about.html')
		template_values = {
			'copyright': datetime.datetime.now().year }

		return template.render(template_values)

	def get_names(self,gen):
		""" function to get the names of the pokemon from a specific generation
			takes integer gen parameter for the generation which should be used
			returns list of pokemon names """
		names = []
		with sql.connect(DB) as cur:
			results = cur.execute( '''SELECT identifier FROM pokemon_species WHERE generation_id = ?''', (gen,) )
			names = [ row[0] for row in results ]	

		return names

	def get_generations(self):
		""" function to get a list of pokemon generations
			returns list of ints """

		generations = []
		with sql.connect(DB) as cur:
			results = cur.execute( '''SELECT DISTINCT generation_id FROM pokemon_species''' )
			generations = [ row[0] for row in results ]

		return generations

	@cherrypy.expose
	def generation(self,gen=1):
		""" generation page
			takes integer gen parameter for the generation which should be used """

		template = JINJA_ENVIRONMENT.get_template('generation.html')
		template_values = {
			'gen': int(gen), 
			'generations': self.get_generations() }

		# get a list of names from that generation and break it into chunks so it's easer to display
		names = self.get_names(gen)
		columns = 8

		template_values['names'] = [ names[i:i+columns] for i in range(0,len(names),columns) ] # chunk the list
		 
		return template.render(template_values)

if __name__ == '__main__':
	cherrypy.config.update( {'server.socket_host': '0.0.0.0'} ) # make it accesible from other machines 
	cherrypy.quickstart( Website() )
