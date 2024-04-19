from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    vendor_sweets = relationship("VendorSweet", back_populates="sweet", cascade="all, delete")

    vendors = relationship(
        "Vendor",
        secondary="vendor_sweets",
        back_populates="sweets"
    )

    def __repr__(self):
        return f'<Sweet {self.id}>'


class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    vendor_sweets = relationship("VendorSweet", back_populates="vendor", cascade="all, delete")

    sweets = relationship(
        "Sweet",
        secondary="vendor_sweets",
        back_populates="vendors"
    )

    def __repr__(self):
        return f'<Vendor {self.id}>'


class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    vendor_id = db.Column(db.Integer, ForeignKey('vendors.id'), nullable=False)
    sweet_id = db.Column(db.Integer, ForeignKey('sweets.id'), nullable=False)

    vendor = relationship("Vendor", back_populates="vendor_sweets")
    sweet = relationship("Sweet", back_populates="vendor_sweets", cascade="all, delete")

    @validates('price')
    def validate_price(self, key, price):
        if price is None:
            raise ValueError("Price must have a value.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        return price

    def __repr__(self):
        return f'<VendorSweet {self.id}>'
