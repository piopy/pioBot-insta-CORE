from chatterbot import ChatBot
import chatterbot, json
from chatterbot.response_selection import get_first_response, get_most_frequent_response
try:from chatterbot.comparisons import LevenshteinDistance #versione PC
except: from chatterbot.comparisons import levenshtein_distance
try: function = chatterbot.comparisons.LevenshteinDistance #versione PC
except: function = chatterbot.comparisons.levenshtein_distance
server, name, db='','',''

with open("config.json") as f:
    data = json.loads(f.read())
    server = data["server_uri"]
    name = data["name"]
    db = data["dbname"]
print(name+' '+db+'\nConnecting to '+server+'...')
pio = ChatBot(
    name,
    storage_adapter = "chatterbot.storage.MongoDatabaseAdapter", #"chatterbot.storage.SQLStorageAdapter",
    database = db, #"./db.sqlite3",
    database_uri = server, ##qua non c'era niente
    input_adapter = "chatterbot.input.VariableInputTypeAdapter",
    output_adapter = "chatterbot.output.OutputAdapter",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            
        }
    ],
    statement_comparison_function = function,
    response_selection_method = get_first_response
)
