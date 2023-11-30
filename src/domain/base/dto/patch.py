from src.domain.base.dto.base import DTO


class PatchDTO(DTO):
    @property
    def updated_data(self) -> dict:
        model_dump = self.model_dump()
        new_data = {}

        for key, value in model_dump.items():
            if value is not None:
                new_data[key] = value

        return new_data
