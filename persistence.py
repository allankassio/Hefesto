import os
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

class HefestoPersistence:
    def __init__(self):
        load_dotenv()

        creds_dict = {
            "type": os.getenv("GOOGLE_TYPE"),
            "project_id": os.getenv("GOOGLE_PROJECT_ID"),
            "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace("\\n", "\n"),
            "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
            "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_CERT"),
            "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_CERT_URL"),
            "universe_domain": os.getenv("GOOGLE_UNIVERSE_DOMAIN"),
        }

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(credentials)
        self.sheet = client.open("gdd_hefesto_dados").sheet1

    def salvar_gdd(self, session_id, pillar, mechanic, public, ggd_result):
        self.sheet.append_row([session_id, pillar, mechanic, public, ggd_result, "", "", "", "", ""])

    def salvar_code(self, session_id, code_result):
        try:
            cell = self.sheet.find(session_id)
            if cell:
                self.sheet.update_cell(cell.row, 6, code_result)
        except gspread.exceptions.CellNotFound:
            print(f"[HefestoPersistence] Sessão {session_id} não encontrada para salvar código.")

    def salvar_artefato(self, session_id, artifact_result):
        try:
            cell = self.sheet.find(session_id)
            if cell:
                self.sheet.update_cell(cell.row, 7, artifact_result)
        except gspread.exceptions.CellNotFound:
            print(f"[HefestoPersistence] Sessão {session_id} não encontrada para salvar artefato.")

    def marcar_gdd_baixado(self, session_id):
        self._marcar_download(session_id, 8)

    def marcar_codigo_baixado(self, session_id):
        self._marcar_download(session_id, 9)

    def marcar_artefato_baixado(self, session_id):
        self._marcar_download(session_id, 10)

    def _marcar_download(self, session_id, col):
        try:
            cell = self.sheet.find(session_id)
            if cell:
                self.sheet.update_cell(cell.row, col, "yes")
        except gspread.exceptions.CellNotFound:
            print(f"[HefestoPersistence] Sessão {session_id} não encontrada para marcar coluna {col}.")
