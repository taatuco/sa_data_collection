from flask import Flask
app = Flask(__name__)

@app.route('/')
def we_are_badasses():
   return 'Shake it baby shake it baby, you wanna dance, you wanna dance!'

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080)
