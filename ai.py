
import openai

# Set your OpenAI API key
openai.api_key = ''

# Define your question
question = "create a detailed 5 day trip plan with a budget of $5000 for a family of 4 in New York City"

# Create a response using the updated model
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # Use gpt-3.5-turbo or gpt-4
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question}
    ],
    max_tokens=100
)

# Extract and print the response
trip_plan = response['choices'][0]['message']['content'].strip()
print(trip_plan)
