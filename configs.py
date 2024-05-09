from dataclasses import dataclass



@dataclass
class ConfigDatabase :
    user : str
    password : str
    database : str
    host : str
    port : str


config_db = ConfigDatabase(user='postgres', password='islam95', database='postgres', host='127.0.0.1', port=5432)

TOKEN = ''

conf_admins = [6330057147, 5216336395]