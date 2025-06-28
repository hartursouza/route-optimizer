from flask import Blueprint, render_template, redirect, url_for, request

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verificação de login aqui
        return redirect(url_for('main.index'))
    return render_template('auth/login.html')
