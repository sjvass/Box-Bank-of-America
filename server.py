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

#main home route. Returns the index.html template
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


#upload route for handling uploads
@app.route('/upload', methods=['POST'])
def upload():

    #get image file from client
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

    # print(path)
    # print(file.filename)

    #set up box client
    client = make_client()

    # print(client)

    #store files in root folder of box account
    folder_id = '0'
    # print(client.folder(folder_id))
    #upload to box account using box SDK
    uploaded_file = client.folder(folder_id).upload(destination)

    # print('ID: {file_id}'.format(file_id=uploaded_file.id))

    #save file ID to session so it can be accessed later
    session['upload_id'] = uploaded_file.id

    #remove the file from the client
    os.remove(destination)
    
    return redirect('/')


#route handles dowloading file to preview submitted files
#Returns the file ID/name of the file on success or 0 on failure
@app.route('/download', methods=['GET', 'POST'])
def download():

    #Check that file id is in session
    if 'upload_id' in session.keys():
        client = make_client()
        file_id = session['upload_id']
        #get file from Box account using sdk
        box_file = client.file(file_id=file_id).get()
        #creates pdf file with name of file ID to store dowloaded file
        output_file = open('static/{file_id}.pdf'.format(file_id=file_id), 'wb')
        box_file.download_to(output_file)
        return jsonify({'success': file_id})
    else:
        #If there is no file ID, the call was unsucessful. Returns a 0
        return jsonify({'success': 0})


#sets up and returns Box client
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