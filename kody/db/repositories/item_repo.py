
from ..models import Item
from .base_repo import BaseRepo


class ItemRepository(BaseRepo[Item]):
    def __init__(self) -> None:
        super().__init__()

    def add(self, item: Item) -> Item:
        with self.session.begin():
            self.session.add(item)

        return item

    def get(self, user_id: int, item_id: int) -> Item | None:
        with self.session.begin():
            user = self.session.query(Item).filter_by(
                user_id=user_id, item_id=item_id).first()

        return user

    def all(self, user_id: int) -> list[Item]:
        with self.session.begin():
            items = self.session.query(Item).filter_by(user_id=user_id).all()

        return items

    def remove(self, target: Item) -> bool:
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

    def save(self, target: Item) -> Item:
        with self.session.begin():
            self.session.merge(target)

        return target
