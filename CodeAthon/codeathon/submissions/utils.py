import os
import secrets
from flask import url_for, current_app


''' def save_code_file(form_code):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_code.filename)
    code_fn = random_hex + f_ext
    code_path = os.path.join(
        current_app.root_path, "static/code_submissions", code_fn
    )

    i = .open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn '''
