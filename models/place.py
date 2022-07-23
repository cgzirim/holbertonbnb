#!/usr/bin/python
""" holds class Place"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

if models.storage_t == "db":
    place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column(
            "place_id",
            String(60),
            ForeignKey("places.id", onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True,
        ),
        Column(
            "amenity_id",
            String(60),
            ForeignKey("amenities.id", onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True,
        ),
    )


class Place(BaseModel, Base):
    """This class is a representation of a place.
    
    Attributes:
        name: The name of the place.
            - Optional: False
            - Type: String
            - Length: <= 128

        city_id: The ID of the city the Place is located.
            - Optional: False
            - Type: String
            - Length: <= 60

        state_id: The ID of the state where the Place is located
            - Optional: False
            - Type: String
            - Length: <= 60

        number_rooms: The number of rooms in the Place
            - Optional: False
            - Type: Integer
            - Default: 0

        number_bathrooms: The number of bathrooms in the Place
            - Optional: False
            - Type: Integer
            - Default: 0

        max_guest: Maximum number of guests that can stay in the Place
            - Optional: False
            - Type: Integer
            - Default: 0

        price_by_night: Price of the Place by night
            - Optional: False
            - Type: Integer
            - Default: 0

        description: Description of the Place
            - Optional: True
            - Type: String
            - Length: <= 1024

        latitude: Latitude of the Place
            - Optional: True
            - Type: Float
        
        longitude: Longitude of the Place
            - Optional: True
            - Type: Float
        
        Note: All attributes are optional when file storage is utilized.
    """

    if models.storage_t == "db":
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
            "Review", backref="place", cascade="all, delete, delete-orphan"
        )
        amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":

        @property
        def reviews(self):
            """getter attribute returns the list of Review instances"""
            from models.review import Review

            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """getter attribute returns the list of Amenity instances"""
            from models.amenity import Amenity

            amenity_list = []
            all_amenities = models.storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.place_id == self.id:
                    amenity_list.append(amenity)
            return amenity_list
