#!/usr/bin/python
""" holds class Review"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """This class is a representation of a review.
    
    Attributes:
        place_id: The ID of the place the review is made for
            - Optional: False
            - Type: String
            - Length: 60
        user_id: The ID of the user making the review
            - Optional: False
            - Type: String
            - Length: 60
        text: The review given to the place by a user
            - Optional: False
            - Type: String
            - Length: 1024

        Note: All attributes are optional when file storage is utilized.
    """
    if models.storage_t == 'db':
        __tablename__ = 'reviews'
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
