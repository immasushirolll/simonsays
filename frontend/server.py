from flask import Flask, request, render_template, url_for, redirect
import time
import asyncio
import threading
from script import get_ss
from state import SingletonState

app = Flask(__name__)

# Simple in-memory app state. For production, persist this in a DB or cache.
# app_state = {
#     "running": False,
#     "start_time": time.time(),
#     "last_elapsed": None,
# }

singleton = SingletonState()

task_name = []

async def periodic_task():
    print("Task started")
    while True:
        print('Task is running...')
        get_ss()    # dummy fcn to rep sshot logic
        await asyncio.sleep(5) # run every 5 seconds

def background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(periodic_task())

@app.route("/")
def home():
    # return "Flask is running!"
    running = singleton.get_state() == "on"
    return render_template("home.html")

@app.route("/goodluck", methods=["GET", "POST"])
def goodluck():
    name = None
    if request.method == "POST":
        name = request.form.get("task")
    return render_template("goodluck.html", name=name)

@app.route("/simonsays/")
def simonsays():
    return render_template("simonsays.html")


@app.route("/start", methods=["POST"])
def start():
    running = singleton.get_state()
    print(running)
    if singleton.get_state() == "off":
        singleton.turn_on()

    return redirect(url_for("dash"))


@app.route("/stop", methods=["POST"])
def stop():

    if singleton.get_state() == "on":
        singleton.turn_off()

    return redirect(url_for("goodluck"))

with app.test_request_context():
    print(url_for("static", filename="styles.css"))

tasks = [] 

#@app.route("/taskinput")
#def task_input():
#    return render_template("task_input.html")


@app.route("/save_task", methods=["POST"])
def save_task():
    task = request.form.get("task")
    if task and task not in tasks:
        tasks.append(task)
    # redirect to the dashboard to show the updated list
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", tasks=tasks)



if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=background_loop, args=(loop,))
    t.start()
    app.run(debug=True)
