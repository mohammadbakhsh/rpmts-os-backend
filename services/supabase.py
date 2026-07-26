from supabase import create_client, Client
from config import Config

class SupabaseService:
    def __init__(self):
        self.client: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

    def get_client(self) -> Client:
        return self.client

    def get_user(self, token: str):
        try:
            return self.client.auth.get_user(token)
        except:
            return None

    def get_user_id(self, token: str):
        user = self.get_user(token)
        return user.user.id if user else None

    def query(self, table: str):
        return self.client.table(table)