import gamestate
import connections



def run():
    gs = gamestate.GameRunner(None, "data.db")
    cm = connections.ConnectionManager(gs.dispatch)
    gs.cm = cm
    cm.emptier = gs.emptier
    cm.leaver = gs.leaver
    cm.start_server()



if __name__ == "__main__":
    run()
