from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

# Initialize Flask app
# template_folder='template' tells Flask to look in your specific folder name
app = Flask(__name__, template_folder='template')

# Connect to MongoDB
# Make sure your MongoDB is running on the default port 27017
client = MongoClient('mongodb://localhost:27017/')

# Create (or access) a database called 'user_database'
db = client['user_database']

# Create (or access) a collection called 'users'
users_collection = db['users']


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get data from the form
        user_name = request.form.get('name')
        user_domain = request.form.get('domain')

        if user_name and user_domain:
            # Insert the data into MongoDB
            existing_user = users_collection.find_one({'name': user_name, 'domain': user_domain})

            if existing_user:
                return f"Welcome back, {user_name} from {user_domain}!"
            else:
                users_collection.insert_one({'name': user_name, 'domain': user_domain})
                return "Data saved to MongoDB successfully! You are now logged in."

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)