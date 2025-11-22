from flask import Flask, request, render_template, url_for, redirect
import time

app = Flask(__name__)

# Simple in-memory app state. For production, persist this in a DB or cache.
app_state = {
    "running": False,
    "start_time": None,
    "last_elapsed": None,
}
task_name = []

@app.route("/home1")
def home1():
    return render_template(
        "home1.html",
        running=app_state["running"],
        last_elapsed=app_state.get("last_elapsed"),
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

    return redirect(url_for("x"))


@app.route("/stop", methods=["POST"])
def stop():
    global running, start_time, last_elapsed

    if running:
        running = False
        last_elapsed = time.time() - start_time
        # trigger your stop function
        on_stop()

    return redirect(url_for("simonsays"))

with app.test_request_context():
    print(url_for("static", filename="styles.css"))

tasks = [] 

@app.route("/taskinput")
def task_input():
    return render_template("task_input.html")


@app.route("/save_task", methods=["POST"])
def save_task():
    task = request.form.get("task")
    if task:
        tasks.append(task)
    # redirect to the dashboard to show the updated list
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", tasks=tasks)



if __name__ == "__main__":
    app.run(debug=True)
