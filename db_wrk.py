from db_control import db_instance, SqlAlchemyBase
from sqlalchemy.future import select
from models import User, Debts


class AsyncCore:
    @staticmethod
    async def create_tables():
        async with db_instance.async_engine.begin() as conn:
            await conn.run_sync(SqlAlchemyBase.metadata.create_all)

    @staticmethod
    async def check_user(tg_tag):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(User).filter(User.tg_tag == tg_tag)
            )
            user = result.scalars().first()
            return user is None

    @staticmethod
    async def add_user(tg_tag, tg_id=' ', wallet=' '):
        if await AsyncCore.check_user(tg_tag):
            async with db_instance.async_session_factory() as session:
                user = User(tg_tag=tg_tag, tg_id=tg_id, wallet=wallet)
                session.add(user)
                await session.commit()

    @staticmethod
    async def add_debt(date_d, us_id_to, us_id, debt, status='no'):
        async with db_instance.async_session_factory() as session:
            debt_record = Debts(date_d=date_d, us_id_to=us_id_to, us_id=us_id, debt=debt, status=status)
            session.add(debt_record)
            await session.commit()

    @staticmethod
    async def update_debt_status(date_d, us_id_to, us_id, new_status='yes'):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(Debts).filter(Debts.date_d == date_d, Debts.us_id_to == us_id_to, Debts.us_id == us_id)
            )
            debt = result.scalars().first()
            if debt:
                debt.status = new_status
                await session.commit()
            else:
                print('No such debt found')

    @staticmethod
    async def get_unpaid_users(date_d, us_id_to):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(User.tg_tag, Debts.debt).join(Debts, Debts.us_id == User.us_id).filter(Debts.date_d == date_d,
                                                                                              Debts.us_id_to == us_id_to,
                                                                                              Debts.status == 'no')
            )
            return result.all()

    @staticmethod
    async def get_paid_users(date_d, us_id_to):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(User.tg_tag, Debts.debt).join(Debts, Debts.us_id == User.us_id).filter(Debts.date_d == date_d,
                                                                                              Debts.us_id_to == us_id_to,
                                                                                              Debts.status == 'yes')
            )
            return result.all()

    @staticmethod
    async def get_debt_of_this_user(date_d, us_id_to, us_id):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(Debts.debt).filter(Debts.date_d == date_d, Debts.us_id_to == us_id_to, Debts.us_id == us_id)
            )
            debt = result.scalars().first()
            return debt if debt else 'No debt found'

    @staticmethod
    async def get_tg_tag_from_us_id(us_id):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(User.tg_tag).filter(User.us_id == us_id)
            )
            tg_tag = result.scalars().first()
            return tg_tag if tg_tag else 'No tag found'

    @staticmethod
    async def get_us_id_from_tg_tag(tg_tag):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(User.us_id).filter(User.tg_tag == tg_tag)
            )
            us_id = result.scalars().first()
            return us_id if us_id else 'No user id found'

    @staticmethod
    async def get_us_id_from_tg_id(tg_id):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(User.us_id).filter(User.tg_id == tg_id)
            )
            us_id = result.scalars().first()
            return us_id if us_id else 'No user id found'

    @staticmethod
    async def get_tg_tag_from_tg_id(tg_id):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(User.tg_tag).filter(User.tg_id == tg_id)
            )
            tg_tag = result.scalars().first()
            return tg_tag if tg_tag else 'No tag found'

    @staticmethod
    async def get_us_id_wallet(us_id):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(User.wallet).filter(User.us_id == us_id)
            )
            wallet = result.scalars().first()
            return wallet if wallet else 'No wallet found'
