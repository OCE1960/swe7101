from .. import db
from .Module import Module
from .Staff import Staff

module_staff_m2m = db.Table(
    "module_staff",
    db.Column("module_id", db.ForeignKey(Module.id), primary_key=True),
    db.Column("staff_id", db.ForeignKey(Staff.id), primary_key=True),
)