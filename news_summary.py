from transformers import AutoTokenizer, TFPegasusForConditionalGeneration
from transformers import pipeline


def summarize_news_pegasus(news_content):
    model = TFPegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
    tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")

    inputs = tokenizer(news_content, min_length=10, max_length=200, return_tensors="tf")

    summary_ids = model.generate(inputs)
    summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
    return summary


def summarize_news_distilbart(news_content):
    pipe = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", min_length=10, max_length=200)
    summary = pipe(news_content)
    return summary

