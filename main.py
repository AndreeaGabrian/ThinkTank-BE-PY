import json

from fastapi import FastAPI, HTTPException
import requests
from news_summary import summarize_news_distilbart
from db_operations import insert_multiple_news

app = FastAPI()
NEWS_API_KEY = "6464cb692c1d4d388b9f3604c3e5faa2"

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get_news")
async def top_headlines_sources():
    url = "https://newsapi.org/v2/top-headlines?category=business&language=en"
    params = {"apiKey": NEWS_API_KEY}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful

        data = response.json()
        # Extracting only the desired keys from each article
        articles = []
        data2 = data["articles"]
        for article in data2[:10]:
            content = article["content"]
            if content is None or "":
                continue
            summary = summarize_news_distilbart(content)

            new_article = {
                "date": article["publishedAt"],
                "link": article["url"],
                "summary": summary[0]["summary_text"],
                "title": article["title"],
                "source": article["source"]["name"],

            }
            articles.append(new_article)

        # Write the data to a JSON file
        with open('output.json', "w") as json_file:
            json.dump(articles, json_file, indent=2)
        insert_multiple_news(articles)
        # return {"articles": articles}
        return True
    except requests.RequestException as e:
        # If an error occurs during the request, raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail="Failed to fetch top headlines sources") from e


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="localhost", port=8001)





