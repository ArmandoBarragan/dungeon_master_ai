from sqlalchemy.orm import Session

from src.models.enemy_model import Enemy


class EnemyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_enemies(self, enemies: list[Enemy]) -> list[Enemy]:
        self.db.add_all(enemies)
        self.db.flush()
        for enemy in enemies:
            self.db.refresh(enemy)
        return enemies

    def get_by_ref(self, enemy_ref: str, encounter_id: int) -> Enemy | None:
        return (
            self.db.query(Enemy)
            .filter(Enemy.ref == enemy_ref, Enemy.encounter_id == encounter_id)
            .first()
        )

    def update(self, enemy: Enemy) -> Enemy:
        self.db.flush()
        return enemy

    def delete(self, enemy_ref: str, encounter_id: int) -> None:
        enemy = self.get_by_ref(enemy_ref, encounter_id)
        if enemy is None:
            return
        self.db.delete(enemy)
        self.db.flush()

    def get_enemies_by_encounter_id(
        self, 
        encounter_id: int,
        params: dict | None = None,
        order_by: list | None = None,
        order_direction: list | None = None
    ) -> list[Enemy]:
        query = self.db.query(Enemy).filter(Enemy.encounter_id == encounter_id)
        if params:
            for key, value in params.items():
                query = query.filter(getattr(Enemy, key) == value)
        if order_by:
            for column, direction in order_by:
                if direction == "desc":
                    query = query.order_by(getattr(Enemy, column).desc())
                else:
                    query = query.order_by(getattr(Enemy, column).asc())
        return query.all()
