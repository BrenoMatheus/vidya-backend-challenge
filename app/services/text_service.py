from app.repositories.text_repository import TextRepository


class TextService:
    def __init__(self, repository: TextRepository):
        self.repository = repository

    def create_text(self, data: dict) -> dict:
        if not data["text"].strip():
            raise ValueError("Texto não pode ser vazio")

        if data["type"] not in ["comment", "observation", "description"]:
            raise ValueError("Tipo de texto inválido")

        return self.repository.create(data)
