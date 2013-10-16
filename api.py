# -*- coding: utf-8 -*- 
import cherrypy
import os.path
import urllib
import urllib2
import unicodedata
from xml.dom.minidom import parse, parseString

class Cursos(object):
	def index(self):

		url = 'http://api.iobconcursos.com'
		values = {'nome' : 'SEUNOME',
		          'key' : 'SUAKEY' }

		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		conteudo = response.read()

		diob = parseString(conteudo)
		tabela = ""
		link = ""
		conference=diob.getElementsByTagName('curso')
		for node in conference:
			for x in node.getElementsByTagName('titulo_curso'):
				texto = x.firstChild.nodeValue.encode('utf-8')
			for x in node.getElementsByTagName('url_compra'):
				link = x.firstChild.nodeValue.encode('utf-8')
			tabela = "%s<tr><td><a href='%s'>%s</a></td></tr>" %( tabela,link, texto)

		html = """ 
		<html>
		<head>
		<title>API IOB</title>
		<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
		<link rel="stylesheet" type="text/css" href="gumby/css/gumby.css"/>
		</head>
		<body>
		<div class="row">
		<h3>IOB Concursos</h3>
			<table class="striped rounded" id="tabela">
				<thead>
					<tr>
						<th class="text-center">Curso</th>
					</tr>
				</thead>
				<tbody>
					%s
				</tbody>
			</table>
		</div>
		<script type="text/javascript" src="gumby/js/libs/jquery-2.0.2.min.js"></script>
		<script type="text/javascript" src="gumby/js/libs/gumby.js"></script>
		</body>
		</html> """ % (tabela)
		return html


	index.exposed = True

### RUN ###

if __name__ == '__main__':
	current_dir = os.path.dirname(os.path.abspath(__file__))
	# Set up site-wide config first so we get a log if errors occur.
	cherrypy.config.update({'environment': 'production',
	'log.error_file': 'site.log',
	'log.screen': True})

	conf = {'/gumby': {'tools.staticdir.on': True,
	'tools.staticdir.dir': os.path.join(current_dir, 'gumby')
	}}
	cherrypy.config.update({'server.socket_host': '127.0.0.1', 
                         'server.socket_port': 9999, 
                        })

	cherrypy.quickstart(Cursos(), '/', config=conf)
