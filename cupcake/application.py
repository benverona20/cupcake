from flask import Flask, render_template, request, url_for, g
from cs50 import SQL
app = Flask(__name__)

db = SQL("sqlite:///cupcake.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/show", methods=['POST'])
def show():
    table = db.execute("SELECT * FROM 'cupcake'")
    return render_template("show.html", table = table)

@app.route("/insert", methods=['POST'])
def insert():
    return render_template("insert.html")

@app.route("/insert_res", methods=['POST'])
def insert_res():
    cake = request.form['cake']
    color = request.form['color']
    nice = request.form['nice']

    if cake or color or nice is not None:
        db.execute('INSERT INTO "cupcake" (cake, color, nice) VALUES(:cake, :color, :nice)', cake = cake, color = color, nice = nice)
        res = "SUCCESS"
    else:
        res = "FAILURE"
    return render_template("insert_res.html", res = res)

@app.route("/delete", methods=['POST'])
def delete():
    table = db.execute("SELECT * FROM 'cupcake'")
    return render_template("delete.html", table = table)

@app.route("/delete_res", methods=['POST'])
def delete_res():
    rowid = request.form['rowid']
    if rowid is not None:
        res = "SUCCESS"
        db.execute('DELETE FROM "cupcake" WHERE ("rowid"=:rowid);', rowid = rowid)
    else:
        res = "FAILURE"
    return render_template("delete_res.html", res = res)

@app.route("/update", methods=['POST'])
def update():
    table = db.execute("SELECT * FROM 'cupcake'")
    return render_template("update.html", table = table)

@app.route("/update_sel", methods=['POST'])
def update_sel():
    cake = db.execute("SELECT cake FROM cupcake WHERE rowid = :rowid", rowid = request.form['rowid'])
    return render_template("update_sel.html", cake = cake[0]["cake"], rowid = request.form['rowid'])

@app.route("/update_ent", methods=['POST'])
def update_ent():
    cupcake = {'number' : request.form['rowid']}
    cake = request.form.get('cake', None)
    if cake is not None:
        cake = int(cake)
        cupcake['cake'] = cake
    color = request.form.get('color', None)
    if color is not None:
        color = int(color)
        cupcake['color'] = color
    nice = request.form.get('nice', None)
    if nice is not None:
        nice = int(nice)
        cupcake['nice'] = nice
    return render_template("update_ent.html", cupcake = cupcake)

@app.route("/update_res", methods=['POST'])
def update_res():
    rowid = request.form['rowid']
    cake = request.form.get('cake', None)
    if cake is not None:
        db.execute('UPDATE cupcake SET cake = :cake WHERE rowid = :rowid', cake = request.form['cake'], rowid = rowid)
        res = "SUCCESS"
    color = request.form.get('color', None)
    if color is not None:
        db.execute('UPDATE cupcake SET color = :color WHERE rowid = :rowid', color = request.form['color'], rowid = rowid)
        res = "SUCCESS"
    nice = request.form.get('nice', None)
    if nice is not None:
        db.execute('UPDATE cupcake SET nice = :nice WHERE rowid = :rowid', nice = request.form['nice'], rowid = rowid)
        res = "SUCCESS"
    if nice and color and cake is None:
        res = "FAILURE"
    return render_template("update_res.html", res = res)