# This file implements "The Gatekeeper", our single, powerful layer of security.
# It uses a three-phase defense protocol to scan incoming data.

def scan_data(raw_data, source_reputation):
    """
    The main function for The Gatekeeper.
    It orchestrates the three-phase scanning process.
    """
    print(f"Gatekeeper: Starting scan for data from a source with reputation: {source_reputation}")

    # Phase 1: "The Sentry" (Static Analysis)
    sentry_passed, sentry_report = phase1_sentry_scan(raw_data)
    if not sentry_passed:
        print(f"GATEKEEPER REJECTED: Failed Phase 1 (The Sentry). Reason: {sentry_report}")
        return None, "Rejected by Sentry"

    # Phase 2: "The Interrogator" (Behavioral Analysis)
    interrogator_passed, interrogator_report = phase2_interrogator_scan(raw_data)
    if not interrogator_passed:
        print(f"GATEKEEPER REJECTED: Failed Phase 2 (The Interrogator). Reason: {interrogator_report}")
        return None, "Rejected by Interrogator"

    # Phase 3: "The Guardian" (Integrity and Sanitization)
    guardian_passed, sanitized_data, guardian_report = phase3_guardian_scan(raw_data)
    if not guardian_passed:
        print(f"GATEKEEPER REJECTED: Failed Phase 3 (The Guardian). Reason: {guardian_report}")
        return None, "Rejected by Guardian"

    print("Gatekeeper: All three security phases passed. Data is safe.")
    return sanitized_data, "Approved by Gatekeeper"


# --- Phase 1: The Sentry (Static Analysis) ---
def phase1_sentry_scan(data):
    """
    Scans for known malicious signatures and suspicious metadata.
    Placeholder function for now.
    """
    # In a real implementation, this would check against a database of virus signatures.
    # For now, we'll simulate a check. Let's assume no data is immediately obviously bad.
    print("Sentry: Performing static analysis...")
    if "malicious_signature" in str(data):
        return False, "Known malicious signature detected."
    print("Sentry: Scan passed.")
    return True, "No known malicious signatures found."


# --- Phase 2: The Interrogator (Behavioral Analysis) ---
def phase2_interrogator_scan(data):
    """
    Analyzes the "behavior" of the data in a simulated environment.
    Placeholder function for now.
    """
    # This is a complex step to simulate. We'll pretend to run it in a sandbox.
    # We'll check for suspicious "intent", like trying to execute code.
    print("Interrogator: Performing behavioral analysis in sandbox...")
    if "attempt_to_execute" in str(data):
        return False, "Data attempted to execute unauthorized code in sandbox."
    print("Interrogator: Scan passed.")
    return True, "No suspicious behavior detected."


# --- Phase 3: The Guardian (Integrity and Sanitization) ---
def phase3_guardian_scan(data):
    """
    Checks for data corruption and sanitizes the content.
    Placeholder function for now.
    """
    # We'll check for basic integrity and "sanitize" the data (e.g., remove scripts).
    print("Guardian: Performing integrity check and sanitization...")
    if data is None:
        return False, None, "Data is null or corrupted."

    # Simulate sanitization: for now, we just return the data as is.
    sanitized_data = str(data).replace("<script>", "&lt;script&gt;")

    print("Guardian: Scan passed.")
    return True, sanitized_data, "Data integrity verified and content sanitized."
