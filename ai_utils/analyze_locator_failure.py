import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_locator(page_source, failed_locator):
    prompt = f"""
You are a test automation expert.

A Selenium locator failed:
{failed_locator}

Here is the HTML DOM:
{page_source}

Suggest 3 alternative stable locators.
Return only locator suggestions.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content
