from flask import Flask, jsonify, request, abort, render_template
# conditional import to make it work in unit tests
try:
	from tctl_handler import TctlHandler
except ImportError:
	from .tctl_handler import TctlHandler
import os


app = Flask(__name__)
tctlhandler = TctlHandler()

# Setting debug mode base on the environment
DEBUG_MODE = os.getenv('DEBUG', False)
# API version
api_version = 'v1.0'
# API url
api_url = "/api/{}/".format(api_version)


@app.route(api_url + "tokens", methods=['GET'])
def get_tokens():
	"""
	Return all current tokens.
	"""
	return jsonify(tctlhandler.get_all_tokens())


@app.route(api_url + "token", methods=['POST'])
def create_token():
	"""
	Create single token for adding nodes to the cluster.
	"""
	try:
		print(request.data)
		return jsonify(tctlhandler.create_token(request)), 202
	except RuntimeError as e:
		abort(400, str(e))


@app.route("/", methods=['GET'])
def index():
	"""
	Load home page.
	"""
	return render_template('index.html')


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=DEBUG_MODE)
