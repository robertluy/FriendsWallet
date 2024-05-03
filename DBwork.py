from data import db_session
from data.users import User
from data.debts import Debts


def check_user(tg_tag):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.tg_tag == tg_tag).first()
    return user is None


def add_user(tg_tag, tg_id=' ', wallet=' '):  # добавление пользователя в таблицу
    if not check_user(tg_tag):
        pass
    else:
        user = User()
        user.tg_tag = tg_tag
        user.tg_id = tg_id
        user.wallet = wallet
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()


def add_friend(date_d, us_id_to, us_id, debt, status='no'):  # добавление друга-должника
    deb = Debts()
    deb.date_d = date_d
    deb.us_id_to = us_id_to
    deb.us_id = us_id
    deb.debt = debt
    deb.status = status
    db_sess = db_session.create_session()
    db_sess.add(deb)
    db_sess.commit()


def upgrade_status_of_this_user(date_d, us_id_to, us_id, new_status='yes'):  # обновление статуса должника
    db_sess = db_session.create_session()
    debt = db_sess.query(Debts).filter(Debts.date_d == date_d, Debts.us_id_to == us_id_to, Debts.us_id == us_id).first()
    if debt:
        debt.status = new_status
        db_sess.commit()
    else:
        print('no one users')


def get_unpaid_users(date_d, us_id_to):  # получение списка пользователей должников кортежом (tg_tag, долг)
    db_sess = db_session.create_session()
    unpaid_users = db_sess.query(User.tg_tag, Debts.debt). \
        join(Debts, Debts.us_id == User.us_id). \
        filter(Debts.date_d == date_d,
               Debts.us_id_to == us_id_to,
               Debts.status == 'no').all()
    sps = []
    for i in unpaid_users:
        sps.append(list(i))
    return sps


def get_paid_users(date_d, us_id_to):  # получение списка пользователей должников кортежом (tg_tag, долг)
    db_sess = db_session.create_session()
    unpaid_users = db_sess.query(User.tg_tag, Debts.debt). \
        join(Debts, Debts.us_id == User.us_id). \
        filter(Debts.date_d == date_d,
               Debts.us_id_to == us_id_to,
               Debts.status == 'yes').all()
    sps = []
    for i in unpaid_users:
        sps.append(list(i))
    return sps


def get_debt_of_this_user(date_d, us_id_to, us_id):  # получение долга этого пользователя
    db_sess = db_session.create_session()
    unpaid = db_sess.query(Debts).filter(Debts.date_d == date_d, Debts.us_id_to == us_id_to,
                                         Debts.us_id == us_id).first()
    if unpaid:
        return unpaid.debt
    else:
        return None


def get__tg_tag__from__us_id(us_id):
    db_sess = db_session.create_session()
    name = db_sess.query(User).filter(User.us_id == us_id).first()
    if name:
        return name.tg_tag
    else:
        return 'No one tg_tag'


def get__us_id__from__tg_tag(tg_tag):
    db_sess = db_session.create_session()
    name = db_sess.query(User).filter(User.tg_tag == tg_tag).first()
    if name:
        return name.us_id
    else:
        return 'No one us_id'


def get__us_id__from__tg_id(tg_id):
    db_sess = db_session.create_session()
    name = db_sess.query(User).filter(User.tg_id == tg_id).first()
    if name:
        return name.us_id
    else:
        return 'No one us_id'


def get__tg_tag__from__tg_id(tg_id):
    db_sess = db_session.create_session()
    name = db_sess.query(User).filter(User.tg_id == tg_id).first()
    if name:
        return name.tg_tag
    else:
        return 'No one tg_tag'


def get__us_id__wallet(us_id):
    db_sess = db_session.create_session()
    wall = db_sess.query(User).filter(User.us_id == us_id).first()
    if wall:
        return wall.wallet
    else:
        return 'No one us_id'
