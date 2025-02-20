from shareX import app, socketio

if __name__ == "__main__":
    # path = os.path.join(os.path.dirname(__file__), 'instance')
    # database_path = os.path.join(path, 'database.database')
    # print(os.path.exists(database_path))
    # print(path)
    socketio.run(app)
    
