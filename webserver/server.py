
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

@app.route('/view/<name>')
def view(name=None):
    cursor = g.conn.execute("SELECT weather, main_attraction FROM city WHERE name = {}".format(name))
    city = {}
    for result in cursor:
      city["name"] = name
      city["weather"] = weather
      city["main_attraction"] = main_attraction
    cursor.close()
    context = dict(data = city)
    return render_template('view.html', **context)  


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
