from dataclasses import dataclass, field


class WorkspaceComponent:
    _exist: bool = field(default=True)

    def delete(self) -> None:
        self._exist = False


@dataclass
class Parent(WorkspaceComponent):
    document: "Document"
    versions: list["Version"] = field(default_factory=list)

    def model_dumps(self) -> dict[str, list[str]]:
        if self._exist and self.versions:
            return {
                self.document.name: [version.number for version in self.versions]
            }
        return {}


@dataclass
class Version(WorkspaceComponent):
    number: str
    parents: list["Parent"] = field(default_factory=list)

    def model_dumps(self) -> dict[str, dict[str, dict[str, list[str]]]]:  #
        if self._exist:
            parents = {}
            result = {self.number: {"parents": parents}}
            for parent in self.parents:
                parents.update(parent.model_dumps())
            return result
        return {}

    def delete(self):
        self._exist = False


@dataclass
class Document(WorkspaceComponent):
    name: str
    versions: list["Version"] = field(default_factory=list)

    def model_dumps(self) -> dict[str, dict[str, dict[str, list[str]]]]:
        if self._exist:
            versions = {}
            for version in self.versions:
                versions.update(version.model_dumps())
            return {self.name: versions}
        return {}

    def delete(self):
        for version in self.versions:
            version.delete()
        return super().delete()
