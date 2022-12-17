from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

tasks = {}

class TaskResource(Resource):
    def get(self, task_id):
        return {task_id: tasks[task_id]}

    def put(self, task_id):
        tasks[task_id] = request.form['data']
        return {task_id: tasks[task_id]}

api.add_resource(TaskResource, '/<string:task_id>')

if __name__ == '__main__':
    app.run(debug=True)
