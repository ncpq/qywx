from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return 'hello world 20200706'

@app.route('/check/')
def check():
    return 'hello check'


if __name__ == '__main__':
    app.run()
