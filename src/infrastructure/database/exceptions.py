class DatabaseError(Exception):
    """Ошибка базы данной"""


class CommitError(DatabaseError):
    """Ошибка при коммите"""


class RollbackError(DatabaseError):
    """Ошибка при откате"""
