from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work
from bson.errors import InvalidId # For catching InvalidId exception for ObjectId
import os
from prometheus_client import make_wsgi_app, Counter, Histogram, start_http_server, Gauge
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import time

# mongodb_host = os.environ.get('MONGO_HOST', 'mongo')
# mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
mongodb_uri = os.environ.get('MONGO_URI', 'localhost')
client = MongoClient(mongodb_uri) #Configure the connection to the database
db = client.todo_app_db #Select the database
todos = db.todo #Select the collection

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})



REQUEST_HEALTH_COUNT = Counter(
    'app_request_health_count',
    'Application Request Count',
    ['method', 'endpoint', 'http_status']
)
REQUEST_HEALTH_LATENCY = Histogram(
    'app_request_health_latency',
    'Application Request Latency',
    ['method', 'endpoint']
)
REQUEST_HEALTH_GAUGE = Gauge(
    'app_request_health_gauge',
	'Application Request Gauge',
	['method', 'endpoint']
)


title = "Yout TaskList"
heading = "Task List"
#modify=ObjectId()

def redirect_url():
	return request.args.get('next') or \
		request.referrer or \
		url_for('index')

@app.route("/list")
def lists ():
	#Display the all Tasks
	todos_l = todos.find()
	a1="active"
	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/")
@app.route("/uncompleted")
def tasks ():
	#Display the Uncompleted Tasks
	todos_l = todos.find({"done":"no"})
	a2="active"
	return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)


@app.route("/completed")
def completed ():
	#Display the Completed Tasks
	todos_l = todos.find({"done":"yes"})
	a3="active"
	return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)

@app.route("/done")
def done ():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		todos.update_one({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		todos.update_one({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir=redirect_url()	# Re-directed URL i.e. PREVIOUS URL from where it came into this one

#	if(str(redir)=="http://localhost:5000/search"):
#		redir+="?key="+id+"&refer="+refer

	return redirect(redir)

#@app.route("/add")
#def add():
#	return render_template('add.html',h=heading,t=title)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	todos.insert_one({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	todos.delete_one({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	id=request.values.get("_id")
	todos.update_one({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})
	return redirect("/")

@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(refer=="id"):
		try:
			todos_l = todos.find({refer:ObjectId(key)})
			if not todos_l:
				return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading,error="No such ObjectId is present")
		except InvalidId as err:
			pass
			return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading,error="Invalid ObjectId format given")
	else:
		todos_l = todos.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

@app.route("/about")
def about():
	return render_template('credits.html',t=title,h=heading)

@app.route("/health")
def health ():
    start_time = time.time()
    REQUEST_HEALTH_COUNT.labels('GET', '/health', 200).inc()
    REQUEST_HEALTH_GAUGE.labels('GET', '/health').set(1)
    REQUEST_HEALTH_LATENCY.labels('GET', '/health').observe(time.time() - start_time)
    
    return("TO-DO APP IS HEALTHY")

@app.route("/ready")
def ready ():
    return("TO-DO APP IS READY TO SERVE")

if __name__ == "__main__":
	env = os.environ.get('FLASK_ENV', 'development')
	port = int(os.environ.get('PORT', 5050))
	debug = False if env == 'production' else True
	app.run(debug=True)
	app.run(port=port, debug=debug)
	# Careful with the debug mode..
