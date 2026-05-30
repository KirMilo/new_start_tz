from models import Document, Version, Parent


class Workspace:
    def __init__(self, raw_index: dict[str, dict[str, dict[str, list[str]]]]):
        self.index: dict[str, Document] = self.build_index(raw_index)

    @staticmethod
    def build_index(raw: dict[str, dict[str, dict[str, list[str]]]]):
        index = {}
        for key, value in raw.items():
            index[key] = Document(
                name=key,
                versions=[Version(number=version) for version in value],
            )

        for document, raw_versions in zip(index.values(), raw.values()):
            for doc_version, raw_version_parents in zip(document.versions, raw_versions.values()):
                for doc_name, versions in raw_version_parents.get("parents", {}).items():
                    doc_version.parents.append(
                        Parent(
                            document=index[doc_name],
                            versions=[version for version in index[doc_name].versions if version.number in versions],
                        )
                    )

        return index

    def model_dumps(self) -> dict[str, dict[str, dict[str, list[str]]]]:
        result = {}
        for document in self.index.values():
            result.update(document.model_dumps())
        return result

    def update_index(self, name: str, vers_num: str, parent: str = None, parent_version: str = None):
        if name in self.index:  # Проверка наличия документа в индексе
            document = self.index[name]
            for v in document.versions:  # Поиск версии в индексе
                if v.number == vers_num:  # Если версия существует
                    version = v
                    break
            else:   # Если версия не существует
                version = Version(number=vers_num)
                document.versions.append(version)
        else:   # Если документа нет в индексе
            document = Document(name=name)
            self.index[name] = document
            version = Version(number=vers_num)
            document.versions.append(version)

        if parent is not None and parent in self.index:
            parent_doc = self.index[parent]
            if parent_version:
                for v in parent_doc.versions:  # Проверяем существует ли указанная версия
                    if v.number == parent_version:
                        par_vers = v
                        break
                else:  # Если не существует
                    raise ValueError(f"Parent version with number {parent_version} not found")

                for p in version.parents:  # Проверяем не существует ли этот родитель у документа
                    if p.document.name == parent:
                        p.versions.append(par_vers)
                        break
                else:   # Если не существует создаем
                    version.parents.append(Parent(document=parent_doc, versions=[par_vers]))
        else:   # Если родитель не найден
            raise ValueError(f"Parent with name {parent} not found")

    def delete_document(self, name: str):
        if name in self.index:
            document = self.index[name]
            document.delete()
            self.refresh_index()

    def delete_version(self, document: str, version: str):
        if document in self.index:
            for v in self.index[document].versions:
                if v.number == version:
                    v.delete()
                    break
            else:
                raise ValueError(f"Document's version with number {version} not found")
            self.refresh_index()

    def refresh_index(self):
        self.index = self.build_index(self.model_dumps())
