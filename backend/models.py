from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base


class Message(Base):
    """Stores every contact-form submission."""

    __tablename__ = "messages"

    id       = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name     = Column(String(120), nullable=False)
    email    = Column(String(254), nullable=False, index=True)
    subject  = Column(String(255), nullable=False)
    message  = Column(Text,        nullable=False)
    sent_at  = Column(DateTime,    default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Message id={self.id} from='{self.name}' at={self.sent_at}>"
