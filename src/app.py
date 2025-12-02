from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []

def validate_task_data(data: dict) -> bool:
    """Validate task data structure"""
    if not isinstance(data, dict):
        return False
    
    if not data.get('title') or not isinstance(data['title'], str):
        return False

    if data.get('description') and not isinstance(data['description'], str):
        return False
    
    if data.get('completed') and not isinstance(data['completed'], bool):
        return False
    
    return True

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with basic info"""
    return 'Task Organizer API'

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks or filter by status"""
    completed = request.args.get('completed')
    
    if completed is not None:
        try:
            completed_bool = completed.lower() == 'true'
            filtered_tasks = [task for task in tasks if task.get('completed') == completed_bool]
            return jsonify(filtered_tasks)
        except:
            return jsonify({'error': 'Invalid parameter'}), 400
    
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by task_id"""
    if task_id < 0 or task_id >= len(tasks):
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(tasks[task_id])

@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    if not request.json:
        return jsonify({'error': 'No data provided'}), 400
    
    if not validate_task_data(request.json):
        return jsonify({'error': 'Invalid task data'}), 400
    
    task = {
        'id': len(tasks),
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'completed': request.json.get('completed', False)
    }
    
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    """Mark task as completed"""
    if task_id < 0 or task_id >= len(tasks):
        return jsonify({'error': 'Task not found'}), 404
    
    tasks[task_id]['completed'] = True
    return jsonify(tasks[task_id])

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get statistics about tasks"""
    total = len(tasks)
    completed = sum(1 for task in tasks if task.get('completed', False))
    pending = total - completed
    
    return jsonify({
        'total_tasks': total,
        'completed_tasks': completed,
        'pending_tasks': pending
    })

def main():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()
