"""
SaaS Service — Multi-Tenant Organizations, API Keys & Webhooks
"""

import uuid
import secrets
from typing import List, Dict, Any, Optional
from app.database.db import get_connection
from app.core.logger import logger


def get_or_create_organization(org_name: str = "Acme Enterprise Org") -> Dict[str, Any]:
    """
    Retrieves or initializes default organization tenant.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, tier, max_documents FROM organizations LIMIT 1")
        row = cursor.fetchone()

        if row:
            conn.close()
            return {"org_id": row[0], "name": row[1], "tier": row[2], "max_documents": row[3]}

        org_id = f"org-{uuid.uuid4().hex[:8]}"
        cursor.execute("INSERT INTO organizations (id, name, tier, max_documents) VALUES (?, ?, 'enterprise', 5000)", (org_id, org_name))
        conn.commit()
        conn.close()
        return {"org_id": org_id, "name": org_name, "tier": "enterprise", "max_documents": 5000}
    except Exception as e:
        logger.error(f"Error managing organization: {e}")
        return {"org_id": "default_org", "name": org_name, "tier": "enterprise", "max_documents": 1000}


def create_developer_api_key(name: str = "Production API Key", org_id: str = "default_org") -> Dict[str, Any]:
    """
    Generates a secure API key for external developer REST integration.
    """
    raw_key = f"ki_live_{secrets.token_urlsafe(24)}"
    key_id = f"key-{uuid.uuid4().hex[:8]}"

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO api_keys (key_id, api_key, name, org_id, role, is_active)
        VALUES (?, ?, ?, ?, 'admin', 1)
        """, (key_id, raw_key, name, org_id))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error creating API key: {e}")

    return {
        "key_id": key_id,
        "api_key": raw_key,
        "name": name,
        "org_id": org_id,
        "role": "admin"
    }


def list_api_keys(org_id: str = "default_org") -> List[Dict[str, Any]]:
    """
    Lists developer API keys.
    """
    keys = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT key_id, api_key, name, role, is_active, created_at FROM api_keys ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            masked = f"{row[1][:8]}...{row[1][-4:]}" if len(row[1]) > 12 else "****"
            keys.append({
                "key_id": row[0],
                "masked_key": masked,
                "name": row[2],
                "role": row[3],
                "is_active": bool(row[4]),
                "created_at": str(row[5])
            })
    except Exception as e:
        logger.error(f"Error listing API keys: {e}")

    return keys
