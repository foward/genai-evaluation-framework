# GenAI Evaluation Framework

This project is a FastAPI application designed to evaluate GenAI models by running batch tests based on a provided configuration file. The application supports CORS and allows uploading a configuration file to run tests and return the results.

## Project Structure
- [`main.py`]: The main entry point for the FastAPI application.
- `utils.py`: Contains utility functions for fetching data and running batch tests.
- [`requirements.txt`]: Lists the dependencies required for the project.

## Setup

### Prerequisites

- Python 3.7+
- `pip` (Python package installer)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/foward/genai_evaluation.git
cd genai_evaluation

pip install -r requirements.txt
```

2. Running the Application

To run the FastAPI application, use the following command:
```bash
uvicorn main:app --reload
```

This will start the FastAPI server, and you can access the endpoint /upload-config-and-run-tests to upload your configuration file and run the tests.

## API Endpoints
Upload Configuration and Run Tests
URL: /upload-config-and-run-tests
Method: POST
Description: Upload a configuration file and run batch tests based on the provided configuration.
### Request
- Content-Type: multipart/form-data
- File: A JSON file containing the configuration.

This configuration file, example_batch_tests_answer.json, is used to run batch tests by sending queries to a specified Large Language Model (LLM) endpoint. The file contains various parameters to configure the LLM and a set of questions with their expected answers.

## File Structure
The JSON file is structured as follows:

- api_endpoint: The URL of the LLM endpoint to which the queries will be sent.
- parameters: A set of parameters to configure the behavior of the LLM.
  - number_results: The number of results to return.
  - threshold: The threshold value for filtering results.
  - llm_model_name: The name of the LLM model to use.
  - llm_max_output_tokens: The maximum number of tokens the LLM can output.
  - llm_temperature: The temperature setting for the LLM, which controls the randomness of the output.
  - llm_top_p: The top-p sampling parameter.
  - llm_top_k: The top-k sampling parameter.
  - llm_verbose: A boolean indicating whether to enable verbose logging.
  - lgc_search_type: The type of search to perform (e.g., similarity).
  - retrieval_chain_type: The type of retrieval chain to use (e.g., stuff).
  - questions: A list of questions to send to the LLM, each with an expected answer.
  - query: The question to ask the LLM.
  - expected_answer: The expected answer for the question.

Example
Here is an example of the JSON configuration:

```json
{
    "api_endpoint": "http://127.0.0.1:8000/YOUR_LLM_ENDPOINT",
    "parameters": {
      "number_results": 10,
      "threshold": 0.6,
      "llm_model_name": "text-bison",
      "llm_max_output_tokens": 2048,
      "llm_temperature": 0.2,
      "llm_top_p": 0.95,
      "llm_top_k": 40,
      "llm_verbose": true,
      "lgc_search_type": "similarity",
      "retrieval_chain_type": "stuff"
    },
    "questions": [
      {
        "query": "What is a threshold for procurement?",
        "expected_answer": "€1,000 per contractor"
      },
      {
        "query": "What is a Baseline Itinerary?",
        "expected_answer": "A baseline itinerary is defined as the most direct and economical"
      }
    ]
}
```

## Usage
1. Update the api_endpoint with the URL of your LLM endpoint.
2. Modify the parameters as needed to configure the LLM.
3. Add or update the questions with the queries you want to test and their expected answers.
4. Use this configuration file in your batch testing script to send the queries to the LLM endpoint and validate the responses against the expected answers.


## Response
- Content-Type: application/json
- Body: A JSON object containing the results of the batch tests.

Example response:

```json
{
  "message": "Batch tests completed",
  "config": "{\"number_results\": 20, \"threshold\": 0.7, ...}",
  "results": [
    {
      "query": "What is a threshold for decentralized procurement?",
      "timestamp": "2023-10-01T12:34:56.789Z",
      "actual_answer": "€5,000 per contractor",
      "expected_answer": "€5,000 per contractor",
      "passed": "True"
    }
  ]
}
```

### Utility Functions
#### Fetch Function
The fetch function sends a GET request to the specified URL with the provided parameters and returns the JSON response.

#### Run Batch Tests
The run_batch_tests function runs batch tests based on the provided configuration and returns the results.

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgments
