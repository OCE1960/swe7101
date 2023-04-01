from .. import db


module_staff_m2m = db.Table(
    "module_staff",
    db.Column("modules_id",db.Integer, db.ForeignKey('modules.id'), index=True),
    db.Column("staffs_id", db.Integer, db.ForeignKey('staffs.id'), index=True),
)