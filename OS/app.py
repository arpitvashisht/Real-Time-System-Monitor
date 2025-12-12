from flask import Flask, render_template, jsonify
import psutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/data')
def get_data():
    # non-blocking snapshot (uses last computed value)
    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory().percent

    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            info = proc.info
            info['name'] = info.get('name') or ''
            info['cpu_percent'] = info.get('cpu_percent', 0.0)
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
    top10 = processes[:10]

    return jsonify({"cpu": cpu, "memory": mem, "processes": top10})

if __name__ == "__main__":
    app.run(debug=True)
