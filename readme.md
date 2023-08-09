# Design Doc

## Flowchart

- Create a query plan based on question (few shot prompting)
- Select first item and choose an action (search [keyword(s)])
- Choose an action based on search result (search, navigate, output partial)
- If on a page, choose action (find relevant segments using embedding, in-page search)
- Given relevant segments, choose action (navigate, output partial, end)

## Possible cases

### Initial bootstraping

```
Create a step-by-step search engine query plan that fulfills the given command by user.

Command: Answer the question: Who wrote the play 'Hamlet,' and where was he born?

Plan:
1. search the author of 'Hamlet'
2. search where the author was born in
3. compose answer

Command: Answer the question: Who are the current Prime Ministers of the UK and Canada, and who has a higher educational background?

Plan:
1. search for the Prime Minister of UK
2. search for the Prime Minister of Canada
3. compose answer by comparing educatoin backgrounds

Command: {{command or question}}
{{gen}}
```

### Pre Action

```
Final Goal: {{}}
Current answer: {{}}
Plan: {{}}
Available Actions:
- web-search [keywords] (search keywords using a search engine)
- semantic-memory-search [text] (search for semantically similar text segments to answer question)
- edit-answer [new-answer] (edit and update the current answer)
- navigate [url] (navigate to the given url)
- terminate
```

### Post Action

```
...
Action: {{chosen action}}
Result: ...

Updated plan: {{gen}}
```
