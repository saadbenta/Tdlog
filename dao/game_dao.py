from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Integer, String, Column,ForeignKey,select
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from model.game import Game
from model.player import Player
from model.vessel import Vessel
from model.battlefield import Battlefield
engine = create_engine('sqlite:////tmp/tdlog.db', echo=True, future=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

class GameEntity(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    player = relationship("PlayerEntity", back_populates="game",
    cascade="all, delete-orphan")
class PlayerEntity(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    game = relationship("GameEntity", back_populates="player")
    battle_field = relationship("BattlefieldEntity",back_populates="player",uselist=False, cascade="all, delete-orphan")
class BattlefieldEntity(Base):
    __tablename__ = 'battlefield'
    id = Column(Integer, primary_key=True)
    min_x = Column(Integer)
    min_y= Column(Integer)
    min_z = Column(Integer)
    max_x = Column(Integer)
    max_y = Column(Integer)
    max_z = Column(Integer)
    max_power= Column(Integer)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    player = relationship("PlayerEntity", back_populates="battle_field")
    vessel = relationship("VesselEntity",back_populates="vessel",uselist=False, cascade="all, delete-orphan")

class VesselEntity(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    coord_x = Column(Integer)
    coord_y = Column(Integer)
    coord_z = Column(Integer)
    hits_to_be_destroyed = Column(Integer)
    type = Column(String)
    Battle_field_id = Column(Integer, ForeignKey("battlefield.id"), nullable=False)
    battle_field =  relationship("BattlefieldEntity", back_populates="battle_field")
    weapon = relationship("WeaponEntity", back_populates="vessel", uselist=False, cascade="all, delete-orphan")
class WeaponEntity(Base):
    id = Column(Integer, primary_key=True)
    ammunations = Column(Integer)
    range = Column(Integer)
    type = Column(String)
    vessel_id = Column(Integer, ForeignKey("vessel.id"), nullable = False)
    vessel = relationship("BattlefieldEntity", back_populates="weapons")

def map_to_game(game: GameEntity) :
    ga=Game(game.id)
    a=game.players
    for i in range(len(a)) :
        ga.add_player(a[i])
    return ga

def map_to_game_entity(game: Game) :
    game_entity = GameEntity()
    if game.get_id() is not None:
        game_entity.id = game.get_id()
    for player in game.get_players():
        player_entity = PlayerEntity()
        player_entity.id = player.id
        player_entity.name = player.get_name()
        battlefield_entity = map_to_battlefield_entity(
            player.get_battlefield())
        vessel_entities = map_to_vessel_entities(player.get_battlefield().id,player.get_battlefield().vessels)
        battlefield_entity.vessels = vessel_entities
        player_entity.battle_field = battlefield_entity
        game_entity.players.append(player_entity)
    return game_entity

def map_to_player_entity(player: Player) :
    player_entity = PlayerEntity()
    player_entity.id = player.id
    player_entity.name = player.name
    player_entity.battle_field = map_to_battlefield_entity(
        player.get_battlefield())
    return player_entity
def find_vessel(self, vessel_id: int) :
    stmt = select(VesselEntity).where(VesselEntity.id == vessel_id) 
    vessel_entity = self.db_session.scalars(stmt).one()
    return map_to_vessel(vessel_entity)
def map_to_player(player:PlayerEntity) :
    result= Player()
    result.name=player.name
    result.id=player.id
    result.battle_field=player.battle_field
    return result

def map_to_vessel_entities(battlefield_id: int, vessels):
    vessel_entities: list[VesselEntity] = []
    for vessel in vessels:
        vessel_entity = map_to_vessel_entity(battlefield_id, vessel)
        vessel_entities.append(vessel_entity)
    return vessel_entities
def map_to_vessel(weapon_entity: WeaponEntity, vessel_entity: VesselEntity) -> Vessel:
    weapon = weapon(weapon_entity.id,weapon_entity.ammunitions,weapon_entity.range)
    result = Vessel(vessel_entity.id,vessel_entity.coord_x,vessel_entity.coord_y,vessel_entity.coord_z,vessel_entity.hits_to_be_destroyed,weapon)
    type(result.weapon).__name__ = weapon_entity.type 
    type(result).__name__= vessel_entity.type
    return result

def map_to_vessel_entity(battlefield_id: int, vessel: Vessel) -> VesselEntity:
    vessel_entity = VesselEntity()
    weapon_entity = WeaponEntity()
    weapon_entity.id = vessel.weapon.id
    weapon_entity.ammunitions = vessel.weapon.ammunitions
    weapon_entity.range = vessel.weapon.range
    weapon_entity.type = type(vessel.weapon).__name__
    vessel_entity.id = vessel.id
    vessel_entity.weapon = weapon_entity
    vessel_entity.type = type(vessel).__name__
    vessel_entity.hits_to_be_destroyed = vessel.hits_to_be_destroyed
    vessel_entity.coord_x = vessel.coordinates[0]
    vessel_entity.coord_y = vessel.coordinates[1]
    vessel_entity.coord_z = vessel.coordinates[2]
    vessel_entity.battle_field_id = battlefield_id
    return vessel_entity

def map_to_battlefield(battlefield: BattlefieldEntity):
    result=battlefield(battlefield.min_x,battlefield.max_x,battlefield.min_y,battlefield.max_y,battlefield.min_z,battlefield.max_z,battlefield.max_power)
    return result

def map_to_weapon(weapon: WeaponEntity):
    result=weapon()

def map_to_battlefield_entity(battlefield: Battlefield)  :
    battlefield_entity = BattlefieldEntity()
    battlefield_entity.id = battlefield.id
    battlefield_entity.max_x = battlefield.max_x
    battlefield_entity.max_y = battlefield.max_y
    battlefield_entity.max_z = battlefield.max_z
    battlefield_entity.min_x = battlefield.min_x
    battlefield_entity.min_y = battlefield.min_y
    battlefield_entity.min_z = battlefield.min_z
    battlefield_entity.max_power = battlefield.max_power
    return battlefield_entity


class GameDao:
    def __init__(self):
        Base.metadata.create_all()
        self.db_session = Session()
    def create_game(self, game: Game) -> int:
        game_entity = map_to_game_entity(game)
        self.db_session.add(game_entity)
        self.db_session.commit()
        return game_entity.id
    def find_game(self, game_id: int) -> Game:
        stmt = select(GameEntity).where(GameEntity.id == game_id)
        game_entity = self.db_session.scalars(stmt).one()
        return map_to_game(game_entity)