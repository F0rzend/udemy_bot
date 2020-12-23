import uuid


def is_valid_uuid(value, version: int = 4):
    version = version if not version else int(version)

    if version not in range(1, 5):
        raise ValueError("Unknown UUID version!")

    try:
        uuid.UUID(str(value), version=version)
        return True
    except ValueError:
        return False
