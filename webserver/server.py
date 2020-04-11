
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
    cursor = g.conn.execute("SELECT gdp, population, crime_rate FROM place, country WHERE place.name = '{}' and country.place_id = place.place_id".format(name))
    country = {}
    for result in cursor:
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

    context = dict(data = country, content = content, cities = cities)
    return render_template('view_country.html', **context) 

@app.route('/view_content/<title>')
def view_content(name=None):

    return render_template('view_content.html', **context) 

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
