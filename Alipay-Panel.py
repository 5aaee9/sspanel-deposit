from Actions import Actions
from flask import Flask
app = Flask(__name__)

# app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
Actions(app).init()

if __name__ == '__main__':
    app.run()
