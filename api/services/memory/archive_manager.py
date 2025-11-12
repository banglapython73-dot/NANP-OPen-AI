# This file will manage the "Eternal Archive", our system's long-term memory.
import json
import os
import hashlib
from datetime import datetime

# --- Configuration ---
ARCHIVE_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'archive_index.json') # Store it in the root `api` folder

# --- Core Archive Functions ---

def load_archive():
    """
    Loads the entire archive from the JSON file.
    Includes verification using "The Verifier".
    """
    if not os.path.exists(ARCHIVE_FILE_PATH):
        return {"entries": {}, "metadata": {}} # Return a clean slate if no archive exists

    with open(ARCHIVE_FILE_PATH, 'r') as f:
        archive_data = json.load(f)

    # "The Verifier": Check data integrity
    if not verify_archive_integrity(archive_data):
        print("WARNING: Archive integrity check failed! The file may be corrupted.")
        # We could either return empty or try to use the partial data.
        # For safety, we'll return an empty state.
        return {"entries": {}, "metadata": {}}

    print("Archive loaded and verified successfully.")
    return archive_data.get("entries", {})

def save_archive(entries, metadata):
    """
    Saves the archive data to the JSON file.
    Includes integrity hash generation for "The Verifier".
    """
    archive_data = {
        "entries": entries,
        "metadata": metadata
    }

    # "The Verifier": Generate hash before saving
    archive_data["metadata"]["hash"] = generate_data_hash(entries)

    with open(ARCHIVE_FILE_PATH, 'w') as f:
        json.dump(archive_data, f, indent=4)
    print("Archive saved successfully.")


def add_to_archive(prompt, response_data, source, keywords=None):
    """
    Adds a new entry to the archive.
    This function embodies "The Librarian" by structuring the data.
    Includes placeholder for AI-generated keywords ("The Curation Engine").
    """
    if keywords is None:
        keywords = [] # Default to an empty list

    archive_entries = load_archive()

    # "The Librarian": Structure the data
    entry_id = hashlib.sha256(prompt.encode()).hexdigest() # Use a hash of the prompt as a unique ID

    archive_entries[entry_id] = {
        "prompt": prompt,
        "response": response_data,
        "source": source,
        "keywords": keywords, # "The Curation Engine" input
        "timestamp": datetime.utcnow().isoformat(),
        "access_count": 1
    }

    # Update metadata and save
    metadata = {"last_updated": datetime.utcnow().isoformat()}
    save_archive(archive_entries, metadata)
    print(f"New entry for prompt '{prompt[:30]}...' added to archive.")

def find_in_archive(prompt):
    """
    Searches for a prompt in the archive.
    """
    archive_entries = load_archive()
    entry_id = hashlib.sha256(prompt.encode()).hexdigest()

    entry = archive_entries.get(entry_id)
    if entry:
        print(f"Found match for '{prompt[:30]}...' in archive.")
        # Update access count for usage statistics
        entry["access_count"] += 1
        save_archive(archive_entries, {"last_updated": datetime.utcnow().isoformat()})
        return entry

    return None

# --- Integrity Verification ("The Verifier") ---

def generate_data_hash(data):
    """
    Generates a SHA256 hash of the archive's entry data.
    """
    # Use a consistent dump format to ensure the hash is always the same for the same data
    serialized_data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(serialized_data.encode()).hexdigest()

def verify_archive_integrity(archive_data):
    """
    Verifies that the archive's data matches its stored hash.
    """
    if "metadata" not in archive_data or "hash" not in archive_data["metadata"]:
        print("Archive has no metadata or hash. Verification skipped for older/new archives.")
        return True # Can't verify, so we assume it's okay for now.

    stored_hash = archive_data["metadata"]["hash"]
    current_hash = generate_data_hash(archive_data.get("entries", {}))

    return stored_hash == current_hash
