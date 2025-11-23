from flask import Flask, request, render_template, url_for, redirect
import time
from datetime import date

app = Flask(__name__)

users = {
    "default": {
        "streak": 0,
        "health_points": 0,
        "last_completed_day": None
    }
}
daily_habits = [
    {"id": 1, "name": "Drink 1 Glass of Water"},
    {"id": 2, "name": "Sleep 8 Hours"},
    {"id": 3, "name": "Take a 5-Minute Walk"},
    {"id": 4, "name": "Stretch for 2 Minutes"}
]
completed_habits = set()


app_state = {
    "running": False,
    "start_time": None,
    "last_elapsed": None,
}

running = False
start_time = None
last_elapsed = None

tasks = []

def start_task(name):
    return None

def on_start():
    return None

def on_stop():
    return None


@app.route("/home1")
def home1():
    return render_template(
        "home1.html",
        running=app_state["running"],
        last_elapsed=app_state["last_elapsed"]
    )


@app.route("/home2", methods=["GET", "POST"])
def home2():
    name = None
    if request.method == "POST":
        name = request.form.get("task")
    return render_template("home2.html", name=name)


@app.route("/simonsays/")
def simonsays():
    return render_template("simonsays.html")


@app.route("/start", methods=["POST"])
def start():
    global running, start_time

    if not running:
        running = True
        start_time = time.time()
        start_task(task_name)
        on_start()

    return redirect(url_for("home2.html"))


@app.route("/stop", methods=["POST"])
def stop():
    global running, start_time, last_elapsed

    if running:
        running = False
        last_elapsed = time.time() - start_time
        on_stop()

    return redirect(url_for("stoppage.html"))


@app.route("/taskinput")
def task_input():
    return render_template("home1.html")


@app.route("/save_task", methods=["POST"])
def save_task():
    # Server-side validation: strip whitespace and only save non-empty tasks
    task_raw = request.form.get("task", "")
    task = task_raw.strip()
    if task:
        tasks.append(task)
    # If the input was empty or whitespace only, ignore it and redirect.
    return redirect(url_for("dashboard"))

@app.route("/complete_habit/<int:habit_id>", methods=["POST"])
def complete_habit(habit_id):
    user = "default"

    if habit_id not in completed_habits:
        completed_habits.add(habit_id)
        users[user]["health_points"] += 5  # reward for completing habits

    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    user = "default"
    return render_template(
        "dashboard.html",
        tasks=tasks,
        streak=users[user]["streak"],
        health_points=users[user]["health_points"],
        habits=daily_habits,
        completed=completed_habits
    )

if __name__ == "__main__":
    app.run(debug=True)
