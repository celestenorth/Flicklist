from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template
from google.appengine.api import urlfetch
from django.utils import simplejson

class Movie(db.Model):                                                         
  Title = db.StringProperty(required=False)                                    
  Director = db.StringProperty(required=False)
  Year = db.StringProperty(required=False)                              

class MainHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render("templates/index.html", locals()))

  def post(self):
    title = self.request.get("title")
    director = self.request.get("director")
    year = self.request.get("year")
    movie = Movie(Title=title,Director=director,Year=year)
    movie.put()
    self.redirect("/list")

class ListHandler(webapp.RequestHandler):
  def get(self):
    peliculas=[]
    movies = Movie.all()
    order = self.request.get("order")
    if order:
        movies.order(order)
	movies.fetch(1000)
    for movie in movies:
		movie.url = 'http://www.deanclatworthy.com/imdb/?q='+ movie.Title.replace(' ', '+')
		result = urlfetch.fetch(movie.url)
		movie.result = simplejson.loads(result.content)
		peliculas.append(movie)
    self.response.out.write(template.render("templates/list.html", locals()))

def main():
  application = webapp.WSGIApplication([
      ('/', MainHandler),
      ('/list', ListHandler),
  ],debug=True)
  util.run_wsgi_app(application)
  
if __name__ == '__main__':
  main()
