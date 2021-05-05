from flask import Flask, render_template

app = Flask(__name__)


@app.route('/modais')
def teste():
    return render_template('cadastro_produto.html')


app.run()
