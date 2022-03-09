from ast import dump
from asyncio.windows_events import NULL
from flask import Flask, Response, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

todo_lists = [
    {'id': "1", 'name': "list 1"}
]

todos = [
    {
     'id': '1', 
     'name': 'test', 
     'description': 'i wish i were written with php',
     'user_id': '1',
     'list_id': '1'
    }
]
users = [
    {
        'id': '1',
        'name': "amogus"
    }
]

@app.route('/')
def redirectIndex():
    return redirect(url_for('listIndex'));

# todolist routes
@app.route("/list")
def listIndex():
    return render_template("todolist/index.html", todoLists=todo_lists) 

@app.route("/todo-list/<list_id>", methods = ["GET"])
def todoShow(list_id):
    data = {}
    for list in todo_lists:
        if list['id'] == list_id: #find the searched list by id
            entries = []
            for entry in todos:
                if entry['list_id'] == list_id: # find all todo entries in this list
                    for user in users:  #find the user belonging to the todo entry
                        if user['id'] == entry['user_id'] : 
                            entries.append({ #create new resource for the frontend containing the user and the todo entry
                                'user' : user,
                                'entry' : entry
                            })    
            data =  {
                "list" : list,
                'entries': entries,
                'users': users
            }
    
    if 'list' not in data:
            return redirect(url_for('listIndex')) # if the list was not found redirect to the index page
    return render_template("todolist/show.html" , data=data) #else return the html
            
@app.route("/todo-list/<list_id>", methods = ["DELETE"])
def todoListDelete(list_id):
    for todo in todos:
        
        if todo['list_id'] == list_id: #find the affected todos to remove
            todos.remove(todo)
            
    for list in todo_lists:
        if(list['id'] == list_id): #find the affected list to remove
            todo_lists.remove(list)
            break
        
    return Response([],200) # return response to ajax request


#todo routes
@app.route("/todo/<todo_id>", methods = ["GET"])
def todoDelete(todo_id):
    list_id = NULL
    for todo in todos:
        if todo['id'] == todo_id:
            list_id = todo['list_id']
            todos.remove(todo)
            break
    
    if list == NULL:
        return redirect(url_for('listIndex'))
    return redirect(url_for("todoShow", list_id=list_id))
        
@app.route("/todo-list/store", methods = ["POST"])
def createList ():
    id = "1"
    if len(todos) != 0: #if list not empty get latest entry
        lastEntry = todo_lists[-1]
        id =  str(int(lastEntry['id']) + 1)
        
    newList = {
        'id': id,
        'name': request.form.get("name")
    }
    
    todo_lists.append(newList)
    return redirect(url_for('listIndex'))

@app.route("/todo/<list_id>/store", methods= ["POST"])
def createTodoEntry(list_id):
    
    id = "1"
    if len(todos) != 0: #if list not empty get latest entry
        todo = todos[-1]
        id =  str(int(todo['id']) + 1)
        
    newEntry = { #prepare new todo resource
        'id' :id,
        'name': request.form.get('name'), 
        'description': request.form.get('content'),
        'user_id': request.form.get('user'),
        'list_id': list_id
    }
    todos.append(newEntry) #create new todo
    
    return redirect(url_for('todoShow', list_id=list_id))
    
@app.route("/todo/<todo_id>/edit", methods= ["GET"])
def todoEdit(todo_id):
    selectedTodo = {}
    for todo in todos: # find todo entry
        if todo['id'] == todo_id:
            selectedTodo = todo
            break
         
    data = {
        'todo': selectedTodo,
        'users': users
    }
    return render_template('todolist/edit.html', data=data)

@app.route('/todo/<todo_id>/update', methods=["POST"])
def todoUpdate(todo_id):
    for todo in todos:
        if todo['id'] == todo_id: # find effected todo entry and rewrite all data
            todo['name'] = request.form.get('name')
            todo['user_id'] = request.form.get('user')
            todo['description'] = request.form.get('content')
            break
    return redirect(url_for('todoShow', list_id=todo['list_id']))

@app.route('/user', methods=["GET"])
def userIndex():
    return render_template('user/index.html', data=users)

@app.route("/user/store", methods=["POST"])
def storeUser():
    id = "1"
    if len(users) != 0: #if list not empty get latest entry
        lastEntry = users[-1]
        id =  str(int(lastEntry['id']) + 1)
    users.append({ #create new user
        'id': id,
        'name': request.form.get('name')
    })
    return redirect(url_for('userIndex'))

@app.route("/user/<user_id>", methods=["GET"])
def deleteUser(user_id):
    for user in users:
        if user['id'] == user_id: # find effected user entry
            users.remove(user)
            break
    return redirect(url_for('userIndex'))

if __name__ == "__main__" :
    app.run(debug=True)