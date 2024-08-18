from flask import Flask, jsonify, request
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import random

app = Flask(__name__)

# Load the GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Enhanced joke prompts by category
joke_categories = {
    "tech": "Tell me a funny tech joke about programmers or computers.",
    "puns": "Share a clever pun that's guaranteed to make people laugh.",
    "animals": "Give me a hilarious joke about animals.",
    "kids": "Tell me a silly joke that kids would find funny.",
    "dad": "Tell me a classic dad joke that’s both cringy and funny.",
    "work": "Share a funny work-related joke about the office or jobs."
}

# Improved fallback jokes for each category
fallback_jokes = {
    "tech": [
        "Why do Java developers wear glasses? Because they can't C#!",
        "Why did the computer keep freezing? It left its Windows open!",
    ],
    "puns": [
        "I'm on a whiskey diet. I've lost three days already!",
        "I wondered why the baseball was getting bigger. Then it hit me."
    ],
    "animals": [
        "Why don’t some fish play piano? Because you can't tuna fish!",
        "Why do cows have hooves instead of feet? Because they lactose."
    ],
    "kids": [
        "What did the ocean say to the beach? Nothing, it just waved!",
        "Why was the math book sad? It had too many problems."
    ],
    "dad": [
        "How does a penguin build its house? Igloos it together.",
        "I'm reading a book on anti-gravity. It's impossible to put down!"
    ],
    "work": [
        "Why did the scarecrow get a promotion? He was outstanding in his field!",
        "Why don’t skeletons fight each other? They don't have the guts."
    ]
}

def generate_joke(category):
    # Get the appropriate prompt for the category
    prompt = joke_categories.get(category, "Tell me a joke that will make me laugh out loud.")
    
    # Encode the input and generate output
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=50, num_return_sequences=1, do_sample=True)
    
    # Decode the generated text
    joke = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Remove the prompt part from the joke (if present)
    if joke.lower().startswith(prompt.lower()):
        joke = joke[len(prompt):].strip()
    
    # Strip leading and trailing whitespace, including newline characters
    joke = joke.strip()
    
    # Ensure the joke starts with a capital letter
    joke = joke.capitalize()
    
    # Simple post-processing to ensure it's a complete joke
    if not joke.endswith('.'):
        joke += '.'
        
    # Check if the joke seems incomplete or irrelevant
    if len(joke.split()) < 6 or joke == ".":
        joke = random.choice(fallback_jokes.get(category, ["This is a fallback joke."]))
    
    return joke

@app.route('/generate_joke', methods=['GET'])
def generate_joke_endpoint():
    category = request.args.get('category', 'general').lower()
    joke = generate_joke(category)
    return jsonify({"joke": joke})

if __name__ == '__main__':
    app.run(debug=True)
