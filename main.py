from cmyui import (AsyncSQLPool, Version, Ansi, log)
from quart import Quart

from objects import glob

""" application """
app = Quart(__name__)

""" globals """
# database
@app.before_serving
async def mysql_conn() -> None:
    glob.db = AsyncSQLPool()
    await glob.db.connect(glob.config.mysql)
    log("Connected to MySQL!", Ansi.LGREEN)

# version
@app.before_serving
@app.template_global("appVersion")
def app_version() -> str:
    return Version(0, 1, 0)

# app name
@app.before_serving
@app.template_global("appName")
def app_name() -> str:
    return glob.config.app_name

""" blueprints """
# frontend
from blueprints.frontend import frontend
app.register_blueprint(frontend)

# backend
from blueprints.admin import admin
app.register_blueprint(admin, url_prefix="/admin")

# api
from blueprints.api import api
app.register_blueprint(api, url_prefix="/api")


""" start application """
if __name__ == "__main__":
    app.run(debug=True)
