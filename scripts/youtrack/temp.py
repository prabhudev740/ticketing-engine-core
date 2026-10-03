import requests
import json
import datetime

# --- CONFIGURATION ---
YOUTRACK_BASE_URL = "https://prabhudev.youtrack.cloud/api"
YOUTRACK_TOKEN = "perm-YWRtaW4=.NjMtMA==.vaANK9zFuAjM6f3Z1Ph7zz909nT0ka"
INTERNAL_PROJECT_ID = "0-10"  # Replace with your actual internal ID (e.g., 81-1)

HEADERS = {
    "Authorization": f"Bearer {YOUTRACK_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Base Date: Sunday, October 4, 2026 (Noon UTC to prevent timezone shifts)
# BASE_DATE = datetime.datetime(2026, 10, 4, 12, 0, 0, tzinfo=datetime.timezone.utc)

def get_timestamp(day_offset):
    """Calculates the exact Unix timestamp in milliseconds for the target date."""
    target_date = BASE_DATE + datetime.timedelta(days=day_offset)
    return int(target_date.timestamp() * 1000)

# --- 14-DAY TASK STRUCTURE ---
task_groups = [
    {
        "parent": {
            "summary": "Infrastructure & System State",
            "description": "Establish core monorepo architecture and external database connections.",
            "start_offset": 0, "end_offset": 3
        },
        "children": [
            {
                "summary": "Initialize Monorepo Architecture",
                "description": "Execute init_project.sh to generate the monorepo directory and file structure.",
                "start_offset": 0, "end_offset": 0
            },
            {
                "summary": "Provision PostgreSQL & Redis",
                "description": "Deploy managed PostgreSQL and Serverless Redis. Store connection strings in .env.",
                "start_offset": 1, "end_offset": 1
            },
            {
                "summary": "Implement Async Data Clients",
                "description": "Implement database.py utilizing an async SQLAlchemy connection pool and cache.py.",
                "start_offset": 2, "end_offset": 3
            },
            {
                "summary": "Build System Health API",
                "description": "Implement GET /api/v1/health returning JSON connection statuses.",
                "start_offset": 3, "end_offset": 3
            }
        ]
    }
]

# --- EXECUTION FUNCTIONS ---
def create_issue(summary, description, start_offset, end_offset):
    start_ms = get_timestamp(start_offset)
    end_ms = get_timestamp(end_offset)
    
    payload = {
        "project": {"id": INTERNAL_PROJECT_ID},
        "summary": summary,
        "description": description,
        "customFields": [
            {
                "name": "Type",
                "$type": "SingleEnumIssueCustomField",
                "value": {"name": "Task"}
            },
            {
                "name": "Start Date",
                "$type": "SimpleIssueCustomField",
                "value": start_ms
            },
            {
                "name": "Due Date",
                "$type": "SimpleIssueCustomField",
                "value": end_ms
            }
        ]
    }
    
    response = requests.post(
        f"{YOUTRACK_BASE_URL}/issues?fields=idReadable", 
        headers=HEADERS, 
        data=json.dumps(payload)
    )
    
    if response.status_code == 200:
        return response.json().get("idReadable")
    else:
        print(f"Error creating issue '{summary}': {response.status_code} {response.text}")
        return None

def link_as_subtask(child_id, parent_id):
    payload = {
        "query": f"subtask of {parent_id}",
        "issues": [{"idReadable": child_id}]
    }
    response = requests.post(
        f"{YOUTRACK_BASE_URL}/commands",
        headers=HEADERS,
        data=json.dumps(payload)
    )
    if response.status_code != 200:
        print(f"Error linking {child_id} to {parent_id}: {response.status_code} {response.text}")

def main():
    print(f"Connecting to YouTrack: {YOUTRACK_BASE_URL}...")
    
    for group in task_groups:
        parent = group["parent"]
        print(f"\nCreating Parent Task: {parent['summary']}...")
        parent_id = create_issue(parent["summary"], parent["description"], parent["start_offset"], parent["end_offset"])
        
        if not parent_id:
            print("Failed to create parent Task. Skipping its subtasks.")
            continue
            
        print(f"Success! Parent Task ID: {parent_id}")
        
        for child in group["children"]:
            print(f"  -> Creating Child Task: {child['summary']}...")
            child_id = create_issue(child["summary"], child["description"], child["start_offset"], child["end_offset"])
            
            if child_id:
                link_as_subtask(child_id, parent_id)
                print(f"     Linked {child_id} to {parent_id}")

if __name__ == "__main__":
    main()