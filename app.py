import tempfile
from flask import Flask, render_template, request, send_file

app = Flask(__name__, template_folder='./templates')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/osint', methods=['GET', 'POST'])
def osint():
    if request.method == 'GET':
        return render_template('osint.html', osint_result='GET')
    elif request.method == 'POST':
        print(request)
        if request.form['action'] == 'GENERATE':
            txt = tempfile.TemporaryFile()
            txt.write(b'123')
            txt.seek(0)
            return send_file(txt, as_attachment=True, attachment_filename='password.txt')
        else:
            data = {}
            for key in request.form:
                if key:
                    data[key] = [x.strip() for x in request.form[key].split(',')]
                else:
                    data[key] = []
            return render_template('osint.html', osint_result=data, data=data)

if __name__ == "__main__":
    app.run(port=9000)
