from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/outline")
async def get_country_outline(country: str):
    """Fetch the Wikipedia page for a given country and create a Markdown outline of its headings."""
    wikipedia_url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"

    try:
        response = requests.get(wikipedia_url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=404, detail="Wikipedia page not found.")

    # Parse the Wikipedia page with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all headings (H1 to H6)
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    if not headings:
        raise HTTPException(status_code=404, detail="No headings found on the Wikipedia page.")

    # Generate a Markdown outline
    markdown_outline = "## Contents\n\n"
    for heading in headings:
        level = int(heading.name[1])  # Get the heading level (1-6)
        text = heading.get_text().strip()
        markdown_outline += f"{'#' * level} {text}\n\n"

    return {"country": country, "markdown_outline": markdown_outline}
