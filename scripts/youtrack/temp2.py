import requests

YOUTRACK_BASE_URL = "https://prabhudev.youtrack.cloud/api"
YOUTRACK_TOKEN = "perm-YWRtaW4=.NjMtMA==.vaANK9zFuAjM6f3Z1Ph7zz909nT0ka"

HEADERS = {
    "Authorization": f"Bearer {YOUTRACK_TOKEN}",
    "Accept": "application/json"
}

def find_project_id():
    print("Fetching projects from YouTrack...\n")
    response = requests.get(
        f"{YOUTRACK_BASE_URL}/admin/projects?fields=id,shortName,name", 
        headers=HEADERS
    )

    if response.status_code == 200:
        projects = response.json()
        for p in projects:
            print(f"Project Name: {p.get('name')}")
            print(f"Short Name  : {p.get('shortName')}")
            print(f"INTERNAL ID : {p.get('id')}")
            print("-" * 30)
    else:
        print(f"Failed to fetch projects: HTTP {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    find_project_id()