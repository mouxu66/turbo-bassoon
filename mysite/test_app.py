from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World! 网站正常'

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)
