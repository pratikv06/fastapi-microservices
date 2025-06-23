# stdlib
import uuid
from typing import Any, Callable
from datetime import datetime

# third party
from pydantic import BaseModel
from sqlalchemy import UUID, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base


class BaseModelMixin(Base):
    """A mixin for adding common fields to SQLAlchemy models"""

    __abstract__ = True

    id: Mapped[UUID[str]] = mapped_column(
        String(32),
        primary_key=True,
        index=True,
        default=lambda: uuid.uuid4().hex,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )


class BaseSchemaMixin(BaseModel):
    """A mixin for serializing SQLAlchemy models to Pydantic models"""

    __abstract__ = True

    @classmethod
    def serialize(cls, record: Any, many: bool = False) -> list[Any] | Any:
        if many:
            return [cls.serialize(r) for r in record]

        data = {f: getattr(record, f) for f in cls.model_fields}
        return cls(**data)


class BaseFilterMixin(BaseModel):
    """A mixin for filtering SQLAlchemy models"""

    __abstract__ = True

    def apply_filters(self, model: Any, query: Any) -> Any:
        filter_operators: dict[str, Callable[[Any, Any], Any]] = {
            "eq": lambda col, val: col == val,
            "in": lambda col, val: col.in_(val),
            "gt": lambda col, val: col > val,
            "gte": lambda col, val: col >= val,
            "lt": lambda col, val: col < val,
            "lte": lambda col, val: col <= val,
            "neq": lambda col, val: col != val,
            "like": lambda col, val: col.like(f"%{val}%"),
            "ilike": lambda col, val: col.ilike(f"%{val}%"),
            "isnull": lambda col, val: (
                col.is_(None) if val is True else col.isnot(None)
            ),
            "istrue": lambda col, val: col.is_(True) if val is True else col.is_(False),
        }

        for key, value in self.model_dump(exclude_unset=True).items():
            if any(key.endswith(f"_{op}") for op in filter_operators):
                field, op = key.rsplit("_", 1)
                if hasattr(model, field) and op in filter_operators:
                    query = query.where(
                        filter_operators[op](getattr(model, field), value)
                    )
            elif hasattr(model, key):
                query = query.where(getattr(model, key) == value)
        return query
