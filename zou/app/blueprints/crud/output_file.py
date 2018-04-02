from zou.app.models.output_file import OutputFile
from zou.app.models.entity import Entity
from zou.app.models.project import Project
from zou.app.services import user_service, entities_service

from .base import BaseModelsResource, BaseModelResource


class OutputFilesResource(BaseModelsResource):

    def __init__(self):
        BaseModelsResource.__init__(self, OutputFile)

    def check_read_permissions(self):
        return True

    def add_project_permission_filter(self, query):
        if user_service.is_current_user_manager():
            return query
        else:
            query = query \
                .join(Entity, Project) \
                .filter(user_service.related_projects_filter())
            return query


class OutputFileResource(BaseModelResource):

    def __init__(self):
        BaseModelResource.__init__(self, OutputFile)

    def check_read_permissions(self, instance):
        entity = entities_service.get_entity(instance["entity_id"])
        return user_service.check_project_access(entity["project_id"])