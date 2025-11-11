# Project Athena: An Advanced, Self-Healing, AI-Powered Research Assistant

Welcome to Project Athena, a next-generation AI research assistant designed to be powerful, resilient, secure, and incredibly user-friendly. This project combines multiple AI agents, a self-healing architecture, and a rich, intuitive Android interface to deliver a seamless research experience.

## Core Features

- **Dual AI Core & Self-Healing System**: Automatically switches between a powerful cloud model and a local agent swarm, ensuring the system is always available.
- **The Eternal Archive**: A long-term memory system that caches results for lightning-fast responses (1-3 seconds). It features:
    - **The Librarian**: Automatically categorizes and indexes data.
    - **The Verifier**: Ensures data integrity with digital fingerprints.
    - **User-Controlled Sync**: Sync your archive to your Google Drive without any APIs.
- **The Gatekeeper Security Protocol**: A three-phase defense system (`Sentry`, `Interrogator`, `Guardian`) that scans all incoming data for threats.
- **Resilient Swarm Intelligence**: A parallel data scraping system that automatically detects, debugs, and recovers from failures, ensuring maximum reliability.
- **Advanced Research Suite**:
    - **Hypothesis Expansion Core**: Breaks down simple questions into deep, analytical sub-questions.
    - **Cross-Verification Fact-Checker**: Compares data from multiple sources to ensure accuracy.
    - **Academic Integrity Suite**: (Future) Plagiarism detection and paraphrasing.
- **"Zero-Code" Data Visualization Engine**: Automatically generates graphs and charts from natural language commands (e.g., "show me a bar chart of...") using R and ggplot2.
- **AI-Powered Image Curation**: Enriches text responses with relevant, high-quality images from free sources like Pexels.
- **Fully Bilingual**: Supports both English and Bengali seamlessly.
- **Adaptive Connectivity**: Automatically configures network settings to work in both a hosted environment and a local machine.

## Architecture Overview

- **Backend**: A modular Flask application written in Python. It serves a robust API for the Android app.
- **Frontend**: A native Android application built with Kotlin and Jetpack Compose for a modern and reactive UI.
- **CI/CD**: A GitHub Actions workflow automatically builds a downloadable APK on every push to the `main` branch.

## Getting Started

### Backend Setup

1.  Navigate to the `api/` directory.
2.  Create a virtual environment: `python3 -m venv venv` and `source venv/bin/activate`.
3.  Install the required dependencies: `pip install -r requirements.txt`.
4.  (Optional) For the image curation feature, create a `.env` file (use `.env.example` as a template) and add your Pexels API key.
5.  Run the server: `python3 app.py`.

### Android App Setup

1.  Open the `android-app/` directory in Android Studio.
2.  Let Gradle sync the dependencies.
3.  Run the app on an emulator or a physical device. The app will automatically connect to the backend running on your local machine.

## Future Enhancements

-   Implement the "Academic Integrity Suite".
-   Enable the "Dynamic Integration Hub" for user-controlled data sources.
-   Fully implement the R-based data visualization engine with `rpy2`.

---
*This project was developed by Jules, your AI Software Engineer.*
