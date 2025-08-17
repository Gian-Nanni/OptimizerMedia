import pandas as pd
from sqlalchemy.orm import Session
from DB_scheme import Event, Contact

# Check if event already exists
def is_event_exists(event_id, engine):
    """
    Check if an event already exists in the database.

    Args:
        event_id (str): The unique ID of the event to check.
        engine (Engine): SQLAlchemy engine for the database connection.

    Returns:
        bool: True if the event exists, False otherwise.
    """
    query = f"SELECT 1 FROM events WHERE event_id = '{event_id}' LIMIT 1"
    return pd.read_sql_query(query, con=engine).shape[0] > 0


# Check if contact already exists
def is_contact_exists(object_id, engine):
    """
    Check if a contact already exists in the database.

    Args:
        object_id (int): The contact ID to check.
        engine (Engine): SQLAlchemy engine for the database connection.

    Returns:
        bool: True if the contact exists, False otherwise.
    """
    query = "SELECT 1 FROM contacts WHERE object_id = ? LIMIT 1"
    return pd.read_sql_query(query, con=engine, params=(object_id,)).shape[0] > 0


# Insert new event
def insert_event(row, engine):
    """
    Insert a new event into the database.

    Args:
        row (pd.Series or dict): Row containing event data with keys:
            - eventId (str)
            - eventType (str)
            - occurredAt (datetime)
            - objectId (int)
        engine (Engine): SQLAlchemy engine for the database connection.

    Returns:
        None
    """
    session = Session(bind=engine)

    new_event = Event(
        event_id=row['eventId'],
        event_type=row['eventType'],
        occurred_at=row['occurredAt'],
        object_id=row['objectId']
    )

    session.add(new_event)
    session.commit()
    session.close()


# Insert new contact
def insert_contact(row, engine):
    """
    Insert a new contact into the database.

    Args:
        row (pd.Series or dict): Row containing contact data with keys:
            - objectId (int)
            - email (str)
            - firstname (str)
            - lastname (str)
            - phone (str)
            - lifecyclestage (str)
        engine (Engine): SQLAlchemy engine for the database connection.

    Returns:
        None
    """
    session = Session(bind=engine)

    new_contact = Contact(
        object_id=row['objectId'],
        email=row.get('email'),
        firstname=row.get('firstname'),
        lastname=row.get('lastname'),
        phone=row.get('phone'),
        lifecyclestage=row.get('lifecyclestage')
    )

    session.add(new_contact)
    session.commit()
    session.close()

# Update existing contact
def update_contact(row, engine):
    """
    Update an existing contact in the database with new data.

    Args:
        row (pd.Series or dict): Row containing updated contact data with keys:
            - objectId (int) (required)
            - email (str, optional)
            - firstname (str, optional)
            - lastname (str, optional)
            - phone (str, optional)
            - lifecyclestage (str, optional)
        engine (Engine): SQLAlchemy engine for the database connection.

    Returns:
        None
    """
    session = Session(bind=engine)

    contact = session.query(Contact).filter(Contact.object_id == row['objectId']).first()
    if contact:
        contact.email = row.get('email', contact.email)
        contact.firstname = row.get('firstname', contact.firstname)
        contact.lastname = row.get('lastname', contact.lastname)
        contact.phone = row.get('phone', contact.phone)
        contact.lifecyclestage = row.get('lifecyclestage', contact.lifecyclestage)
        session.commit()
        
    session.close()