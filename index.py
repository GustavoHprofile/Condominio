from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/jesus', methods=['POST'])
def jesus():
    login = request.form.get('login')
    senha = request.form.get('senha')
    return render_template('resposta.html', login=login, senha=senha)

if __name__ == '__main__':
    app.run(debug=True)

