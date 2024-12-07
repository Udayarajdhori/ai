from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # For session security

# Fake user database for demonstration
users = {
    "testuser": {"password": "testpassword"}
}

@app.route('/')
def home():
    if 'username' in session:
        # If user is logged in, redirect to chat
        return redirect(url_for('chat'))
    return redirect(url_for('login'))  # Otherwise, show login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate user
        if username in users and users[username]['password'] == password:
            session['username'] = username  # Save user in session
            return redirect(url_for('chat'))
        else:
            return "Invalid credentials, try again."

    return render_template('login.html')  # Show login page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match."
        if username in users:
            return "Username already exists."
        
        # Add user to "database"
        users[username] = {'password': password}
        return redirect(url_for('login'))  # Redirect to login after successful signup

    return render_template('signup.html')  # Show signup page

@app.route('/chat')
def chat():
    # If the user is not logged in and accesses the chat, show the login page
    if 'username' not in session and 'stay_logged_out' not in session:
        return redirect(url_for('login'))  # Restrict access if not logged in
    
    return render_template('chat.html')  # Show chat dashboard

@app.route('/logout')
def logout():
    session.pop('username', None)  # Clear user session
    session.pop('stay_logged_out', None)  # Clear stay_logged_out session flag
    return redirect(url_for('login'))  # Redirect to login

@app.route('/stayloggedout', methods=['POST'])
def stay_logged_out():
    # Set a flag in the session to indicate the user wants to access the chat while staying logged out
    session['stay_logged_out'] = True
    return redirect(url_for('chat'))  # Redirect to the chat page

if __name__ == '__main__':
    app.run(debug=True)
