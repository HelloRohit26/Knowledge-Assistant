"""
API Router for Next-Level Enterprise Platform Capabilities (Memory, Multi-Agent, Graph, SaaS)
"""

from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.services.memory_service import get_memory_items, save_user_preference, get_user_preferences
from app.services.multi_agent_system import run_multi_agent_collaboration
from app.services.knowledge_graph import generate_knowledge_graph
from app.services.rule_engine import list_automation_rules, dispatch_event_trigger
from app.services.saas_service import get_or_create_organization, create_developer_api_key, list_api_keys
from app.core.logger import logger

router = APIRouter(prefix="/api/platform", tags=["platform"])


class MultiAgentTaskRequest(BaseModel):
    task: str
    agents: Optional[List[str]] = None


class UserPrefRequest(BaseModel):
    key: str
    value: Any


class APIKeyRequest(BaseModel):
    name: str = "Developer Integration Key"


# ── Phase 1: Memory APIs ──
@router.get("/memory")
def get_memory(user_id: str = "default_user", memory_type: Optional[str] = None):
    return {"memory": get_memory_items(user_id=user_id, memory_type=memory_type)}


@router.post("/preferences")
def update_preference(req: UserPrefRequest, user_id: str = "default_user"):
    save_user_preference(user_id=user_id, pref_key=req.key, pref_val=req.value)
    return {"status": "success", "preferences": get_user_preferences(user_id)}


@router.get("/preferences")
def get_preferences(user_id: str = "default_user"):
    return {"preferences": get_user_preferences(user_id)}


# ── Phase 2: Multi-Agent Collaboration API ──
@router.post("/multi-agent/collaborate")
def execute_multi_agent_task(req: MultiAgentTaskRequest):
    try:
        return run_multi_agent_collaboration(task_description=req.task, target_agents=req.agents)
    except Exception as e:
        logger.error(f"Multi-agent execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ── Phase 4: Knowledge Graph API ──
@router.get("/knowledge-graph")
def get_graph():
    return generate_knowledge_graph()


# ── Phase 9: Automation Rules API ──
@router.get("/automation/rules")
def get_rules():
    return {"rules": list_automation_rules()}


# ── Phase 10: SaaS & API Keys APIs ──
@router.get("/organization")
def get_organization():
    return get_or_create_organization()


@router.get("/api-keys")
def get_api_keys():
    return {"keys": list_api_keys()}


@router.post("/api-keys")
def create_api_key(req: APIKeyRequest):
    return create_developer_api_key(name=req.name)
