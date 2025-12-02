import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import app as tested_app
import json

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        tested_app.app.config['TESTING'] = True
        self.app = tested_app.app.test_client()
        tested_app.tasks.clear()
    
    def tearDown(self):
        tested_app.tasks.clear()
    
    def test_home_endpoint(self):
        r = self.app.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data.decode(), 'Task Organizer API')
    
    def test_get_empty_tasks(self):
        """Get empty tasks"""
        r = self.app.get('/tasks')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json, [])
    
    def test_create_task(self):
        """Create task"""
        task_data = {'title': 'Купить молоко', 'description': '1 л'}
        r = self.app.post('/tasks', 
                         content_type='application/json',
                         data=json.dumps(task_data))
        
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json['title'], 'Купить молоко')
        self.assertEqual(r.json['completed'], False)
        self.assertEqual(r.json['id'], 0)
    
    def test_create_task_without_title(self):
        """Create task without title"""
        task_data = {'description': '2 л'}
        r = self.app.post('/tasks',
                         content_type='application/json',
                         data=json.dumps(task_data))
        
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json['error'], 'Invalid task data')
    
    def test_get_task_by_id(self):
        """Get specific task"""
        task_data = {'title': 'Купить молоко'}
        self.app.post('/tasks',
                     content_type='application/json',
                     data=json.dumps(task_data))

        r = self.app.get('/tasks/0')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json['title'], 'Купить молоко')
    
    def test_get_nonexistent_task(self):
        """Get task that doesn't exist"""
        r = self.app.get('/tasks/999')
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json['error'], 'Task not found')
    
    def test_complete_task(self):
        """Mark task as completed"""
        task_data = {'title': 'Купить молоко'}
        self.app.post('/tasks',
                     content_type='application/json',
                     data=json.dumps(task_data))

        r = self.app.put('/tasks/0/complete')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json['completed'], True)
    
    def test_filter_tasks_by_completion(self):
        """Filter tasks by status"""
        self.app.post('/tasks',
                     content_type='application/json',
                     data=json.dumps({'title': 'Купить молоко'}))
        self.app.post('/tasks',
                     content_type='application/json',
                     data=json.dumps({'title': 'Выполнить задание'}))
        
        self.app.put('/tasks/0/complete')
        
        r = self.app.get('/tasks?completed=true')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json), 1)
        self.assertEqual(r.json[0]['title'], 'Купить молоко')

        r = self.app.get('/tasks?completed=false')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json), 1)
        self.assertEqual(r.json[0]['title'], 'Выполнить задание')
    
    def test_get_stats(self):
        """Get stats"""
        self.app.post('/tasks',
                     content_type='application/json',
                     data=json.dumps({'title': 'Купить молоко'}))
        self.app.post('/tasks',
                     content_type='application/json',
                     data=json.dumps({'title': 'Выполнить задание'}))

        self.app.put('/tasks/0/complete')

        r = self.app.get('/stats')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json['total_tasks'], 2)
        self.assertEqual(r.json['completed_tasks'], 1)
        self.assertEqual(r.json['pending_tasks'], 1)
    
    def test_invalid_json_post(self):
        """Post invalid request"""
        r = self.app.post('/tasks',
                         content_type='application/json',
                         data='some data')
        self.assertEqual(r.status_code, 400)

if __name__ == '__main__':
    unittest.main()
