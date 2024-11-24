from transformers import pipeline

def summarize_text(text: str):
    """
    Gera um resumo para o texto fornecido usando o modelo especificado.
    
    :param text: O texto a ser resumido.
    :return: O resumo gerado.
    """
    summarizer = pipeline("summarization", model='facebook/bart-large-cnn')
    summary = summarizer(text, do_sample=False)
    return summary[0]["summary_text"]