# Webhook Events Processor
## Overview

This project simulates the ingestion and processing of HubSpot contact events (created/updated) through a webhook pipeline.
The workflow receives events in JSON format, validates duplicates, inserts/updates them into a SQLite database, and keeps track of contacts and their lifecycle.

## Project Structure
``` bash
├── DB_scheme.py        # Defines database schema (Contacts, Events)
├── DB_operations.py    # CRUD operations for contacts and events
├── Exercise.ipynb      # Notebook with processing logic and examples
├── eventcreate.json    # Example payload for "contact.created"
├── eventupdate.json    # Example payload for "contact.updated"
├── Hubspot.db          # SQLite database file
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Setup

1. Clone this repository:
```
git clone https://github.com/Gian-Nanni/OptimizerMedia.git
cd OptimizerMedia
```
2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Initialize the database:
```
python DB_scheme.py
```

## Usage
- Run the Jupyter Notebook to test event ingestion:
```
jupyter notebook Exercise.ipynb
```
- Insert/update contacts and events using the functions in DB_operations.py.

## Database Schema

- Contacts
  
  - `object_id`, `email`, `firstname`, `lastname`, `phone`, `lifecyclestage`, `utm_source`, `utm_medium`, `utm_campaign`

- Events
  - `event_id`, `event_type (created/updated)`, `occurred_at`, `processed_at`, `object_id (FK to contacts)`

## Example Workflow
1. Receive event payload (eventcreate.json / eventupdate.json).
2. Check if event already exists.
3. If event is new:
  - For contact.created: insert new contact (if not duplicated).
  - For contact.updated: update contact information.
4. Commit transaction to the database.

## Notes

- Duplicated events are ignored (could be logged separately).
- Basic schema simplification: UTM fields are kept inside contacts table for convenience.
- Concurrency handling not implemented (would require queueing or locking in production).
