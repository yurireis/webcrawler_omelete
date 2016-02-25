#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pymongo
import urllib2
import re
from bs4 import BeautifulSoup, UnicodeDammit


# Conectando ao MongoDB
try:
    conn=pymongo.MongoClient()
    print "\nConectado com sucesso ao MongoDB!"
except pymongo.errors.ConnectionFailure, e:
   print "\nNão foi possível conectar ao MongoDB: %s" % e 

db = conn.mydb

for cont in range(1, 3):
	url = "http://omelete.uol.com.br/busca/?q=the+walking+dead"
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	documento = opener.open(url)
	documento = UnicodeDammit.detwingle(documento.read())
	soup = BeautifulSoup(documento)

	paginas = soup.body.find("div", {"class": "pagination"})
	paginas = paginas.findAll('a')
	paginas = paginas[len(paginas)-2]
	paginas = paginas.text
	paginas = int(paginas)

	i = 0
	for i in range(1, paginas+1):
		if(i==1):
			url = "http://omelete.uol.com.br/busca/?q=the+walking+dead"
		else:
			url = "http://omelete.uol.com.br/busca/?page="+ str(i) +"&q=the%20walking%20dead"
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		documento = opener.open(url)
		documento = UnicodeDammit.detwingle(documento.read())
		soup = BeautifulSoup(documento)
		print url
		print soup.title.string

		for x in soup.body.findAll('a', href=re.compile('/walking-dead/')):
			numComentarios = 0

			url2 = "http://omelete.uol.com.br"+ x['href']
			print url2

			opener2 = urllib2.build_opener()
			opener2.addheaders = [('User-agent', 'Mozilla/5.0')]
			documento2 = opener.open(url2)
			documento2 = UnicodeDammit.detwingle(documento2.read())
			soup2 = BeautifulSoup(documento2)

			print soup2.title.string

			for comentarios in soup2.findAll('div', id=re.compile('div_comentario_')):
				comentario = comentarios.find("div", {"id": "HOTWordsTxt"})
				if comentario != None:
					print comentario.text
					curtidas = comentarios.find("span", {"class": "comentario-opiniao"})
					print curtidas.text
					numComentarios += 1
					usuario = comentarios.find('a')
					print usuario.text
					dado = {'url': url2, 'comentario':  comentario.text, 'curtidas': int(curtidas.text),'usuario': usuario.text}
					db.comentario.save(dado)
			print numComentarios
			dado = {'_id': url2, 'titulo': soup2.title.string, 'numComentarios': numComentarios}
			db.pagina.save(dado)



