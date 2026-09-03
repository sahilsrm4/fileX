import json
from utils.validation import (validate_username,validate_password)
from models.player import Player

class Authentication:
    def __init__(self):
        self.players = []
        self.admin = {"password":""}
        try:
            with open("data\\users.json",'r') as file:
                data = json.load(file)
                self.players = data["players"]
                self.admin = data['admin']
        except FileNotFoundError:
            print("Warning users.json file not found starting with no registered players")
        except (json.JSONDecodeError, KeyError):
            print("Warning users.json corrupted. Starting with no registered players")    
        
    def register_player(self,player:Player):
        if not validate_username(player.username):
            return False
        if not validate_password(player.password):
            return False
        
        if self.players:
            player_id = max(play['id'] for play in self.players)+1
        else:
            player_id = 1
        player_data = {
            "id":player_id,
            "username":player.username,
            "password":player.password,
        }
        
        for user in self.players:
            if user['username'] == player.username:
                print("User already exists")
                return False
           
        self.players.append(player_data)
        self._save_players()
        
        return True
    
    def login_player(self,username:str,password:str):
        for player in self.players:
            if player['username']==username and player['password']==password:
                player_obj = Player(
                    username=player['username'],
                    password=player['password'],
                )
                player_obj.is_logged_in = True
                return player_obj
        print("Invalid username or password! Try again")
        return None
    
    def login_admin(self,password:str):
        
        return self.admin['password']==password
    
    def _save_players(self):
        with open("data\\users.json",'w') as file:
            data = {
                "players":self.players,
                "admin":self.admin
            }
            json.dump(data,file,indent=4)
 