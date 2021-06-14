from flask import Flask, render_template, request, abort, redirect, url_for, make_response
from flask.helpers import url_for
from AzureDB import AzureDB
import pypyodbc

app = Flask(__name__)

connection = pypyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
  'Server=mateuszkuletaserver.database.windows.net;'
  'Database=mateuszkuletasql;'
  'uid=mateji;pwd=Kolkolkol11!') 
cursor = connection.cursor() 


@app.route('/index')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/v_timestamp')
def v_timestamp():
    cursor.execute("select * from data") 
    data = cursor.fetchall() 
    return render_template("example.html", value=data)

@app.route('/result')
def result():
    
    with AzureDB() as a:
        data = a.azureGetData()
        
    return render_template("result.html", data = data)

@app.route('/aboutme', methods =["GET", "POST"])
def aboutme():
    if request.method == "POST":
       first_name = request.form.get("name") 
       last_name = request.form.get("text") 
       cursor.execute("INSERT INTO data (name, text) VALUES(?, ?)", (first_name, last_name))
       connection.commit()
       return "Dodano opinię"
       
    return render_template("aboutme.html")

@app.route('/deleee', methods =["GET", "POST"])
def deleee():
    if request.method == "POST":
       first_name = request.form.get("name")
       cursor.execute('DELETE FROM data WHERE name=?', (first_name,))
       connection.commit()
       return "Usunięto wpis"
       
    return render_template("deleee.html")
    

@app.route("/gallery")
def gallery():
    return app.send_static_file('gallery.html')


@app.route("/contact")
def contact():
    return app.send_static_file('contact.html')

@app.route('/error_denied')
def error_denied():
    abort(401)

@app.route('/error_internal')
def error_internal():
    return render_template('template.html', name='ERROR 505'), 505

@app.route('/error_not_found')
def error_not_found():
    response = make_response(render_template('template.html', name='ERROR 404'), 404)
    response.headers['X-Something'] = 'A value'
    return response

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.route("/guestbook")    
def guestbook():
    with AzureDB() as a:
        data = a.azureGetData()
    return render_template("guestbook.html", data = data)
    

@app.route("/process", methods=["POST"])   
def process(): 
    name = request.form['name']
    text = request.form['text']

    with AzureDB() as b:
        b.azureAddData(name,text)
        data = b.azureGetData()

    return redirect(url_for('guestbook'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)