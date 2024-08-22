import aiohttp
import json
import re
from datetime import datetime
import pytz
import asyncio
from urllib.parse import quote

async def fetch(session, url, params):
    try:
        string_params = {key: str(value) for key, value in params.items()}
        async with session.get(url, params=string_params) as response:
            content_type = response.headers.get('content-type', '').lower()
            
            if response.status == 200:
                return await response.json()
            else:
                print(f"Received non-200 response: {response.status}")
                return None

    except Exception as e:
        print(f"Error during request: {str(e)}")
    return None

async def run_batch_tests(config):
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for item in config['questions']:
            query = item['query']
            encoded_query = quote(query)
            params = {**config['parameters'], 'query': encoded_query}
            task = asyncio.ensure_future(fetch(session, config['api_endpoint'], params))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        for response, item in zip(responses, config['questions']):
            if response is not None:
                try:
                    actual_answer = response.get('response')
                    expected_answer = item['expected_answer']
                    source_documents = response.get('source_documents', [])
                    passed = bool(re.search(expected_answer, actual_answer))
                    
                    passed = calculat_similarity_using_llm(actual_answer, expected_answer)

                    cet = pytz.timezone('CET')
                    timestamp = datetime.now(cet).isoformat()
                    
                    result = {
                        'query': item['query'],
                        'timestamp': timestamp,
                        'actual_answer': actual_answer,
                        'expected_answer': expected_answer,
                        'source_documents': source_documents,
                        'passed': str(passed),
                    }
                    results.append(result)
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {str(e)}")
                except Exception as e:
                    print("ERROR in Query: ", item['query'])
                    print(f"JSON parsing error: {str(e)}")
            else:
                print("Received a non-200 response")
    return results

def calculate_similarity(actual_answer, expected_answer):
    embeddings_actual = get_embeddings_wrapper(actual_answer)
    embeddings_expected = get_embeddings_wrapper(expected_answer)
    similarity_score = np.dot(embeddings_actual, embeddings_expected)
    print("similarity_score", similarity_score)
    return similarity_score

def calculat_similarity_using_llm(actual_answer, expected_answer):
    prompt = f"""Decide whether the actual_answer is similar to expected_answer

    actual_answer : {actual_answer}

    expected_answer: {expected_answer}
    Is it Similar? Just respond True or False and then separated by a dash put a percentage of similarity and explain why you think is True or False:
    """
    llm = VertexAI()
    llm_response = llm(prompt)
    return llm_response

BATCH_SIZE = 5
def get_embeddings_wrapper(text):
    embs = []
    for i in range(0, len(text), BATCH_SIZE):
        time.sleep(1)
        result = text_embedding_model.get_embeddings(text)
        embs = embs + [e.values for e in result]
    return embs