'''
Задание
Создать базовый шаблон для интернет-магазина, содержащий общие элементы
дизайна (шапка, меню, подвал), и дочерние шаблоны для страниц категорий
товаров и отдельных товаров. Например, создать страницы «Одежда», «Обувь»
и «Куртка», используя базовый шаблон.
'''

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def market():
    return render_template('home.html')


@app.route('/clothes/')
def clothes():
    return render_template('clothes.html')


@app.route('/shoes/')
def shoes():
    return render_template('shoes.html')


@app.route('/jackets/')
def jackets():
    return render_template('jackets.html')


if __name__ == '__main__':
    app.run(debug=True)