from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from zou.app import db
from zou.app.models.serializer import SerializerMixin
from zou.app.models.base import BaseMixin


class OutputFile(db.Model, BaseMixin, SerializerMixin):
    """
    Describe a file generated from a CG artist scene. It's the result of a
    publication.
    It is linked to a working file, an entity and a task type.
    """
    shotgun_id = db.Column(db.Integer())

    name = db.Column(db.String(250), nullable=False)
    extension = db.Column(db.String(10))
    revision = db.Column(db.Integer(), nullable=False)
    representation = db.Column(db.String(20), index=True)
    nb_elements = db.Column(db.Integer(), default=1)

    path = db.Column(db.String(400))

    description = db.Column(db.Text())
    comment = db.Column(db.Text())
    size = db.Column(db.Integer())
    checksum = db.Column(db.String(32))
    source = db.Column(db.String(40))

    canceled = db.Column(db.Boolean(), default=False, nullable=False)

    file_status_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("file_status.id"),
        nullable=False
    )
    entity_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("entity.id")
    )
    asset_instance_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("asset_instance.id"),
        index=True
    )
    output_type_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("output_type.id"),
        index=True
    )
    task_type_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("task_type.id"),
        index=True
    )
    person_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("person.id")
    )
    source_file_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("working_file.id"),
    )
    source_file = relationship(
        "WorkingFile",
        back_populates="outputs"
    )
    temporal_entity_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("entity.id"),
        default=None,
        nullable=True
    )

    __table_args__ = (
        db.UniqueConstraint(
            "name",
            "entity_id",
            "asset_instance_id",
            "output_type_id",
            "task_type_id",
            "temporal_entity_id",
            "representation",
            "revision",
            name="output_file_uc"
        ),
    )

    def __repr__(self):
        return "<OutputFile %s>" % self.id
