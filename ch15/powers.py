from flask import Flask

app = Flask(__name__)

@app.route('/powers/<int:n>')
def powers(n):
    return ', '.join(str(2**i) for i in range(n))
