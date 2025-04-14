from core.database.models import Project, db

class ProjectRepository:
    def create(self, name, description, target_amount):
        new_project = Project(name=name, description=description, target_amount=target_amount)
        db.session.add(new_project)
        db.session.commit()
        return new_project

    def get_by_id(self, project_id):
        return Project.query.get(project_id)

    def get_all(self):
        return Project.query.all()

    def update(self, project_id, name, description, target_amount):
        project = self.get_by_id(project_id)
        if project:
            project.name = name
            project.description = description
            project.target_amount = target_amount
            db.session.commit()
            return project
        return None

    def delete(self, project_id):
        project = self.get_by_id(project_id)
        if project:
            db.session.delete(project)
            db.session.commit()