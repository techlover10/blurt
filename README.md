# Blurt

## Preparing development environment (Linux/WSL)
```
git clone <this repo>
cd <this repo>
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./pre_init.sh
```

To run, simply execute 
```
./dev_server.sh
```
This will start a server at localhost:8000.


# old directions

# blurt

TO RUN (jwonggg):
```
git clone <this repo>
cd <this repo>
python3 -m venv .
source bin/activate
pip install -r requirements.txt
sqlite3 data.db < schema.sql
sqlite3 data.db < init.sql
python src/runner.py &
cd static
python -m http.server
```

or whatever the windows versions of all that is

this should get you started at `localhost:8000`



the whole of the game is conducted through websocket messages


ARCHITECTURE OF THE CONNECTION MANAGER:
registers players as they come in, but more than anything else calls a passed dispatch function, which takes a message and the connectionmanager

this passed function handles all the logic, and since it's passed the connectionmanager, it can broadcast various results and so forth.

I may modify this later to add some sort of client id system or something, to enable more than fairly naive broadcast situations, though this may be possible externally (well, the main thing is associating the websocket object for a connection with some sort of username or something, probably best done through subclassing or the like, maybe kinda hacky but still probably okay)

Then from there, the game object handles everything, using the methods available to it from the passed connectionmanager (mostly, broadcast)


to join the game (or rejoin the game), client sends stringified json of the form
`{"join": "<username>"}`. As long as one person has a live connection the current game will maintain, when everyone drops the game is tossed and a new game is started when new clients connect

The die roll and everything is done by the server. The server gives out the question, and when the client recieves it sends back an acknowledgement for latency measuring purposes.


--------

notes on word lists:

SAT words, from https://www.vocabulary.com/lists/191545
