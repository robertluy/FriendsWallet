from db_control import db_instance, SqlAlchemyBase
from sqlalchemy.future import select
from models import User, Debts


class AsyncCore:
    @staticmethod
    async def create_tables():
        async with db_instance.async_engine.begin() as conn:
            await conn.run_sync(SqlAlchemyBase.metadata.de)
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
    async def add_debt(date_d, tg_id_to, tg_id, debt, status='no'):
        async with db_instance.async_session_factory() as session:
            debt_record = Debts(date_d=date_d, tg_id_to=tg_id_to, tg_id=tg_id, debt=debt, status=status)
            session.add(debt_record)
            await session.commit()

    @staticmethod
    async def update_debt_status(date_d, tg_id_to, tg_id, new_status='yes'):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(Debts).filter(Debts.date_d == date_d, Debts.tg_id_to == tg_id_to, Debts.tg_id == tg_id)
            )
            debt = result.scalars().first()
            if debt:
                debt.status = new_status
                await session.commit()
            else:
                print('No such debt found')

    @staticmethod
    async def get_unpaid_users(date_d, tg_id_to):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(User.tg_tag, Debts.debt).join(Debts, Debts.tg_id == User.tg_id).filter(Debts.date_d == date_d,
                                                                                              Debts.tg_id_to == tg_id_to,
                                                                                              Debts.status == 'no')
            )
            return result.all()

    @staticmethod
    async def get_paid_users(date_d, tg_id_to):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(User.tg_tag, Debts.debt).join(Debts, Debts.tg_id == User.tg_id).filter(Debts.date_d == date_d,
                                                                                              Debts.tg_id_to == tg_id_to,
                                                                                              Debts.status == 'yes')
            )
            return result.all()

    @staticmethod
    async def get_debt_of_this_user(date_d, tg_id_to, tg_id):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(Debts.debt).filter(Debts.date_d == date_d, Debts.tg_id_to == tg_id_to, Debts.tg_id == tg_id)
            )
            debt = result.scalars().first()
            return debt if debt else 'No debt found'

    @staticmethod
    async def get_tg_tag_from_tg_id(tg_id):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(User.tg_tag).filter(User.tg_id == tg_id)
            )
            tg_tag = result.scalars().first()
            return tg_tag if tg_tag else 'No tag found'

    @staticmethod
    async def get_tg_id_from_tg_tag(tg_tag):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(User.tg_id).filter(User.tg_tag == tg_tag)
            )
            tg_id = result.scalars().first()
            return tg_id if tg_id else 'No user id found'

    @staticmethod
    async def get_tg_tag_from_tg_id(tg_id):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(User.tg_tag).filter(User.tg_id == tg_id)
            )
            tg_tag = result.scalars().first()
            return tg_tag if tg_tag else 'No tag found'

    @staticmethod
    async def get_tg_id_wallet(tg_id):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(User.wallet).filter(User.tg_id == tg_id)
            )
            wallet = result.scalars().first()
            return wallet if wallet else 'No wallet found'

    @staticmethod
    async def get_to_whom__tg_id__owe(tg_id):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(
                    Debts.us_id_to,
                    Debts.debt,
                    Debts.status,
                    Debts.currency,
                    User.wallet
                ).join(User, Debts.tg_id_to == User.tg_id).where(Debts.tg_id == tg_id)  # tg_id является должником
            )
            debts_list = [
                {
                    "us_id_to": debt[0],
                    "debt": debt[1],
                    "status": debt[2],
                    "currency": debt[3],
                    "wallet": debt[4]
                } for debt in result.all()
            ]
            return debts_list

    @staticmethod
    async def get_who_owe_to__tg_id(tg_id):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(
                    Debts.us_id,
                    Debts.debt,
                    Debts.status,
                    Debts.currency,
                    User.wallet
                ).join(User, Debts.us_id == User.tg_id).where(Debts.us_id_to == tg_id)
            )
            credits_list = [
                {
                    "us_id": debt[0],
                    "debt": debt[1],
                    "status": debt[2],
                    "currency": debt[3],
                    "wallet": debt[4]
                } for debt in result.all()
            ]
            return credits_list

    @staticmethod
    async def get_all__tg_id_operations(tg_id):
        async with db_instance.async_session_factory() as session:
            result = await session.execute(
                select(
                    Debts.us_id,
                    Debts.debt,
                    Debts.status,
                    Debts.currency,
                    User.wallet
                ).join(User, Debts.us_id == User.tg_id).where(Debts.us_id_to == tg_id))
            result2 = await session.execute(
                select(
                    Debts.us_id_to,
                    Debts.debt,
                    Debts.status,
                    Debts.currency,
                    User.wallet
                ).join(User, Debts.tg_id_to == User.tg_id).where(Debts.tg_id == tg_id))
            debts_list = [
                {
                    "us_id_to": debt[0],
                    "debt": debt[1],
                    "status": debt[2],
                    "currency": debt[3],
                    "wallet": debt[4]
                } for debt in result2.all()
            ]
            debts_list2 = [
                {
                    "us_id": debt[0],
                    "debt": debt[1],
                    "status": debt[2],
                    "currency": debt[3],
                    "wallet": debt[4]
                } for debt in result.all()
            ]
            return debts_list + debts_list2
