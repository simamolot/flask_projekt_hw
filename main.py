from flask import Flask

app = Flask(__name__)


@app.route('/')
def homepage():
    return 'Hi, welcome to my new page!'


@app.route('/name/<string:user_name>')
def great(user_name):
    return f'Hello, your name is {user_name}'


if __name__ == '__main__':
    app.run(debug=True)
