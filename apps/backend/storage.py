"""
Simple file-based storage for demo purposes
In production, this would be replaced with a proper database
"""
import json
import pathlib
from typing import Dict, List, Any
from datetime import datetime

STORAGE_DIR = pathlib.Path("data/storage")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def load_data(filename: str) -> Dict[str, Any]:
    """Load data from JSON file"""
    file_path = STORAGE_DIR / f"{filename}.json"
    if file_path.exists():
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_data(filename: str, data: Dict[str, Any]) -> None:
    """Save data to JSON file"""
    file_path = STORAGE_DIR / f"{filename}.json"
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    except IOError as e:
        print(f"Error saving data to {file_path}: {e}")

def load_jobs() -> Dict[str, Any]:
    """Load jobs data"""
    return load_data("jobs")

def save_jobs(jobs: Dict[str, Any]) -> None:
    """Save jobs data"""
    save_data("jobs", jobs)

def load_sites() -> Dict[str, Any]:
    """Load sites data"""
    return load_data("sites")

def save_sites(sites: Dict[str, Any]) -> None:
    """Save sites data"""
    save_data("sites", sites)

def load_activity() -> List[Dict[str, Any]]:
    """Load activity data"""
    data = load_data("activity")
    return data.get("items", [])

def save_activity(activity: List[Dict[str, Any]]) -> None:
    """Save activity data"""
    save_data("activity", {"items": activity})
