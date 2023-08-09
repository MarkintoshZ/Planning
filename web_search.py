from duckduckgo_search import DDGS

def search(query: str):
    return DDGS().text(query)

results = search("What is the capital of France?")
results = list(results)
print(results)