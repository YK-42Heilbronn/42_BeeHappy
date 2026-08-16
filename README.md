# BeeHappy — Hive wellbeing prediction & analysis

Project from Bildung Campus and Arkadia GmbH to predict and analyse bee-hive wellbeing using sensor data from hives.

## What this is
BeeHappy ingests time-series sensor data from beehives, parses and normalizes it, stores it in a database, and provides utility scripts to update hive metadata and run monitoring/collection jobs. It's intended for researchers and developers working on beehive monitoring, analytics and simple prediction pipelines.

### Stack
- Language(s): Python (primary), Dockerfile (for containerization)
- Framework / runtime: Python 3.x (requirements pinned in `requirements.txt`)
- Notable libraries: pandas, numpy, psycopg2-binary, python-dotenv, requests

## How it's organized
Top-level layout:
```
Dockerfile                 # container image build
docker-compose.yml         # compose for local development / services
requirements.txt           # Python dependencies
src/
  run.py                   # entry / runner script
  s1_data/                 # sample/input data and schema files
    beehives_sensors_v2.json
    schema.txt
    state_vars.json
  s2_configure/            # configuration & monitoring helpers
    config.py
    db.py
    monitor.py
  s3_db/                   # database scripts (connect, parse, create schema, update tables)
    a1_connect_fetch.py
    a2_parsing_data.py
    a3_json_to_triplequote.py
    a4_meta_data.py
    a5_measured_data.py
    a98_db_beehives_update.py
    a99_db_schema_creation.py
  s4_collect/              # data collection & table-fill scripts
    b1_fill_sensor_node_tables.py
    b2_data_collection.py
  utils/
    db.py                  # shared DB utilities
tests/                     # unit / integration tests
  test.py
  test_collect.py
  test_db_a1-a5.py
  test_db_beehives_update.py
```

How it fits together:
- s1_data contains example sensor payloads and a schema; use these as sample input.
- s2_configure holds configuration and connection helpers used across scripts.
- s3_db contains a sequence of scripts: connect & fetch, parse, convert JSON, generate metadata, and create/update DB schema and tables.
- s4_collect implements higher-level collection and table-filling workflows.
- `src/run.py` ties pieces together for common workflows (see Usage).

## Quick start — local (Python)
1. Clone the repo
2. Create a virtual environment and install dependencies
3. Configure environment variables (database connection, etc.)
4. Run the main script or individual modules

Example commands:
```bash
git clone https://github.com/YK-42Heilbronn/42_BeeHappy.git
cd 42_BeeHappy
python -m venv .venv
source .venv/bin/activate            # or .venv\Scripts\activate on Windows
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the main entry (project includes `src/run.py` as the runner):
```bash
python src/run.py
```

Run a specific DB setup or update script:
```bash
python src/s3_db/a99_db_schema_creation.py    # create DB schema/tables
python src/s3_db/a98_db_beehives_update.py   # update beehives metadata/tables
```

Run collection workflow:
```bash
python src/s4_collect/b2_data_collection.py
```

Run tests:
```bash
python -m pytest -q tests/
```

## Quick start — Docker
Build and run via Docker:
```bash
docker build -t beehappy .
docker run --env-file .env -v $(pwd)/src/s1_data:/app/src/s1_data beehappy
```

Or use docker-compose:
```bash
docker-compose up --build
```
(Adjust `docker-compose.yml` and `.env` as needed.)

## Configuration / Environment
Look at `src/s2_configure/config.py` and `src/s2_configure/db.py` for supported environment variables and how DB connections are established. Typical variables to provide:
- DATABASE_URL or individual DB_* variables (host, port, user, password, dbname)
- Any API keys or endpoints used by collection scripts
- Optionally a `.env` file parsed by python-dotenv

## Data & sample files
- Sample sensor data: `src/s1_data/beehives_sensors_v2.json`
- Schema/field documentation: `src/s1_data/schema.txt`
- State variables: `src/s1_data/state_vars.json`

These are useful for local development and tests.

## Tests
Unit / integration tests are under `tests/`. Run them with pytest:
```bash
python -m pytest -q tests/
```
Review failing tests to see expected behavior for DB and collection scripts.

## Contributing
- Open an issue describing the feature or bug.
- Create a small, focused branch and open a pull request with tests for behavioral changes.
- Follow the existing style and module layout: configuration -> parsing -> DB -> collection.

## Troubleshooting tips
- If DB connections fail, confirm env vars and run `a99_db_schema_creation.py` to create required schema.
- Use sample file `src/s1_data/beehives_sensors_v2.json` to validate parsing scripts (`a2_parsing_data.py`, `a3_json_to_triplequote.py`).
- Logs or debug prints are available in the monitor/config modules — check `src/s2_configure/monitor.py`.

## License
Specify license here (add LICENSE file to repo if missing). If this is internal or proprietary, note that instead.

## Contact
For project questions contact the maintainers listed in the repository or the organization (Arkadia GmbH / Bildung Campus).

## Try asking
- "Which environment variables does `src/s2_configure/config.py` expect and what are their default values?"
- "What tables does `src/s3_db/a99_db_schema_creation.py` create and what are the key columns?"
- "How can I run `b2_data_collection.py` to ingest only the sample `src/s1_data/beehives_sensors_v2.json` file for local testing?"
