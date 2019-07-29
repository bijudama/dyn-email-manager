from sanic import Sanic
from databases import Database
from config import Config
from routes import setup as setupRoutes
from middlewares import setup as setupMiddlewares

app = Sanic(__name__)
app.config.from_object(Config)

app.db = Database(app.config.DB_URL)

@app.listener('after_server_start')
async def connect_to_db(*args, **kwargs):
    await app.db.connect()

@app.listener('after_server_stop')
async def disconnect_from_db(*args, **kwargs):
    await app.db.disconnect()


setupRoutes(app)
setupMiddlewares(app)


def run():
    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG,
    )

if __name__ == "__main__":
    run()