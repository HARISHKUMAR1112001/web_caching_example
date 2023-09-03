# import time
# from flask import Flask, jsonify
import hashlib
from flask_cors import CORS  # Import Flask-CORS

# app = Flask(__name__)

# Enable CORS for all routes
# CORS(app)

# @app.route('/api/data')
# def get_data():
#     # Simulate data that might change over time
#     data = {'message': 'Hello, World!', 'timestamp': int(time.time())}

#     # Return the data as JSON with a Cache-Control header
#     response = jsonify(data)
#     response.headers['Cache-Control'] = 'public, max-age=60'
#     return response

# if __name__ == '__main__':
#     app.run()

from flask import Flask, jsonify, Response, request
import os
import time
import random
import hashlib

app = Flask(__name__)

CORS(app)

image_dir = 'images'

@app.route('/api/images')
def get_image_list():
    
    image_filenames = [filename for filename in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, filename))]

    image_filenames_hash = hashlib.md5("".join(image_filenames).encode()).hexdigest()

    cache_control = 'public, max-age=1'  # 1 minute

    expires = int(time.time()) + 60  # 1 minute

    etag = f'"{image_filenames_hash}"'
    
    print(etag, "etag>>>>>>>>>>>>>>>")

    if request.headers.get('If-None-Match') == etag:
        return Response(status=304)

    response = jsonify(image_filenames)
    response.headers['Cache-Control'] = cache_control
    response.headers['Expires'] = expires
    response.headers['ETag'] = etag

    return response

if __name__ == '__main__':
    app.run()


