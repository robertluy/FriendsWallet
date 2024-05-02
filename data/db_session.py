import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()  # абстрактная декларативная бд
__factory = None  # получение сессий подключения к бд


def global_init(db_file):  # инициализация бд
    global __factory
    if __factory:  # проверка что вызвали в первый раз
        return  # если не в первый
    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'  # тип бд, адрес до бд и парам подкл
    print(f"Подключение к базе данных по адресу {conn_str}")
    engine = sa.create_engine(conn_str,
                              echo=False)  # скалхимик выбирает движок для работы с бд, у нас это с SQLite,
    # echo=True будет выводить в консоль SQL запросы
    __factory = orm.sessionmaker(bind=engine)  # фабрика подключений создана
    from . import __all_models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:  # для удобства в виде подсказок, вообще это тип возвращаемый
    global __factory
    return __factory()
