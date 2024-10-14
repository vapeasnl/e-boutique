from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/client')
def client():
    return render_template('client.html')
