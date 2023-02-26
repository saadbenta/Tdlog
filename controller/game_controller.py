import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# import the Game model and the GameService class from their respective modules
from model.game import Game
from services.game_service import GameService

# instantiate the FastAPI app
app = FastAPI()

# instantiate a GameService object to be used by the API endpoints
game_service = GameService()

# define a Pydantic model for the data required to create a game
class CreateGameData(BaseModel):
    player_name: str
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int

# define an endpoint for creating a game
@app.post("/create-game")
async def create_game(game_data: CreateGameData):
    return game_service.create_game(game_data.player_name, game_data.min_x,game_data.max_x, game_data.min_y,game_data.max_y, game_data.min_z,game_data.max_z)

# define an endpoint for getting a game by its ID
@app.get("/get-game")
async def get_game(game_id: int) -> Game:
    return game_service.get_game(game_id)

# define a Pydantic model for the data required to join a game
class JoinGameData(BaseModel):
    game_id: int
    player_name: str

# define an endpoint for joining a game
@app.post("/join-game")
async def join_game(game_data: JoinGameData) -> bool:
    try:
        game_service.join_game(game_data.game_id,game_data.player_name)
    except :
        return False
    return True

# define a Pydantic model for the data required to add a vessel to a game
class AddVesselData(BaseModel):
    game_id: int
    player_name: str
    vessel_type: str
    x: int
    y: int
    z: int

# define an endpoint for adding a vessel to a game
@app.post("/add-vessel")
async def add_vessel(game_data: AddVesselData) -> bool:
    try:
        game_service.add_vessel(game_data.game_id,game_data.player_name, game_data.vessel_type,game_data.x, game_data.y,game_data.z)
    except:
        return False
    return True

# define a Pydantic model for the data required to shoot at a vessel in a game
class ShootAtData(BaseModel):
    game_id: int
    shooter_name: str
    vessel_id: int
    x: int
    y: int
    z: int

# define an endpoint for shooting at a vessel in a game
@app.post("/shoot-at")
async def shoot_at(game_data: ShootAtData) -> bool:
    try:
        game_service.shoot_at(game_data.game_id,game_data.shooter_name,game_data.vessel_id,game_data.x,game_data.y,game_data.z)
    except:
        return False
    return True

# define an endpoint for getting the status of a game
@app.get("/game-status")
async def get_game_status(game_id: int, player_name: str) -> str:
    try:
        return game_service.get_game_status(game_data.game_id,game_data.player_name)
    except:
        return False

# Running the application using Uvicorn server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)