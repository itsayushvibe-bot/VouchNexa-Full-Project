from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, BigInteger, Boolean, DateTime, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)  # Telegram User ID
    username = Column(String(64), nullable=True)
    first_name = Column(String(128), nullable=True)
    is_banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"

    id = Column(String(64), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), default="Digital Vouchers")
    price_paise = Column(Integer, nullable=False)  # Stored in integer paise (e.g. 50000 = ₹500)
    is_active = Column(Boolean, default=True)
    low_stock_threshold = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)

    vouchers = relationship("Voucher", back_populates="product")

class Voucher(Base):
    __tablename__ = "vouchers"

    id = Column(String(64), primary_key=True)
    product_id = Column(String(64), ForeignKey("products.id"), nullable=False)
    code = Column(Text, nullable=False)
    status = Column(String(20), default="AVAILABLE")  # AVAILABLE, RESERVED, DELIVERED, WITHDRAWN
    order_id = Column(String(64), nullable=True)
    delivered_to = Column(BigInteger, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    delivered_at = Column(DateTime, nullable=True)

    product = relationship("Product", back_populates="vouchers")

class Order(Base):
    __tablename__ = "orders"

    id = Column(String(64), primary_key=True)  # e.g. VN-12345
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    user_name = Column(String(128))
    user_handle = Column(String(128))
    product_id = Column(String(64), ForeignKey("products.id"), nullable=False)
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    amount_paise = Column(Integer, nullable=False)
    upi_reference = Column(String(128), nullable=True, unique=True)
    status = Column(String(30), default="PENDING_PAYMENT")  # PENDING_PAYMENT, AWAITING_REVIEW, APPROVED, REJECTED
    rejection_reason = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)

class RecoveryRequest(Base):
    __tablename__ = "recovery_requests"

    id = Column(String(64), primary_key=True)
    order_id = Column(String(64), ForeignKey("orders.id"), nullable=False)
    user_id = Column(BigInteger, nullable=False)
    reason = Column(String(255), nullable=False)
    explanation = Column(Text, nullable=False)
    status = Column(String(20), default="OPEN")  # OPEN, APPROVED, REJECTED, CLOSED
    admin_notes = Column(Text, nullable=True)
    replacement_code = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(String(64), primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    user_name = Column(String(128))
    message = Column(Text, nullable=False)
    status = Column(String(20), default="OPEN")
    created_at = Column(DateTime, default=datetime.utcnow)
