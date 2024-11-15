
# Project 11 OCR (Vadim333)

This project is a **reservation platform for strength competitions** organized by the company **Güdlft**.

The goal is to **fix bugs and errors** in the existing project, [Python_Testing](https://github.com/OpenClassrooms-Student-Center/Python_Testing), and to **add new features**. Each fix or feature is implemented in a dedicated branch and accompanied by tests using **Pytest** and **Locust**.

---

## Project Setup

### Steps for Windows:
```bash
git clone https://github.com/Vadim333/gudlft.git

cd gudlft
python -m venv env
env\Scriptsctivate

pip install -r requirements.txt
```

### Steps for MacOS and Linux:
```bash
git clone https://github.com/Vadim333/gudlft.git

cd gudlft
python3 -m venv env
source env/bin/activate

pip install -r requirements.txt
```

---

## Usage

### Start the Flask server:
```bash
$env:FLASK_APP = "server.py"  # For Windows
flask run
```

- Access the site at the following address: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Tests

### Unit and Integration Tests
Unit and integration tests are run using [Pytest](https://docs.pytest.org/en/6.2.x/index.html) (version 6.2.5).

To run all tests, use the command:
```bash
pytest tests
```

A coverage report is generated using [Coverage](https://coverage.readthedocs.io/en/6.3.1/) (version 6.3.1). Run the following commands:
```bash
coverage run -m pytest tests
coverage report
```

---

### Performance Testing
Performance testing is handled using [Locust](https://locust.io) (version 2.7.2).

To launch the performance test server, run:
```bash
locust -f tests/performance_tests/locustfile.py
```

Visit [http://localhost:8089](http://localhost:8089) to configure test options. Use the default host address: [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

---

## Reports

Screenshots of the latest test reports are available in the `reports` folder:

- [Pytest Report](reports/tests_report.png) (all tests passed)
- [Coverage Report](reports/coverage.PNG) (100% coverage)
- [Locust Performance Report](reports/locust_report.html) (15 users, 1 user per second)
