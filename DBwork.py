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


def add_friend(date_d, us_id_to, us_id, debt, status):  # добавление друга-должника
    deb = Debts()
    deb.date_d = date_d
    deb.us_id_to = us_id_to
    deb.us_id = us_id
    deb.debt = debt
    deb.status = status
    db_sess = db_session.create_session()
    db_sess.add(deb)
    db_sess.commit()


def upgrade_status_of_this_user(date_d, us_id_to, us_id, new_status):  # обновление статуса должника
    db_sess = db_session.create_session()
    debt = db_sess.query(Debts).filter(Debts.date_d == date_d, Debts.us_id_to == us_id_to, Debts.us_id == us_id).first()
    if debt:
        debt.status = new_status
        db_sess.commit()
    else:
        print('no one users')


def get_unpaid_users(date_d, us_id_to):  # получение списка пользователей должников кортежом (tg_tag, долг)
    db_sess = db_session.create_session()
    unpaid_users = db_sess.query(User.tg_tag).join(Debts, Debts.us_id == User.us_id).filter(Debts.date_d == date_d,
                                                                                            Debts.us_id_to == us_id_to,
                                                                                            Debts.status == 'no').all()
    return [(i.tg_tag, i.debt) for i in unpaid_users]


def get_paid_users(date_d, us_id_to):  # получение списка оплативших друзей в том же формате
    db_sess = db_session.create_session()
    paid_users = db_sess.query(User).join(Debts, Debts.us_id == User.us_id).filter(Debts.date_d == date_d,
                                                                                   Debts.us_id_to == us_id_to,
                                                                                   Debts.status == 'yes').all()
    return [(i.tg_tag, i.debt) for i in paid_users]


def get_debt_of_this_user(date_d, us_id_to, us_id):  # получение долга этого пользователя
    db_sess = db_session.create_session()
    unpaid = db_sess.query(Debts).filter(Debts.date_d == date_d, Debts.us_id_to == us_id_to,
                                         Debts.us_id == us_id).first()
    if unpaid:
        return unpaid.debt
    else:
        return None
