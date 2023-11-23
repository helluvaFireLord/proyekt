#Импорт
from flask import Flask, render_template,request, redirect
#Подключение библиотеки баз данных
from flask_sqlalchemy import SQLAlchemy
from speach import speach
import random
app = Flask(__name__)
#Подключение SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Создание db
db = SQLAlchemy(app)
#Создание таблицы

class Card(db.Model):
    #Создание полей
    #id
    id = db.Column(db.Integer, primary_key=True)
    #Заголовок
    title = db.Column(db.String(100), nullable=False)
    #Описание
    subtitle = db.Column(db.String(300), nullable=False)
    #Текст
    text = db.Column(db.Text, nullable=False)

    #Вывод объекта и id
    def __repr__(self):
        return f'<Card {self.id}>'
    

#Задание №1. Создать таблицу User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)





@app.route("/random_fact")
def fact():
    random_fact = ["Помимо помощи борьбы с глобальным потеплением посадка деревьев полезна:\n - Улучшение качества воздуха: Посадка деревьев помогает очищать воздух от вредных частиц и загрязнений, таких как углекислый газ, пыль и аллергены. Это особенно важно в городах и промышленных зонах, где качество воздуха часто оставляет желать лучшего. \n - Защита почвы от эрозии: Деревья помогают сохранить плодородность почвы, предотвращая ее эрозию и выветривание.\n - Регулирование количества осадков: Деревья могут помочь контролировать количество осадков, поскольку они сохраняют влагу и предотвращают ее испарение.\n - Создание тени и прохлады: Деревья обеспечивают тень и прохладу, что делает их важными для создания комфортных условий для людей и животных.\n - Обеспечение продуктов питания и лекарств: Многие деревья производят съедобные фрукты и орехи, а также содержат лекарственные вещества, которые могут быть использованы для лечения различных заболеваний.\n - Привлечение дикой природы: Деревья являются жизненно важной частью среды обитания для многих видов животных, обеспечивая им укрытие, пищу и места для гнездования.",
                    "Помимо помощи борьбы с глобальным потеплением экономия энергии полезна:\n - Экономия денег: Экономия энергии позволяет сократить расходы на электричество, газ и другие виды топлива.\n - Сохранение природных ресурсов: Экономия энергии способствует сохранению природных ресурсов, таких как нефть, газ и уголь, которые являются исчерпаемыми.\n - Улучшение экологической ситуации: Экономия энергии снижает выбросы вредных веществ в атмосферу, что способствует улучшению экологической ситуации. \n - Снижение зависимости от импорта энергоносителей: Экономия энергии помогает снизить зависимость от импорта энергоносителей, что делает экономику более устойчивой."]

    return f'<p>{random.choice(random_fact)}</p>'





#Запуск страницы с контентом
@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            
            #Задание №4. Реализовать проверку пользователей
            users_db = User.query.all()
            for user in users_db:
                if form_login == user.login and form_password == user.password:
                    return redirect('/index')
            else:
                error = 'Неправильно указан пользователь или пароль'
                return render_template('login.html', error=error)

            
        else:
            return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        login = request.form['email']
        password = request.form['password']
        id = len(User.query.order_by(User.id).all())
        #Задание №3. Реализовать запись пользователей
        user = User(id=id, login=login, password=password)
        db.session.add(user)
        db.session.commit()

        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


#Запуск страницы с контентом
@app.route('/index')
def index():
    #Отображение объектов из БД
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

#Запуск страницы c картой
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

#Запуск страницы c созданием карты
@app.route('/create')
def create():
    return render_template('create_card.html')

#Форма карты
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        #Создание объкта для передачи в дб

        card = Card(title=title, subtitle=subtitle, text=text)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

@app.route('/voice')
def voices():
    try:
        text = speach()
    except:
        text = "Что-то пошло не так..."
    return render_template('create_card.html', text=text)



if __name__ == "__main__":
    app.run(debug=True)