# Создать страницу, на которой будет форма для ввода имени и электронной почты,
# при отправке которой будет создан cookie-файл с данными пользователя, а также
# будет произведено перенаправление на страницу приветствия, где будет отображаться
# имя пользователя. На странице приветствия должна быть кнопка «Выйти», при нажатии
# на которую будет удалён cookie-файл с данными пользователя и произведено
# перенаправление на страницу ввода имени и электронной почты.


from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/set_cookie', methods=['POST'])
def set_cookie():
    name = request.form['name']
    email = request.form['email']
    response = make_response(redirect('/greet'))
    response.set_cookie('name', name)
    response.set_cookie('email', email)
    return response

@app.route('/greet')
def greet():
    name = request.cookies.get('name')
    email = request.cookies.get('email')
    if name and email:
        return render_template('hello.html', name=name)
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie('name')
    response.delete_cookie('email')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
