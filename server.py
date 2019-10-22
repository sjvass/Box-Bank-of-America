from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                    session, jsonify)

from boxsdk import Client, OAuth2

import os

# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['image_uploads']

    file_read = file.stream.read()

    #Get path to root of app
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    #save img
    destination = "/".join([APP_ROOT, file.filename])


    #create image file
    my_file = open(destination, 'wb')
    #write blob data to image file
    my_file.write(file_read)

    #close file
    my_file.close()

    # path = os.path.realpath(file.name)

    # print(path)
    print(file.filename)

    client = make_client()

    print(client)

    folder_id = '0'
    print(client.folder(folder_id))
    uploaded_file = client.folder(folder_id).upload(destination)

    os.remove(destination)
    
    return redirect('/')



# def upload_file(client):
#     root_folder = client.folder(folder_id='0')
#     file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
#     a_file = root_folder.upload(file_path, file_name='i-am-a-file.txt')
#     try:
#         print('{0} uploaded: '.format(a_file.get()['name']))
#     finally:
#         print('Delete i-am-a-file.txt succeeded: {0}'.format(a_file.delete()))


def make_client():

    auth = OAuth2(
        client_id='{CLIENT_ID}'.format(CLIENT_ID=os.environ.get('CLIENT_ID')),
        client_secret='{CLIENT_SECRET}'.format(CLIENT_SECRET=os.environ.get('CLIENT_SECRET')),
        access_token='{DEV_TOKEN}'.format(DEV_TOKEN=os.environ.get('DEV_TOKEN')),
    )
    client = Client(auth)

    user = client.user().get()
    print('The current user ID is {0}'.format(user.id))

    return client


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be5000 True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    # app.jinja_env.auto_reload = app.debug

    # connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')