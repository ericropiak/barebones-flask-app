
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return 'hi'


print('ayyy')

if __name__ == "__main__":
    app.run()