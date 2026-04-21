import requests
import json

class BotMonitorObject:

    def __init__(self, api_url, api_key, bot_id):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.bot_id = bot_id
        self.headers = {
            "x-api-key": self.api_key,
            "x-bot-id": self.bot_id,
            "Content-Type": "application/json",
        }
        self.connected = False

        try:
            r = requests.get(f"{self.api_url}/api/check", headers=self.headers)
            if r.status_code == 200:
                data = r.json()
                if data.get("success"):
                    self.connected = True
        except:
            self.connected = False

    def sendLog(self, level, message, payload=None, durationMs=None):
        body = {
            "level": level,
            "message": message
        }
        if payload is not None:
            body["payload"] = payload
        if durationMs is not None:
            body["durationMs"] = durationMs

        r = requests.post(f"{self.api_url}/api/logs", headers=self.headers, json=body)
        return r.json()

    def sendData(self, table, row, columns=None):
        body = {
            "table": table,
            "row": row
        }
        if columns is not None:
            body["columns"] = columns

        r = requests.post(f"{self.api_url}/api/data", headers=self.headers, json=body)
        return r.json()

    def uploadDatabase(self, db_path, primary_keys=None, batch_size=500):
        """
        Lee un archivo SQLite completo y envia cada tabla al backend en lotes.

        Args:
            db_path: Ruta al archivo .sqlite local.
            primary_keys: Lista de columnas que actuan como PK. Si la lista
                esta contenida en las columnas de la tabla, se usa; si no, se
                hace fallback a los PK declarados en el schema SQLite.
            batch_size: Filas por request HTTP (default 500).

        Returns:
            Dict con resumen: {"tables": [...], "totalInserted": N, "totalSkipped": M}
        """
        import sqlite3
        import base64

        primary_keys = primary_keys or []
        summary = {"tables": [], "totalInserted": 0, "totalSkipped": 0}

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        try:
            table_rows = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            ).fetchall()
            table_names = [r[0] for r in table_rows]

            for table in table_names:
                info = conn.execute('PRAGMA table_info("' + table + '")').fetchall()
                col_names = [c["name"] for c in info]
                columns = [
                    {
                        "name": c["name"],
                        "type": (c["type"] or "TEXT").upper(),
                        "label": c["name"],
                    }
                    for c in info
                ]

                # PKs efectivos: lista global si todas las columnas existen, sino fallback al schema SQLite
                if primary_keys and all(pk in col_names for pk in primary_keys):
                    effective_pks = list(primary_keys)
                else:
                    effective_pks = [c["name"] for c in info if c["pk"] and c["pk"] > 0]

                inserted = 0
                skipped = 0
                total = 0
                batch = []

                for r in conn.execute('SELECT * FROM "' + table + '"'):
                    row = {}
                    for k in col_names:
                        v = r[k]
                        if isinstance(v, (bytes, bytearray)):
                            v = base64.b64encode(v).decode("ascii")
                        row[k] = v
                    batch.append(row)
                    if len(batch) >= batch_size:
                        resp = self._postBulk(table, columns, batch, effective_pks)
                        inserted += resp.get("inserted", 0)
                        skipped += resp.get("skipped", 0)
                        total += len(batch)
                        batch = []

                if batch:
                    resp = self._postBulk(table, columns, batch, effective_pks)
                    inserted += resp.get("inserted", 0)
                    skipped += resp.get("skipped", 0)
                    total += len(batch)

                summary["tables"].append({
                    "table": table,
                    "inserted": inserted,
                    "skipped": skipped,
                    "total": total,
                    "primaryKeys": effective_pks,
                })
                summary["totalInserted"] += inserted
                summary["totalSkipped"] += skipped
        finally:
            conn.close()

        return summary

    def _postBulk(self, table, columns, rows, primaryKeys):
        body = {
            "table": table,
            "columns": columns,
            "rows": rows,
            "primaryKeys": primaryKeys,
        }
        r = requests.post(
            f"{self.api_url}/api/data/bulk",
            headers=self.headers,
            json=body,
            timeout=60,
        )
        return r.json()
