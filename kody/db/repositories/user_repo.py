
from ..models import User
from .base_repo import BaseRepo


class UserRepository(BaseRepo[User]):
    def __init__(self) -> None:
        super().__init__()

    def add(self, user: User) -> User:
        with self.session.begin():
            self.session.add(user)

        return user

    def get(self, _id: int) -> User | None:
        with self.session.begin():
            user = self.session.query(User).filter_by(id=_id).first()

        return user

    def remove(self, target: User) -> bool:
        success = False
        try:
            with self.session.begin():
                self.session.delete(target)

            success = True
        except:
            pass
        finally:
            self.session.close()

        return success

    def save(self, target: User) -> User:
        with self.session.begin():
            self.session.merge(target)

        return target