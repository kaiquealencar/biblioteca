import os
from werkzeug.utils import secure_filename
from flask import current_app
from uuid import uuid4


class ServiceImage:

    @staticmethod
    def salvar_image(file, nome_diretorio: str) -> str:
        if not file:
            return None

        filename = secure_filename(file.filename)
        ext = filename.rsplit(".", 1)[-1]

        novo_nome = f"{uuid4().hex}.{ext}"

        upload_path = os.path.join(
            current_app.root_path,
            "static",
            "uploads",
            nome_diretorio
        )

        os.makedirs(upload_path, exist_ok=True)

        file.save(os.path.join(upload_path, novo_nome))

        return novo_nome
