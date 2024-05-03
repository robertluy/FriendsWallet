from flask import Flask, render_template
from data import db_session
import DBwork as dbw
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'robl_secret_key'

"""@app.route("/profile")
def wallet__tg_tag:
    pass"""


@app.route('/')
def index():
    date_d = datetime(2024, 3, 3)
    us_id_to = 1
    unpaid_users = dbw.get_unpaid_users(date_d, us_id_to)  # получаем список кортежей
    paid_users = dbw.get_paid_users(date_d, us_id_to)  # тоже список кортежей , поз[0]=tg_tag, поз[1]=debt
    return render_template('index.html', us_name=dbw.get__tg_tag__from__us_id(us_id_to),
                           wallet=dbw.get__us_id__wallet(us_id_to), unpaid_users=unpaid_users, paid_users=paid_users)


if __name__ == '__main__':
    db_session.global_init("db/transactions.sqlite")
    '''dbw.add_user('@RealRoberL', '410403', '3120432')
    dbw.add_user('@RobotDolbaeb', '21311', '21321103')
    dbw.add_user('@NikitaDolbaeb', '32311', '53321103')
    timem = datetime(2024, 3, 3)
    dbw.add_friend(timem, 1, 2, 1000)
    dbw.add_friend(timem, 1, 3, 1000)
    dbw.upgrade_status_of_this_user(timem, 1, 2)
    print('unpaid:', dbw.get_unpaid_users(timem, 1))
    print('paid:', dbw.get_paid_users(timem, 1))
    print('debt of him: ', dbw.get_debt_of_this_user(timem, 1, 2))
    print(dbw.get__tg_tag__from__us_id(1))
    print(dbw.get__us_id__from__tg_tag('@RealRoberL'))
    print(dbw.get__tg_tag__from__tg_id('410403'))
    print(dbw.get__us_id__from__tg_id('410403'))
    print(dbw.get__us_id__wallet(1))'''
    app.run(host="127.0.0.1", port=8080)
