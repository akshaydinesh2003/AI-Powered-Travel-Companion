import openai

openai.api_key = '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'

def generate_trip_plan(destination, budget, days):
    question = (
        f"Create a travel itinerary for {days} days to {destination} "
        f"with a budget of ${budget}. Include key attractions and activities."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating trip plan: {str(e)}"
