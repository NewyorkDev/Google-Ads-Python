from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Home Page</h1>'

@app.route('/book/<book_id>')
def book(book_id):
    return 'Book ' + book_id

@app.route('/books', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return 'All Books'
    if request.method == 'POST':
        name = request.json['name']
        age = request.json['age']
        married = request.json['married']
        user = {name: name, age: age, married: married}
        return user
        # return request.json

@app.route('/returnjson')
def returnjson():
    num_list = [1,2,3,4,5]
    num_dict = {'numbers' : num_list, 'name' : 'Numbers'}
    return jsonify({'output' : num_dict})

if __name__ == '__main__':
 app.run(port = 3000, host='localhost', debug=True)