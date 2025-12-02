# flask-cicd-demo
A student project for educational purposes: simple organizer app with unit tests and CI/CD workflow

## Installation

1. Clone and go to project:
```bash
git clone https://github.com/horacemtb/flask-cicd-demo.git
cd flask-ci-cd-demo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Try commands:

- create task:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"title":"Buy milk"}' http://localhost:8080/tasks
```

- get task:

```bash
curl http://localhost:8080/tasks/0
```

- add another task:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"title":"Study Japanese"}' http://localhost:8080/tasks
```

- set status:

```bash
curl -X PUT http://localhost:8080/tasks/0/complete
```

- show tasks by filter:

```bash
curl "http://localhost:8080/tasks?completed=true"
curl "http://localhost:8080/tasks?completed=false"
```

- show stats:

```bash
curl http://localhost:8080/stats
```

4. Run tests:

```bash
coverage run -m unittest src/tests.py
```