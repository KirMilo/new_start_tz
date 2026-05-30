import json

from workspace import Workspace


### 1.	Нужно создать document4 (версия 1). Этот документ должен быть дочерним для document3 (версия 3).
### 2.	Нужно полностью удалить версию 1 из документа document1. Исходить из правила, что при удалении родительского документа требуется удалять его упоминание в дочернем.


def main():
    with open("test.json") as f:
        index = json.load(f)

    workspace = Workspace(index)
    print(workspace.model_dumps())
    workspace.update_index("document4", "1", "document3", "3")
    print(workspace.model_dumps())
    workspace.delete_version("document1", "1")
    print(workspace.model_dumps())

    # with open("updated.json", "w") as f:
    #     json.dump(workspace.model_dumps(), f, indent=4)


if __name__ == "__main__":
    main()
