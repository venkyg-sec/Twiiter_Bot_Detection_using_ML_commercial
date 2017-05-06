from flask import Flask
from flask import render_template, request, url_for, redirect
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def hello():
    if request.method=='POST':
        #text = request.form['fname']
        #processed_text = text.upper()
        return redirect(url_for('response'))
    else:
        return render_template('hello.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
@app.route('/response')
def response():
    return render_template('response.html')

if __name__ == '__main__':
    app.run()