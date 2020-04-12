
"""
Travel Website Server
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
DATABASEURI = "postgresql://seh2209:2753@35.231.103.173/proj1part2"
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def index():
  cursor = g.conn.execute("SELECT name FROM city")
  cities = []
  for result in cursor:
    cities.append(str(result['name']))  
  cursor.close()
  context = dict(data = cities)
  return render_template("index.html", **context)

@app.route('/view_city/<name>')
def view_city(name=None):

    #get information about city
    cursor = g.conn.execute("SELECT name, weather, main_attraction FROM city WHERE name = '{}'".format(name))
    city = {}
    for result in cursor:
      city["name"] = str(result['name'])
      city["weather"] = str(result['weather'])
      city["main_attraction"] = str(result['main_attraction'])
    cursor.close()

    #get content titles about city
    cursor = g.conn.execute("SELECT title FROM about, city WHERE city.name = '{}' and about.place_id = city.place_id".format(name))
    content = []
    for result in cursor:
      content.append(str(result['title']))
    cursor.close()

    #get country city is in
    cursor = g.conn.execute("SELECT place.name FROM place, city, in_country WHERE city.name = '{}' AND in_country.country_id = place.place_id AND in_country.city_id = city.place_id".format(name))
    for result in cursor:
      city["country"] = str(result[0])
    cursor.close()
    context = dict(data = city, content = content)
    return render_template('view_city.html', **context)  


@app.route('/view_country/<name>')
def view_country(name=None):

    #get information about country
    cursor = g.conn.execute("SELECT place.place_id, gdp, population, crime_rate FROM place, country WHERE place.name = '{}' and country.place_id = place.place_id".format(name))
    country = {}
    for result in cursor:
      country["id"] = str(result[0])
      country["name"] = str(name)
      country["gdp"] = str(result['gdp'])
      country["population"] = str(result['population'])
      country["crime_rate"] = str(result['crime_rate'])
    cursor.close()

    #get content titles about country
    cursor = g.conn.execute("SELECT title FROM about, country, place WHERE place.name = '{}' and about.place_id = country.place_id and place.place_id = country.place_id".format(name))
    content = []
    for result in cursor:
      content.append(str(result['title']))
    cursor.close()

    #get cities in country
    cursor = g.conn.execute("SELECT DISTINCT city.name from city, country, in_country, place where place.name = '{}' and place.place_id = in_country.country_id and in_country.city_id = city.place_id".format(name))
    cities = []
    for result in cursor:
      cities.append(str(result[0]))  
    cursor.close()

    #get continent country is in
    cursor = g.conn.execute("SELECT place.name from place, in_continent where in_continent.country_id = '{}' and place.place_id = in_continent.continent_id".format(country["id"]))
    for result in cursor:
      country["continent"] = str(result[0])
    cursor.close()

    context = dict(data = country, content = content, cities = cities)
    return render_template('view_country.html', **context) 

@app.route('/view_continent/<name>')
def view_continent(name=None):

    #get information about continent
    cursor = g.conn.execute("SELECT continent.place_id, area, north_south, east_west FROM place, continent WHERE place.name = '{}' and continent.place_id = place.place_id".format(name))
    continent = {}
    for result in cursor:
      continent["id"] = str(result[0])
      continent["name"] = str(name)
      continent["area"] = str(result['area'])
      continent["north_south"] = str(result['north_south'])
      continent["east_west"] = str(result['east_west'])
    cursor.close()

    #get content titles about continent
    cursor = g.conn.execute("SELECT title FROM about, continent, place WHERE place.name = '{}' and about.place_id = continent.place_id and place.place_id = continent.place_id".format(name))
    content = []
    for result in cursor:
      content.append(str(result['title']))
    cursor.close()
    
    #get countries in continent
    cursor = g.conn.execute("SELECT DISTINCT place.name from in_continent, place where place.place_id = in_continent.country_id and in_continent.continent_id = '{}'".format(continent['id']))
    countries = []
    for result in cursor:
      countries.append(str(result[0]))  
    cursor.close()
    context = dict(data = continent, content = content, countries = countries)
    return render_template('view_continent.html', **context) 

@app.route('/view_content/<title>')
def view_content(title=None):
  #get editor info
  cursor = g.conn.execute("SELECT name, YOE, education FROM editor, edits where edits.title = '{}' and edits.editor_id = editor.editor_id".format(title))
  editor = {}
  for result in cursor:
    editor["name"] = str(result["name"])
    editor["yoe"] = str(result["yoe"])
    editor["education"] = str(result["education"])
  cursor.close()
  #decide if content is photo or article
  cursor = g.conn.execute("SELECT CASE WHEN EXISTS ( SELECT * FROM article WHERE title = '{}' )THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END".format(title))
  for result in cursor:
      n = result[0]
      print(str(n))
      
  if int(n) > 0: #content is article
    article = {}
    #get article information
    cursor = g.conn.execute("SELECT text, tag from article where title = '{}'".format(title))
    for result in cursor:
      article["title"] = str(title)
      article["tag"] = str(result['tag'])
      article["text"] = str(result['text'])
    cursor.close()
    #get author information
    cursor = g.conn.execute("SELECT name, bio, genre from writer, writes where writes.title = '{}' and writes.writer_id = writer.writer_id".format(title))
    writer = {}
    for result in cursor:
      writer["name"] = str(result['name'])
      writer["bio"] = str(result["bio"])
      writer["genre"] = str(result["genre"])
    cursor.close()
    context = dict(article = article, writer = writer, editor = editor)
    return render_template('view_article.html', **context) 
  else: #content is a photo
    #get photo information
    photo = {}
    cursor = g.conn.execute("SELECT size, resolution, type, copyright, url from photo where title = '{}'".format(title))
    for result in cursor:
      photo["title"] = str(title)
      photo["size"] = str(result['size'])
      photo["resolution"] = str(result['resolution'])
      photo["type"] = str(result['type'])
      photo["copyright"] = str(result["copyright"])
      photo["url"] = str(result['url'])
    cursor.close()
    #get photographer information
    cursor = g.conn.execute("SELECT name, bio, company, known_for from photographer, takes where takes.title = '{}' and takes.photographer_id = photographer.photographer_id".format(title))
    photographer = {}
    for result in cursor:
      photographer["name"] = str(result['name'])
      photographer["bio"] = str(result["bio"])
      photographer["company"] = str(result["company"])
      photographer["known_for"] = str(result["known_for"])
    cursor.close()
    context = dict(photo = photo, photographer = photographer, editor = editor)
    return render_template('view_photo.html', **context)

@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('q')
    s1 = search_term.lower()
    s2 = s1.title()
    cursor = g.conn.execute("SELECT name FROM city WHERE name LIKE '%%{}%%' OR name LIKE '%%{}%%'".format(s1,s2))
    cities = []
    for result in cursor:
      cities.append(str(result[0]))  
    cursor.close()
    cursor = g.conn.execute("SELECT place.name FROM place, country WHERE place.name LIKE '%%{}%%' OR name Like '%%{}%%' and country.place_id = place.place_id".format(s1, s2))
    countries = []
    for result in cursor:
      countries.append(str(result[0]))  
    cursor.close()
    context = dict(cities = cities, countries = countries)
    return render_template('search_results.html', **context)


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
