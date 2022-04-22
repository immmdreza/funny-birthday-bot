from .shared_types import T
from typing import Generic, TYPE_CHECKING

if TYPE_CHECKING:
    from .update_manager import UpdateManager


class UpdateContext(Generic[T]):
    def __init__(self, update_manager: UpdateManager, update: T) -> None:
        super().__init__()
        self._update_manager = update_manager
        self._update = update

    @property
    def update(self) -> T:
        return self._update

    @property
    def update_manager(self) -> UpdateManager:
        return self._update_manager
