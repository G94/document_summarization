SUMMARY_PROMPT = """
You are an assistant that summarizes information.
Summarize the following document, keep the main aspects,do not include irrelevant information.

Context:
{context}

User query: {query}
"""


SUMMARY_PROMPT_DOC = """
You are an assistant that summarizes papers about social science.
Summarize the following document, keep the main aspects,
do not include irrelevant information.

Document content:
{document_content}

summary:

"""