from fastapi import FastAPI, UploadFile, File, HTTPException
import json
import asyncio
import aiohttp
from datetime import datetime
import pytz
from urllib.parse import quote
from utils import fetch, run_batch_tests

app = FastAPI()

@app.post("/upload-config-and-run-tests")
async def upload_and_test(file: UploadFile = File(...)):
    try:
        content = await file.read()
        config = json.loads(content)
        
        results_with_docs = await run_batch_tests(config)
        
        # Prepare results without source_documents for the response
        results_for_response = [{k: v for k, v in result.items() if k != 'source_documents'} for result in results_with_docs]

        return {"message": "Batch tests completed", "config": json.dumps(config['parameters']), "results": results_for_response}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in uploaded file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))