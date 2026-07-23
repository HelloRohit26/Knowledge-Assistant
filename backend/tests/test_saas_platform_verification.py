"""
Verification script for SaaS Multi-Tenant Platform & Multi-Agent Capabilities
"""

from app.database.init_db import initialize_database
from app.services.memory_service import save_user_preference, get_user_preferences
from app.services.multi_agent_system import run_multi_agent_collaboration
from app.services.knowledge_graph import generate_knowledge_graph
from app.services.rule_engine import list_automation_rules
from app.services.saas_service import get_or_create_organization, create_developer_api_key

def test_saas_platform():
    initialize_database()

    # Test Phase 1: Memory
    save_user_preference("test_user", "default_department", "Engineering")
    prefs = get_user_preferences("test_user")
    print(f"User Preferences: {prefs}")
    assert prefs.get("default_department") == "Engineering"

    # Test Phase 2: Multi-Agent Collaboration
    multi_res = run_multi_agent_collaboration("Synthesize onboarding and leave rules across HR and Legal")
    print(f"Multi-Agent Task Result: {multi_res.get('task')}")
    assert len(multi_res.get("agents_participated", [])) > 0

    # Test Phase 4: Knowledge Graph
    graph_res = generate_knowledge_graph()
    print(f"Knowledge Graph Nodes: {graph_res['nodes_count']}, Edges: {graph_res['edges_count']}")
    assert graph_res['nodes_count'] > 0

    # Test Phase 9: Rule Engine
    rules = list_automation_rules()
    print(f"Automation Rules Count: {len(rules)}")
    assert len(rules) > 0

    # Test Phase 10: SaaS & API Keys
    org = get_or_create_organization("Acme Corp")
    print(f"Org Tenant ID: {org['org_id']}, Tier: {org['tier']}")
    assert org["tier"] == "enterprise"

    key = create_developer_api_key("Production Key", org["org_id"])
    print(f"Generated Developer API Key: {key['api_key'][:12]}...")
    assert key["api_key"].startswith("ki_live_")

if __name__ == "__main__":
    test_saas_platform()
