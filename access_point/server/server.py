from flask import Flask , render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/install')
def install():
    return 'starting the installation script'

if __name__ == '__main__':
    app.run(debug=False) # to allow the server to be accessible by any device on the network/access point
