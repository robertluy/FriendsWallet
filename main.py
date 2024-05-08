import asyncio
from datetime import datetime
from db_control import db_instance  # Убедитесь, что это правильный импорт для вашей конфигурации
from db_wrk import AsyncCore as dbw
from db_control import SqlAlchemyBase


async def main():
    await db_instance.init_db()
    await dbw.create_tables()

    # Добавление пользователей
    await dbw.add_user('@RealRoberL', '410403', '3120432')
    await dbw.add_user('@RobotDolbaeb', '21311', '21321103')
    await dbw.add_user('@NikitaDolbaeb', '32311', '53321103')

    timem = datetime(2024, 3, 3)
    await dbw.add_debt(timem, 1, 2, 1000)
    await dbw.add_debt(timem, 1, 3, 1000)
    await dbw.update_debt_status(timem, 1, 2, 'yes')

    unpaid = await dbw.get_unpaid_users(timem, 1)
    paid = await dbw.get_paid_users(timem, 1)
    debt_of_him = await dbw.get_debt_of_this_user(timem, 1, 2)
    tg_tag = await dbw.get_tg_tag_from_us_id(1)
    us_id_by_tag = await dbw.get_us_id_from_tg_tag('@RealRoberL')
    tg_tag_by_tg_id = await dbw.get_tg_tag_from_tg_id('410403')
    us_id_by_tg_id = await dbw.get_us_id_from_tg_id('410403')
    wallet = await dbw.get_us_id_wallet(1)

    print('unpaid:', unpaid)
    print('paid:', paid)
    print('debt of him:', debt_of_him)
    print('tg_tag from us_id:', tg_tag)
    print('us_id from tg_tag:', us_id_by_tag)
    print('tg_tag from tg_id:', tg_tag_by_tg_id)
    print('us_id from tg_id:', us_id_by_tg_id)
    print('wallet:', wallet)


if __name__ == "__main__":
    asyncio.run(main())
