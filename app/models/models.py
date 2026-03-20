"""
Database Models
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid

Base = declarative_base()


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    API = "api"


class ModelStatus(str, Enum):
    PENDING = "pending"
    TRAINING = "training"
    ACTIVE = "active"
    FAILED = "failed"
    ARCHIVED = "archived"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    models = relationship("MLModel", back_populates="owner")
    predictions = relationship("Prediction", back_populates="user")
    api_keys = relationship("ApiKey", back_populates="user")


class MLModel(Base):
    __tablename__ = "ml_models"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    version = Column(String(50), default="1.0.0")
    framework = Column(String(50))  # tensorflow, pytorch, sklearn
    status = Column(SQLEnum(ModelStatus), default=ModelStatus.PENDING)
    
    # Model metadata
    input_schema = Column(JSONB)
    output_schema = Column(JSONB)
    hyperparameters = Column(JSONB)
    metrics = Column(JSONB)
    
    # File storage
    storage_path = Column(String(500))
    file_size_bytes = Column(Integer)
    checksum = Column(String(64))
    
    # Foreign keys
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    trained_at = Column(DateTime)
    
    # Relationships
    owner = relationship("User", back_populates="models")
    predictions = relationship("Prediction", back_populates="model")


class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Input/Output
    input_data = Column(JSONB, nullable=False)
    output_data = Column(JSONB)
    confidence = Column(Float)
    
    # Performance
    latency_ms = Column(Float)
    
    # Status
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING)
    error_message = Column(Text)
    
    # Foreign keys
    model_id = Column(UUID(as_uuid=True), ForeignKey("ml_models.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    model = relationship("MLModel", back_populates="predictions")
    user = relationship("User", back_populates="predictions")


class ApiKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key_hash = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime)
    expires_at = Column(DateTime)
    
    # Rate limiting
    rate_limit = Column(Integer, default=100)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")


class CeleryTask(Base):
    __tablename__ = "celery_tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(String(255), unique=True, nullable=False, index=True)
    task_name = Column(String(255), nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING)
    
    # Task data
    args = Column(JSONB)
    kwargs = Column(JSONB)
    result = Column(JSONB)
    error = Column(Text)
    
    # Performance
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    retries = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
