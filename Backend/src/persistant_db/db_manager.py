import sqlalchemy as db

from sqlalchemy.orm import sessionmaker

from Backend.src.utils.singletone_meta import SingletonMeta
from Backend.src.settings import settings
from Backend.src.persistant_db.db_models import UserModel, ProductModel


class DBManager(metaclass=SingletonMeta):
    _engine = db.create_engine(settings.postgres_connection_string)
    _metadata = db.MetaData()
    _session_maker = sessionmaker(bind=_engine)


class UsersTable(DBManager):
    """
    Manger class for interacting with the 'users' table
    """
    def create_new_user(self, username, fullname, email=None) -> None:
        """
        Create new user in the database
        :param username: The user's username
        :param fullname: The user's fullname
        :param email: The user's email (optional)
        :return: None
        """
        user = UserModel(username=username, fullname=fullname, email=email)
        with self._session_maker() as session:
            session.add(user)
            session.commit()

    def get_all_users(self, page=1, page_size=1) -> list:
        """
        Fetch all users in the database.
        Inorder to allow handling large amount of data, paging is a relevant solution here
        :param page: The current page to fetch
        :param page_size: The amount of records to include in each the following fetch
        :return:
        """
        if page < 1 or page_size < 1:
            return []

        offset = (page - 1) * page_size
        with self._session_maker() as session:
            result = session.query(UserModel).offset(offset).limit(page_size).all()

        return result

    def get_single_user(self, user_id):
        with self._session_maker() as session:
            user = session.query(UserModel).filter_by(id=user_id).first()

        return user

    def update_mail(self, user_id, new_mail) -> None:
        """
        Update a user's email
        :param user_id: The user's id that you want to update its email
        :param new_mail: The user's new email
        :return: None
        """
        with self._session_maker() as session:
            user_to_update = session.query(UserModel).filter_by(id=user_id).first()
            if user_to_update:
                user_to_update.email = new_mail
                session.commit()

    def update_fullname(self, user_id, new_full_name) -> None:
        """
        Update a user's fullname
        :param user_id: The user's id that you want to update its fullname
        :param new_full_name: The user's fullname
        :return: None
        """
        with self._session_maker() as session:
            user_to_update = session.query(UserModel).filter_by(id=user_id).first()
            if user_to_update:
                user_to_update.fullname = new_full_name
                session.commit()

    def delete_user(self, user_id) -> None:
        """
        Delete a user by its id
        :param user_id: The user's id
        :return: None
        """
        with self._session_maker() as session:
            user = session.query(UserModel).filter_by(id=user_id).first()
            if user:
                session.delete(user)
                session.commit()


class ProductsTable(DBManager):
    def create_product(self, name, price) -> None:
        """
        Create new product
        :param name: The product's name
        :param price: The product's price
        :return: None
        """
        product = ProductModel(name=name, price=price)
        with self._session_maker() as session:
            session.add(product)
            session.commit()

    def get_all_products(self, page=1, page_size=1) -> list:
        """
        Fetch all products in the database.
        Inorder to allow handling large amount of data, paging is a relevant solution here
        :param page: The current page to fetch
        :param page_size: The amount of records to include in each the following fetch
        :return:
        """
        if page < 1 or page_size < 1:
            return []

        offset = (page - 1) * page_size
        with self._session_maker() as session:
            result = session.query(ProductModel).offset(offset).limit(page_size).all()

        return result

    def get_single_product(self, product_id):
        with self._session_maker() as session:
            product = session.query(ProductModel).filter_by(id=product_id).first()

        return product

    def update_price(self, product_id, new_price) -> None:
        """
        Update a product's price
        :param product_id: The product's id for which you want to update its price
        :param new_price: The product's new price
        :return: None
        """
        with self._session_maker() as session:
            product_to_update = session.query(ProductModel).filter_by(id=product_id).first()
            if product_to_update:
                product_to_update.price = new_price
                session.commit()

    def delete_product(self, product_id) -> None:
        """
        Delete a user by its id
        :param product_id: The user's id
        :return: None
        """
        with self._session_maker() as session:
            product = session.query(ProductModel).filter_by(id=product_id).first()
            if product:
                session.delete(product)
                session.commit()


