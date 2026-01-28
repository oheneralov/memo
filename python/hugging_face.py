"""
Hugging Face Transformers Examples
Demonstrates various use cases of the Hugging Face library
"""

# Example 1: Sentiment Analysis
def sentiment_analysis_example():
    """
    Perform sentiment analysis on text using a pre-trained model
    """
    from transformers import pipeline
    
    # Create a sentiment analysis pipeline
    classifier = pipeline("sentiment-analysis")
    
    # Analyze sentiments
    texts = [
        "I love this product! It's amazing!",
        "This is the worst experience ever.",
        "It's okay, nothing special."
    ]
    
    results = classifier(texts)
    
    print("=== Sentiment Analysis ===")
    for text, result in zip(texts, results):
        print(f"Text: {text}")
        print(f"Sentiment: {result['label']}, Score: {result['score']:.4f}\n")


# Example 2: Text Generation
def text_generation_example():
    """
    Generate text using GPT-2 model
    """
    from transformers import pipeline
    
    # Create a text generation pipeline
    generator = pipeline("text-generation", model="gpt2")
    
    prompt = "Artificial intelligence will change the world by"
    
    # Generate text
    results = generator(prompt, max_length=50, num_return_sequences=2)
    
    print("=== Text Generation ===")
    print(f"Prompt: {prompt}\n")
    for i, result in enumerate(results, 1):
        print(f"Generation {i}: {result['generated_text']}\n")


# Example 3: Named Entity Recognition (NER)
def named_entity_recognition_example():
    """
    Extract named entities from text
    """
    from transformers import pipeline
    
    # Create NER pipeline
    ner = pipeline("ner", grouped_entities=True)
    
    text = "Elon Musk founded SpaceX in 2002 and Tesla in 2003. He was born in South Africa."
    
    # Extract entities
    entities = ner(text)
    
    print("=== Named Entity Recognition ===")
    print(f"Text: {text}\n")
    print("Entities found:")
    for entity in entities:
        print(f"- {entity['word']}: {entity['entity_group']} (score: {entity['score']:.4f})")


# Example 4: Question Answering
def question_answering_example():
    """
    Answer questions based on given context
    """
    from transformers import pipeline
    
    # Create QA pipeline
    qa_pipeline = pipeline("question-answering")
    
    context = """
    The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France.
    It is named after the engineer Gustave Eiffel, whose company designed and built the tower.
    Constructed from 1887 to 1889, it was initially criticized by some of France's leading artists
    and intellectuals for its design, but it has become a global cultural icon of France and one
    of the most recognizable structures in the world. The tower is 330 meters tall.
    """
    
    questions = [
        "Who designed the Eiffel Tower?",
        "How tall is the Eiffel Tower?",
        "When was the Eiffel Tower built?"
    ]
    
    print("=== Question Answering ===")
    print(f"Context: {context[:100]}...\n")
    
    for question in questions:
        result = qa_pipeline(question=question, context=context)
        print(f"Q: {question}")
        print(f"A: {result['answer']} (confidence: {result['score']:.4f})\n")


# Example 5: Translation
def translation_example():
    """
    Translate text between languages
    """
    from transformers import pipeline
    
    # Create translation pipeline (English to French)
    translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
    
    texts = [
        "Hello, how are you?",
        "Machine learning is fascinating.",
        "I love programming with Python."
    ]
    
    print("=== Translation (English to French) ===")
    for text in texts:
        result = translator(text, max_length=100)
        print(f"English: {text}")
        print(f"French: {result[0]['translation_text']}\n")


# Main execution
if __name__ == "__main__":
    print("Hugging Face Transformers Examples\n" + "="*50 + "\n")
    
    # Run all examples
    # Note: First run will download models, which may take time
    
    try:
        sentiment_analysis_example()
        print("\n" + "-"*50 + "\n")
        
        text_generation_example()
        print("\n" + "-"*50 + "\n")
        
        named_entity_recognition_example()
        print("\n" + "-"*50 + "\n")
        
        question_answering_example()
        print("\n" + "-"*50 + "\n")
        
        translation_example()
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to install transformers: pip install transformers torch")
