from flask import Flask, request, jsonify
from sympy import symbols, simplify, sqrt, diff, integrate
import plotly.graph_objs as go
import plotly
import json

app = Flask(__name__)

def is_math_question(prompt):
    # Simple check for mathematical symbols or keywords
    math_keywords = ['+', '-', '*', '/', 'sqrt', 'square', 'root', 'integral', 'derivative']
    return any(keyword in prompt for keyword in math_keywords)

def is_greeting(prompt):
    # Enhanced check for greetings and common follow-up questions
    greetings = {
        'hello': "Hello there! How can I assist you with your math problems today?",
        'hi': "Hi! Ready to dive into some math?",
        'greetings': "Greetings! What math problem can I help you with today?",
        'hey': "Hey! Got any math questions for me?",
        'good morning': "Good morning! Let's solve some math problems.",
        'good afternoon': "Good afternoon! What math challenges can I help you with?",
        'good evening': "Good evening! Ready for some math?",
        'how are you': "I'm a chatbot, so I don't have feelings, but I'm ready to help you with math!",
        "what's up": "Just here, ready to solve some math. What's up with you?",
        'howdy': "Howdy! What math problems can we tackle today?",
        'sup': "Not much, just ready to solve some math. Sup with you?",
        'yo': "Yo! Ready to crunch some numbers?"
    }
    
    # Check if the prompt is a greeting
    for greeting, response in greetings.items():
        if greeting in prompt.lower():
            return True, response
    
    return False, ""



def calculate_math_answer(prompt):
    try:
        # Define the symbol
        x = symbols('x')
        
        # Check for specific math operations and calculate accordingly
        if 'sqrt' in prompt:
            # Extract the expression inside sqrt
            expression = prompt.split('sqrt')[1].strip()
            answer = sqrt(simplify(expression))
        elif 'square' in prompt:
            # Extract the expression to square
            expression = prompt.split('square')[1].strip()
            answer = simplify(expression) ** 2
        elif 'root' in prompt:
            # Extract the expression and degree for the root
            degree, expression = prompt.split('root')[1].strip().split('of')
            answer = simplify(expression) ** (1 / int(degree))
        elif 'integral' in prompt:
            # Extract the expression to integrate
            expression = prompt.split('integral')[1].strip()
            answer = integrate(simplify(expression), x)
        elif 'derivative' in prompt:
            # Extract the expression to differentiate
            expression = prompt.split('derivative')[1].strip()
            answer = diff(simplify(expression), x)
        else:
            # Simplify the mathematical expression
            answer = simplify(prompt)
        
        return str(answer)
    except Exception as e:
        # If sympy can't process the expression, return None
        print("Error in calculate_math_answer:", e)
        return None

def plot_function(prompt):
    x = symbols('x')
    try:
        function = prompt.split('plot ')[1]
        # Convert the SymPy objects to floats before serialization
        y_values = [float(simplify(function).subs(x, i)) for i in range(-10, 11)]
        p = go.Figure(data=[go.Scatter(x=[i for i in range(-10, 11)], y=y_values)])
        graphJSON = json.dumps(p, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
    except Exception as e:
        print("Error in plot_function:", e)
        return None

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data['prompt']
    
    is_greet, greet_response = is_greeting(prompt)
    if is_greet:
        # Respond to greetings
        return jsonify({'text': greet_response})
    elif is_math_question(prompt):
        # If it's a math question, calculate the answer
        answer = calculate_math_answer(prompt)
        if answer:
            return jsonify({'text': answer})
        else:
            return jsonify({'text': "I'm sorry, I couldn't understand the math problem. Could you please rephrase it?"})
    elif 'plot' in prompt.lower():
        # If it's a plot request, generate the plot
        plot_data = plot_function(prompt)
        if plot_data:
            return jsonify({'text': 'Here is your plot:', 'plot_data': plot_data})
        else:
            return jsonify({'text': "I'm sorry, I couldn't understand the function to plot. Could you please rephrase it?"})
    else:
        return jsonify({'text': "I'm sorry, I can only help with plotting functions and simple math problems."})


if __name__ == '__main__':
    app.run(debug=True)
