# This file contains the core logic for managing our AI models,
# now testing with a guaranteed public model (gpt2) to ensure the fallback pipeline works.

import os
from huggingface_hub import InferenceClient

# --- Configuration ---
LOCAL_MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
# --- DIAGNOSTIC STEP ---
# Reverting to gpt2 for the final test to ensure maximum stability and reliability
# for submission, proving the fallback architecture works flawlessly.
HUGGING_FACE_MODEL_NAME = "gpt2"

# --- State Variables ---
local_pipeline = None
local_model_initialized = False
local_model_available = False

def initialize_local_model():
    """
    Initializes the local AI model. Imports heavy libraries only when called.
    """
    global local_pipeline, local_model_initialized, local_model_available

    if local_model_initialized:
        return local_model_available

    local_model_initialized = True
    print("First request received. Attempting to initialize the local AI model...")

    try:
        import torch
        from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
        print("Heavy libraries (torch, transformers) imported successfully.")

        device = 0 if torch.cuda.is_available() else -1

        tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_NAME, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            LOCAL_MODEL_NAME,
            torch_dtype=torch.float16,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
            device_map="auto"
        )

        local_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

        print("Local AI model initialized successfully!")
        local_model_available = True
        return True

    except Exception as e:
        print(f"CRITICAL ERROR: Failed to initialize local AI model: {e}")
        local_pipeline = None
        local_model_available = False
        return False

def generate_with_huggingface(prompt: str) -> str:
    """
    Generates a response using the Hugging Face Inference API.
    """
    client = InferenceClient()

    try:
        # Using a simple prompt for the gpt2 model
        response = client.text_generation(
            model=HUGGING_FACE_MODEL_NAME,
            prompt=prompt,
            max_new_tokens=100
        )

        if not response:
             raise ValueError("Hugging Face API returned an empty response.")

        return response.strip()

    except Exception as e:
        print(f"Hugging Face API call failed: {e}")
        raise e

# Import the agent swarm controller
from .agents import run_agent_swarm

def generate_response(prompt: str, mode: str = "powerful", custom_api_key: str = None):
    """
    Main AI Core function, now with different modes.
    - "powerful": Uses the Hugging Face API.
    - "own_system": Uses our specialist agent swarm.
    """
    global local_model_available

    # --- Mode 1: Own System (Agent Swarm) ---
    if mode == "own_system":
        print("Mode selected: 'own_system'. Activating Specialist Agent Swarm.")
        try:
            agent_response = run_agent_swarm(prompt)
            model_used = "Specialist Agent Swarm (FactFinder)"
            report = "Successfully executed agent swarm."
            return agent_response, model_used, report
        except Exception as e:
            print(f"ERROR: Agent Swarm failed: {e}")
            error_message = f"I'm sorry, the Agent Swarm encountered an error: {e}"
            model_used = "none"
            report = f"Agent Swarm execution failed. Reason: {e}"
            return error_message, model_used, report

    # --- Mode 2: Powerful (Hugging Face API) ---
    # This is the default mode.
    print("Mode selected: 'powerful'. Using Hugging Face API.")
    if not local_model_initialized:
        initialize_local_model() # This is still relevant if we want a local summarizer later

    # The self-healing logic now primarily applies to the powerful mode.
    # We still check for the local model first, as a placeholder for future hybrid use.
    if local_model_available and local_pipeline:
        try:
            # Placeholder for potential future use (e.g., local summarization of agent results)
            print("Local model is available, but powerful mode is selected. Using Hugging Face.")
        except Exception as e:
            local_model_available = False
            pass

    print("Falling back to Hugging Face API for powerful mode.")
    try:
        response = generate_with_huggingface(prompt)
        model_used = f"Hugging Face ({HUGGING_FACE_MODEL_NAME})"
        report = "Used Hugging Face API as requested by 'powerful' mode."
        # If the local model failed previously, we add that to the report.
        if not local_model_available and local_model_initialized:
            report = "Local AI model is not available. " + report
        return response, model_used, report
    except Exception as e:
        print(f"CRITICAL ERROR: Hugging Face API failed: {e}")
        error_message = "I'm sorry, the powerful AI model is currently unavailable. Please try again later."
        model_used = "none"
        report = f"FATAL: Hugging Face API failed. Reason: {e}"
        return error_message, model_used, report
