from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura'

# Usuarios estáticos
USERS = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'operario': {'password': 'op456', 'role': 'operario'}
}

# Decorador para proteger rutas
def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = USERS.get(username)
        if user and user['password'] == password:
            session['user'] = username
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('operario'))
        else:
            error = 'Usuario o contraseña incorrectos.'
    return render_template('login.html', error=error)

@app.route('/admin')
@login_required(role='admin')
def admin():
    return render_template('admin.html')

@app.route('/operario')
@login_required(role='operario')
def operario():
    return render_template('operario.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
