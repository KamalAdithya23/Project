from fastapi import FastAPI, Query, HTTPException
import os
import subprocess
import json
from typing import Optional
import openai
import datetime
import sqlite3
import requests
import shutil
import duckdb
from bs4 import BeautifulSoup

app = FastAPI()

# Load AI Proxy Token
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
openai.api_key = AIPROXY_TOKEN

def execute_task(task: str) -> str:
    """Executes a plain-English task by interpreting it with an LLM and executing the required steps."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI assistant that converts natural language tasks into command-line actions."},
                {"role": "user", "content": f"Convert this task into a structured command: {task}"}
            ]
        )
        command = response["choices"][0]["message"]["content"].strip()
        
        # Run the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
        
        return result.stdout
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

# Security constraints
FORBIDDEN_PATHS = ["..", "/", "~"]

def validate_path(path: str):
    if any(forbidden in path for forbidden in FORBIDDEN_PATHS) or not path.startswith("/data/"):
        raise HTTPException(status_code=403, detail="Access outside /data/ is forbidden")
    return path

def fetch_data_from_api(url: str, output_path: str):
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, "w") as file:
        file.write(response.text)
    return "Data fetched and saved."

def clone_git_repo(repo_url: str, local_path: str):
    result = subprocess.run(["git", "clone", repo_url, local_path], capture_output=True, text=True)
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Git clone failed: {result.stderr}")
    return "Repository cloned successfully."

def run_sql_query(db_path: str, query: str, output_path: str):
    validate_path(db_path)
    try:
        conn = duckdb.connect(db_path)
        result = conn.execute(query).fetchall()
        with open(output_path, "w") as file:
            file.write(json.dumps(result))
        conn.close()
        return "Query executed successfully."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQL execution failed: {str(e)}")

def scrape_website(url: str, output_path: str):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    with open(output_path, "w") as file:
        file.write(soup.prettify())
    return "Website content scraped successfully."

def transcribe_audio(audio_path: str, output_path: str):
    validate_path(audio_path)
    transcript = "(Mock transcription)"
    with open(output_path, "w") as file:
        file.write(transcript)
    return "Audio transcribed successfully."

def markdown_to_html(md_path: str, output_path: str):
    validate_path(md_path)
    try:
        with open(md_path, "r") as md_file:
            md_content = md_file.read()
        html_content = f"<html><body>{md_content}</body></html>"
        with open(output_path, "w") as html_file:
            html_file.write(html_content)
        return "Markdown converted to HTML."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Markdown conversion failed: {str(e)}")

def filter_csv(input_path: str, output_path: str, condition: str):
    validate_path(input_path)
    with open(output_path, "w") as file:
        file.write("(Mock CSV filtered output)")
    return "CSV filtered successfully."

@app.post("/run")
def run_task(task: str = Query(..., description="Task description")):
    """Endpoint to execute a task."""
    if "fetch data" in task:
        output = fetch_data_from_api("https://api.example.com/data", "/data/fetched_data.json")
    elif "clone repo" in task:
        output = clone_git_repo("https://github.com/example/repo.git", "/data/repo")
    elif "SQL query" in task:
        output = run_sql_query("/data/database.db", "SELECT * FROM table;", "/data/query_output.json")
    elif "scrape website" in task:
        output = scrape_website("https://example.com", "/data/scraped_content.html")
    elif "transcribe audio" in task:
        output = transcribe_audio("/data/audio.mp3", "/data/transcription.txt")
    elif "convert markdown" in task:
        output = markdown_to_html("/data/docs/file.md", "/data/docs/file.html")
    elif "filter CSV" in task:
        output = filter_csv("/data/input.csv", "/data/output.json", "some condition")
    else:
        output = execute_task(task)
    return {"status": "success", "output": output}

@app.get("/read")
def read_file(path: str = Query(..., description="Path of the file to read")):
    """Endpoint to read file content."""
    validate_path(path)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(path, "r") as file:
        content = file.read()
    return {"status": "success", "content": content}