"""
Memory Service — AI Session Memory, Preferences & Workflow State Persistence
"""

import json
from typing import List, Dict, Any, Optional
from app.database.db import get_connection
from app.core.logger import logger


def save_memory_item(user_id: str, session_id: str, memory_type: str, key: str, value: Any):
    """
    Saves or updates a memory item in SQLite.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO agent_memory (user_id, session_id, memory_type, key, value_json)
        VALUES (?, ?, ?, ?, ?)
        """, (user_id, session_id, memory_type, key, json.dumps(value)))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error saving agent memory: {e}")


def get_memory_items(user_id: str, session_id: Optional[str] = None, memory_type: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Retrieves stored memory items.
    """
    items = []
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT id, user_id, session_id, memory_type, key, value_json, updated_at FROM agent_memory WHERE user_id = ?"
        params = [user_id]

        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        if memory_type:
            query += " AND memory_type = ?"
            params.append(memory_type)

        query += " ORDER BY updated_at DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            m_id, u_id, s_id, m_type, key, val_json, updated_at = row
            try:
                val = json.loads(val_json)
            except Exception:
                val = val_json

            items.append({
                "id": m_id,
                "user_id": u_id,
                "session_id": s_id,
                "memory_type": m_type,
                "key": key,
                "value": val,
                "updated_at": str(updated_at)
            })
    except Exception as e:
        logger.error(f"Error retrieving agent memory: {e}")

    return items


def save_user_preference(user_id: str, pref_key: str, pref_val: Any):
    """
    Save user specific preference settings (e.g. default department, search mode, export format).
    """
    save_memory_item(user_id=user_id, session_id="global_pref", memory_type="user_pref", key=pref_key, value=pref_val)


def get_user_preferences(user_id: str) -> Dict[str, Any]:
    """
    Fetch all user preferences.
    """
    items = get_memory_items(user_id=user_id, session_id="global_pref", memory_type="user_pref", limit=50)
    return {item["key"]: item["value"] for item in items}
