from flask import Flask, render_template
from data import db_session
import DBwork as dbw

app = Flask(__name__)
app.config['SECRET_KEY'] = 'robl_secret_key'


"""@app.route('/')
def index():
    # date_d = как-то получаем дату составления запроса
    # us_id_to = id пользователя которому отображаем
    db_session.global_init("db/transactions.db")
    db_sess = db_session.create_session()
    unpaid_users = dbw.get_unpaid_users(date_d, us_id_to)  # получаем список кортежей
    paid_users = dbw.get_paid_users(date_d, us_id_to)  # тоже список кортежей , поз[0]=tg_tag, поз[1]=debt
    return render_template('index.html', unpaid_users=unpaid_users, paid_users=paid_users)"""


if __name__ == '__main__':
    db_session.global_init("db/transactions.sqlite")
    app.run()
