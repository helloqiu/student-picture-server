from app import app
from flask.ext.script import Manager


#app.run(debug=True, host='0.0.0.0')
manager = Manager(app)
if __name__ == '__main__':
	manager.run()