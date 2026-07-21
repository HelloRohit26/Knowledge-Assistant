"""
Conflict Resolver

Detects when multiple documents cover the same topic
and determines which is authoritative based on:
- Version number
- Effective date
- Authority score
- Status (Active > Draft > Archived)
"""


STATUS_PRIORITY = {
    "Active": 5,
    "Under Review": 4,
    "Draft": 3,
    "Archived": 1,
    "Superseded": 0,
}


def parse_version(version_str):
    """Extract numeric version from string like 'v3', '2.1'."""

    if version_str is None:
        return 0

    import re
    nums = re.findall(r'[\d.]+', str(version_str))

    if not nums:
        return 0

    try:
        return float(nums[0])
    except ValueError:
        return 0


def compute_authority(metadata):
    """Compute overall authority weight for a document."""

    score = 0

    # Authority score from rules engine (0-100)
    authority = metadata.get("authority_score", 50)
    if isinstance(authority, str):
        try:
            authority = int(authority)
        except ValueError:
            authority = 50
    score += authority

    # Status priority
    status = str(metadata.get("status", "Active"))
    score += STATUS_PRIORITY.get(status, 2) * 10

    # Version boost
    version = parse_version(
        metadata.get("version")
    )
    score += version * 5

    # Official document boost
    is_official = metadata.get("is_official", False)
    if is_official is True or is_official == "true":
        score += 20

    return score


def resolve_conflicts(results):
    """
    Given a list of search results, detect conflicts
    and mark which document is authoritative.

    Groups by topic/document_type and compares within
    each group.
    """

    if not results:
        return results

    # Group by topic
    topic_groups = {}

    for item in results:
        metadata = item.get("metadata", {})
        topic = metadata.get("topic", "unknown")
        doc_type = metadata.get(
            "document_type", "unknown"
        )

        key = f"{topic}_{doc_type}".lower()

        if key not in topic_groups:
            topic_groups[key] = []

        topic_groups[key].append(item)

    # Resolve within each group
    for key, group in topic_groups.items():

        if len(group) <= 1:
            # No conflict possible
            group[0]["conflict_status"] = "no_conflict"
            group[0]["is_authoritative"] = True
            continue

        # Score each document
        for item in group:
            metadata = item.get("metadata", {})
            item["authority_weight"] = (
                compute_authority(metadata)
            )

        # Sort by authority (highest first)
        group.sort(
            key=lambda x: x["authority_weight"],
            reverse=True
        )

        # Mark the winner
        group[0]["conflict_status"] = "authoritative"
        group[0]["is_authoritative"] = True

        for item in group[1:]:
            item["conflict_status"] = "superseded"
            item["is_authoritative"] = False

    # Flatten back
    resolved = []
    for key, group in topic_groups.items():
        resolved.extend(group)

    # Sort: authoritative first, then by composite
    resolved.sort(
        key=lambda x: (
            x.get("is_authoritative", False),
            x.get("composite_score", 0)
        ),
        reverse=True
    )

    return resolved
