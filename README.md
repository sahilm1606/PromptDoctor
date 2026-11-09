# PromptDoctor – AI-Powered Prompt Engineering Assistant

## 1. Project Overview

**PromptDoctor** is an AI-powered chatbot designed to help users analyze, diagnose, and improve their prompts to obtain better responses from Large Language Models (LLMs).

Writing an effective prompt is an important part of interacting with AI tools. Poorly structured or unclear prompts can produce incomplete, irrelevant, or inaccurate responses.

PromptDoctor addresses this problem by providing an interactive platform where users can submit prompts and receive AI-assisted analysis and suggestions for improvement.

The application uses a locally running AI model through Ollama, providing an accessible environment for prompt analysis and optimization.

## 2. Problem Statement

Many users struggle to write clear, specific, and effective prompts when interacting with AI systems.

Common problems include:

- Unclear or incomplete instructions.
- Missing context and relevant information.
- Ambiguous wording.
- Poorly structured prompts.
- Lack of specific output requirements.
- Difficulty obtaining consistent AI responses.

PromptDoctor aims to simplify prompt engineering by helping users identify weaknesses in their prompts and improve their structure.

## 3. Project Objectives

- Develop an AI-powered prompt analysis chatbot.
- Identify weaknesses in user-provided prompts.
- Improve prompt clarity and structure.
- Provide suggestions for more effective prompts.
- Demonstrate the practical application of Large Language Models.
- Provide an interactive and user-friendly interface.
- Explore locally hosted AI models through Ollama.

## 4. Key Features

### 4.1 AI-Powered Prompt Analysis
Users can enter their prompts and receive AI-generated analysis and recommendations.

### 4.2 Prompt Diagnosis
The application helps identify common prompt-writing problems, such as unclear instructions, missing context, and ambiguity.

### 4.3 Prompt Improvement
The system assists users in restructuring and refining their prompts to make instructions clearer and more effective.

### 4.4 Interactive Chat Interface
Users can communicate with the application through a conversational interface built using Streamlit.

### 4.5 Local AI Model Integration
PromptDoctor connects to Ollama to access a locally hosted Qwen 2.5 (3B) language model.

### 4.6 Conversation History
The project includes a conversation-history file to support storing chat-related information.

## 5. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Interactive web application interface |
| Ollama | Local AI model execution |
| Qwen 2.5 (3B) | Large Language Model |
| Requests | Communication with the Ollama API |
| JSON | Structured conversation-history storage |

## 6. System Architecture

PromptDoctor follows a simple AI application architecture.

**Application workflow:**

1. User enters a prompt through the Streamlit interface.
2. The Python application receives the user's input.
3. The application prepares the request for the language model.
4. Requests communicates with the locally running Ollama API.
5. The Qwen 2.5 (3B) model processes the prompt.
6. The model generates an analysis or improvement suggestion.
7. The application displays the generated response in the chat interface.

### Architecture Flow

```text
        USER
          |
          v
   STREAMLIT INTERFACE
          |
          v
      PYTHON APP
          |
          v
    REQUESTS LIBRARY
          |
          v
      OLLAMA API
          |
          v
    QWEN 2.5 (3B)
          |
          v
   AI-GENERATED RESPONSE
          |
          v
   STREAMLIT CHAT UI
          |
          v
         USER
```

## 7. How PromptDoctor Works

### Step 1: User Input
The user enters a prompt that they want to analyze or improve.

### Step 2: Input Processing
The Python application receives and prepares the prompt for processing.

### Step 3: AI Model Communication
The application sends the request to Ollama through its API.

### Step 4: Prompt Analysis
The Qwen 2.5 (3B) model interprets the input and generates relevant feedback.

### Step 5: Response Generation
The model provides suggestions or an improved version of the prompt.

### Step 6: Display Results
The Streamlit interface presents the AI-generated response to the user.

## 8. Project Structure

```text
PromptDoctor/
│
├── app.py
│   └── Main Streamlit application
│
├── app_backup.py
│   └── Backup copy of the application
│
├── requirements.txt
│   └── Python dependencies
│
├── .gitignore
│   └── Files excluded from Git tracking
│
└── prompt_doctor_history.json
    └── Local conversation-history data
```

## 9. Installation and Setup

### Prerequisites

Before running PromptDoctor, install:

- Python 3.
- Ollama.
- Git (optional, for cloning the repository).

### Step 1: Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd PromptDoctor
```

### Step 2: Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate the environment on macOS or Linux:

```bash
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

The application uses the following Python dependencies:

```text
streamlit
requests
```

### Step 4: Install Ollama

Download Ollama from:

https://ollama.com/download

Install and start Ollama.

### Step 5: Download the AI Model

Run:

```bash
ollama pull qwen2.5:3b
```

This downloads the Qwen 2.5 (3B) model locally.

### Step 6: Run the Application

Execute:

```bash
streamlit run app.py
```

### Step 7: Access the Application

Open the local Streamlit URL displayed in your Terminal, normally:

```text
http://localhost:8501
```

The PromptDoctor application will be available in your browser.

## 10. Applications and Use Cases

PromptDoctor can be useful for:

- Students learning prompt engineering.
- Developers working with AI applications.
- Researchers experimenting with LLMs.
- Content creators improving AI instructions.
- Users who want clearer and more structured AI outputs.
- Beginners learning how to interact effectively with AI systems.

## 11. Advantages

- Simple and interactive user interface.
- Supports locally hosted AI model execution.
- Helps users understand prompt engineering.
- Provides AI-assisted prompt improvement.
- Uses an open-source model through Ollama.
- Demonstrates integration of Python with modern AI technologies.

## 12. Limitations

- Response quality depends on the selected language model.
- Local model execution requires sufficient system resources.
- AI-generated suggestions may occasionally be inaccurate.
- The application depends on the availability of the local Ollama service.

## 13. Future Enhancements

The project can be extended with:

- Prompt quality scoring.
- Multiple prompt optimization strategies.
- Support for additional language models.
- Prompt comparison and evaluation.
- Exporting improved prompts.
- Advanced prompt templates for different domains.
- More detailed prompt diagnostics.
- Enhanced conversation management.

## 14. Project Learning Outcomes

Through this project, the development process demonstrates:

- Python application development.
- Building interactive applications using Streamlit.
- Working with Large Language Models.
- Integrating locally hosted AI models using Ollama.
- Communicating with APIs using Requests.
- Understanding prompt engineering concepts.
- Managing application data using JSON.

## 15. Conclusion

PromptDoctor demonstrates how Artificial Intelligence and Large Language Models can simplify prompt engineering.

By combining Python, Streamlit, Ollama, and Qwen 2.5 (3B), the application provides an interactive environment for analyzing and improving user prompts.

The project highlights the practical use of locally hosted AI models and demonstrates how prompt quality can be improved through AI-assisted feedback.

---

**Project Name:** PromptDoctor – AI-Powered Prompt Engineering Assistant

**Project Domain:** Artificial Intelligence, Prompt Engineering, and Natural Language Processing.

**Primary Technologies:** Python, Streamlit, Ollama, Qwen 2.5 (3B).

*PromptDoctor – Diagnose, Refine, and Improve Your Prompts with AI.*
