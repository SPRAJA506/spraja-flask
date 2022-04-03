from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='template')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employer2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class employer2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    contact = db.Column(db.String(100), nullable=True)
    mail = db.Column(db.String(100), nullable=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if request.method == "POST":
        try:
            name = request.form['name']
            address = request.form['address']
            contact = request.form['contact']
            mail = request.form['mail']
            data = employer2(name=name, address=address, contact=contact, mail=mail)
            db.session.add(data)
            db.session.commit()
            flash("add Successfully", "success")
        except:
            flash("add error", "danger")
        finally:
            return redirect(url_for("home"))
    return render_template('add_record.html')


@app.route('/view_record', methods=["GET", "POST"])
def view_record():
    if request.method == "GET":
        data = employer2.query.all()
        return render_template("view_record.html", data=data)


@app.route('/update_record/<string:id>', methods=["POST", "GET"])
def update_record(id):
    daat = employer2.query.get(id)
    if request.method == "GET":
        return render_template("update_record.html", data=daat)

    else:
        daat.name = request.form["name"]
        daat.address = request.form["address"]
        daat.contact = request.form["contact"]
        daat.mail = request.form["mail"]
        db.session.commit()

        return redirect(url_for("view_record"))

@app.route('/delete_record/<string:id>')
def delete_record(id):
    asd = employer2.query.get(id)
    db.session.delete(asd)
    db.session.commit()
    return redirect(url_for('view_record'))


if __name__ == '__main__':
    app.run(debug=True)
