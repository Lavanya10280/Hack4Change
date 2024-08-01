from transformers import pipeline

# Test the pipeline
summarizer = pipeline("summarization")
print(summarizer("This is a test text for summarization. It should be summarized correctly."))
