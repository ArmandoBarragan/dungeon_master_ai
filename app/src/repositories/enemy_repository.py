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

    def get_enemy(self, enemy_id: int) -> Enemy | None:
        return self.db.query(Enemy).filter(Enemy.id == enemy_id).first()

    def update_enemy(self, enemy: Enemy) -> Enemy:
        self.db.flush()
        return enemy

    def get_enemies_by_encounter_id(self, encounter_id: int) -> list[Enemy]:
        return self.db.query(Enemy).filter(Enemy.encounter_id == encounter_id).all()
