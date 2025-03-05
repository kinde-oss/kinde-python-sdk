# # postgres_storage.py
# from typing import Dict, Optional
# import psycopg2
# from .storage_interface import StorageInterface

# class PostgresStorage(StorageInterface):
#     def __init__(self, host: str, port: int, database: str, user: str, password: str):
#         self.connection = psycopg2.connect(
#             host=host, port=port, database=database, user=user, password=password
#         )

#     def get(self, key: str) -> Optional[Dict]:
#         """Retrieve data associated with the given key."""
#         cursor = self.connection.cursor()
#         cursor.execute("SELECT value FROM tokens WHERE key = %s", (key,))
#         result = cursor.fetchone()
#         return json.loads(result[0]) if result else None

#     def set(self, key: str, value: Dict) -> None:
#         """Store data associated with the given key."""
#         cursor = self.connection.cursor()
#         cursor.execute(
#             "INSERT INTO tokens (key, value) VALUES (%s, %s) ON CONFLICT (key) DO UPDATE SET value = %s",
#             (key, json.dumps(value), json.dumps(value)),
#         )
#         self.connection.commit()

#     def delete(self, key: str) -> None:
#         """Delete data associated with the given key."""
#         cursor = self.connection.cursor()
#         cursor.execute("DELETE FROM tokens WHERE key = %s", (key,))
#         self.connection.commit()