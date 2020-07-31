class ProjectError(Exception):
    pass


class SpecError(ProjectError):
    pass


class MissingDoc(SpecError):
    pass


class UnmatchDoc(SpecError):
    pass
