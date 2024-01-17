# Задание
# Создать форму для регистрации пользователей на сайте.
# Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль"
# и кнопку "Зарегистрироваться". При отправке формы данные должны
# сохраняться в базе данных, а пароль должен быть зашифрован.

from flask import Flask, request, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm
from models import db, User
from hashlib import sha256


app = Flask(__name__)
app.config['SECRET_KEY'] = b'3a14d471e55647e23a764237c23536e8a106294a0e67de7bb07e9f1c37aab126'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = sha256(form.password.data.encode()).hexdigest()

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Ошибка! Такой email уже есть в базе', 'error')
        else:
            user = User(first_name=first_name, last_name=last_name, email=email, password=password)
            db.session.add(user)
            db.session.commit()

            flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('register'))

    return render_template('register.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)

