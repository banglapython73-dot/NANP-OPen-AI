# This file will act as the central nervous system of our AI,
# orchestrating calls to various modules like security, data sources, and memory.

# Import the new archive manager
from .memory.archive_manager import find_in_archive, add_to_archive

# Import the security gatekeeper
from .security.gatekeeper import scan_data
# Import the data dispatcher
from .data_sources.dispatcher import fetch_data

# Import the image curator
from .enhancements.image_curator import get_relevant_image
# Import the visualization engine
from .enhancements.visualization_engine import create_visualization
# Import the research suite agents
from .agents.research_suite import fact_check_data

async def process_request(prompt: str, mode: str, user_preferences: dict):
    """
    The new central function to handle a user's request.
    It orchestrates the workflow with a focus on speed ("Archive First").
    """
    # 1. "Archive First" Policy for maximum speed.
    # Check the internal archive first based on the prompt.
    archive_result = find_in_archive(prompt)
    if archive_result:
        # Return the found data immediately for a 1-3 second response time.
        return archive_result['response'], "Eternal Archive (Local)", "Fast retrieval from archive."

    # If not in archive, proceed with the rest of the workflow.
    # 2. (Future) Log the request and apply initial security checks.

    # 3. Fetch data from external sources via the dispatcher.
    raw_data, source_reputation = await fetch_data(prompt, user_preferences)

    # 4. Scan the fetched data using The Gatekeeper.
    safe_data, gatekeeper_report = scan_data(raw_data, source_reputation)
    if not safe_data:
        # If data is blocked, inform the user and do NOT archive it.
        return "I could not find safe and reliable information for your query.", "Security Block", gatekeeper_report

    # 5. Fact-check the consolidated data.
    verified_data = fact_check_data(safe_data)

    # 6. Synthesize the final response using the appropriate AI model.
    #    For now, we'll just use the verified data as our response.
    final_text_response = verified_data

    # 6. Visualization Check & Image Enhancement
    # First, check if the user is asking for a graph.
    visualization_path = create_visualization(prompt)

    image_url = None
    if visualization_path:
        # If a graph was created, use its path.
        # Note: In a real server, this local path would need to be converted to a public URL.
        image_url = visualization_path
    else:
        # Otherwise, find a relevant stock image.
        image_url = get_relevant_image(final_text_response, keywords=[]) # Pass keywords in the future

    # 7. Update the archive with the new findings.
    # The archive will now store the full response object.
    response_payload = {
        "text": final_text_response,
        "image_url": image_url
    }
    add_to_archive(prompt, response_payload, source="Live Generation", keywords=[])

    # Prepare the final response object
    model_used = f"Central Controller (Mode: {mode})"
    diagnostic = "Successfully routed through the new main_controller."

    return response_payload, model_used, diagnostic
