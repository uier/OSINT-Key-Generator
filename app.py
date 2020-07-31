from flask import Flask, render_template, request
app = Flask(__name__, template_folder='./templates')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/gen', methods=['GET', 'POST'])
def gen():
    if request.method == 'GET':
        return render_template('gen.html', osint_result='GET')
    elif request.method == 'POST':
        name = [x.strip() for x in request.form['name'].split(',')]
        user_id = [x.strip() for x in request.form['id'].split(',')]
        email = [x.strip() for x in request.form['email'].split(',')]
        birth = [x.strip() for x in request.form['birth'].split(',')]
        phone = [x.strip() for x in request.form['phone'].split(',')]
        return render_template('gen.html', osint_result=request.form)


if __name__ == "__main__":
    app.run(port=9000)
