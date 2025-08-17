from sqlalchemy import create_engine, Column, Integer, String, BigInteger, DateTime, Enum, ForeignKey, TIMESTAMP, func, text
from sqlalchemy.orm import declarative_base, relationship, Session
import enum

# Base class for SQLAlchemy models
Base = declarative_base()

# Table: contacts
class Contact(Base):
    __tablename__ = 'contacts'

    object_id = Column(BigInteger, primary_key=True)    # Contact ID
    email = Column(String(100), unique=True)            # Email (unique)
    firstname = Column(String(50))                      # First name
    lastname = Column(String(50))                       # Last name
    phone = Column(String(30))                          # Phone number
    lifecyclestage = Column(String(30))                 # Lifecycle stage
    utm_source = Column(String(50))                     # UTM source
    utm_medium = Column(String(50))                     # UTM medium
    utm_campaign = Column(String(100))                  # UTM campaign

    # Relationship: one contact -> many events
    events = relationship("Event", back_populates="contact")


# Table: events
class Event(Base):
    __tablename__ = 'events'

    event_id = Column(String(50), primary_key=True)                                     # Event ID
    event_type = Column(Enum('contact.created', 'contact.updated'), nullable=False)     # Event type
    occurred_at = Column(DateTime(timezone=True), nullable=False)                       # Event timestamp    
    processed_at = Column(TIMESTAMP, server_default=func.current_timestamp())           # Processing timestamp
    object_id = Column(BigInteger, ForeignKey('contacts.object_id'), nullable=False)    # FK to contacts
    
    # Relationship: event belongs to one contact
    contact = relationship("Contact", back_populates="events")


# Create DB engine and tables
if __name__ == "__main__":
    engine = create_engine('sqlite:///Hubspot.db')
    Base.metadata.create_all(engine)
