import openai
import gradio
import random
import googlemaps
import re

# Set up OpenAI API key
openai.api_key = "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"

# Set up Google Maps API client with your API key
gmaps = googlemaps.Client(key="AIzaSyBc-1kcyRAyT7QTVeBQtRsPiX5-e1D3srw")

# Chatbot messages
messages = [{"role": "system", "content": "You are a healthcare assistant that specializes in medical advice"}]

# Sample health tips (you can add more tips to this list)
health_tips_list = [
    "Drink plenty of water.",
    "Get regular exercise.",
    "Eat a balanced diet with fruits and vegetables.",
    "Get enough sleep each night.",
    "Practice stress-relief techniques like meditation or yoga.",
    "Avoid smoking and limit alcohol consumption.",
    "Wash your hands frequently to prevent the spread of germs.",
    "Maintain a healthy weight through diet and exercise.",
    "Limit your intake of processed and sugary foods.",
    "Stay physically active throughout the day.",
    "Take breaks from sitting and move around.",
    "Practice good hygiene, including brushing and flossing your teeth.",
    "Use sunscreen to protect your skin from UV rays.",
    "Limit your exposure to harmful pollutants and chemicals.",
    "Stay up-to-date with vaccinations.",
    "Practice safe sex and use protection.",
    "Avoid excessive sun exposure to prevent skin damage.",
    "Keep your home and workplace clean and free of clutter.",
    "Maintain good posture to prevent back and neck pain.",
    "Limit screen time and take regular breaks from electronic devices.",
    "Engage in activities that bring you joy and reduce stress.",
    "Spend time outdoors and connect with nature.",
    "Avoid excessive consumption of caffeine and sugary drinks.",
    "Include probiotics in your diet to support gut health.",
    "Practice mindful eating and listen to your body's hunger cues.",
    "Engage in regular physical activity, such as walking or biking.",
    "Practice deep breathing exercises to reduce stress and anxiety.",
    "Get regular check-ups and screenings to monitor your health.",
    "Limit your intake of processed meats and high-fat foods.",
    "Engage in hobbies and activities that promote mental well-being.",
    "Stay socially connected with friends and family.",
    "Practice proper handwashing to prevent the spread of germs.",
    "Get enough vitamin D through sunlight or supplements.",
    "Limit your exposure to secondhand smoke.",
    "Avoid excessive alcohol consumption.",
    "Stay hydrated by drinking water throughout the day.",
    "Limit your intake of added sugars and salt.",
    "Practice gratitude and focus on positive aspects of life.",
    "Use relaxation techniques to manage stress and anxiety.",
    "Take breaks and stretch if you have a sedentary job.",
    "Practice good sleep hygiene for better sleep quality.",
    "Limit your intake of processed and fried foods.",
    "Engage in regular cardiovascular exercise to strengthen your heart.",
    "Avoid prolonged exposure to loud noises.",
    "Practice safe driving habits and wear seat belts.",
    "Limit your exposure to environmental toxins.",
    "Practice safe lifting techniques to avoid back injuries.",
    "Get regular eye exams to monitor your vision health.",
    "Limit your intake of trans fats and saturated fats.",
    "Engage in activities that challenge your brain and memory.",
    "Practice good oral hygiene for healthy teeth and gums.",
]

# Function to get health tips
def get_health_tips(num_tips=1):
    num_tips_available = len(health_tips_list)
    num_tips_to_provide = min(num_tips, num_tips_available)
    health_tips = random.sample(health_tips_list, num_tips_to_provide)
    return health_tips

# Function to get nearby places using Google Maps API
def get_nearby_places(location, place_type):
    places_result = gmaps.places_nearby(location=location, radius=5000, type=place_type)
    places_names = [place["name"] for place in places_result["results"]]
    return places_names

# Function to geocode the user's input address
def geocode_address(address):
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return f"{lat},{lng}"
    else:
        return None

# Function to perform actions based on user input
def perform_action(user_input):
    if "symptom" in user_input.lower():
        return "SYMPTOM_CHECK"
    elif "health tips" in user_input.lower():
        return "GET_HEALTH_TIPS"
    elif "hospital" in user_input.lower() and "helpline" in user_input.lower():
        return "NEARBY_HOSPITALS_AND_HELPLINE"
    elif "hospital" in user_input.lower():
        return "NEARBY_HOSPITALS"
    elif "helpline" in user_input.lower():
        return "NEARBY_HELPLINE"
    else:
        return "DEFAULT_ACTION"

# Function to perform symptom checking logic (you need to implement this)
def perform_symptom_check(symptom):
    # Construct the messages with system and user inputs
    messages = [{"role": "system", "content": "You are a healthcare assistant that specializes in medical advice"},
                {"role": "user", "content": symptom}]

    # Make the API call to OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Get the chatbot's response from the API response
    chatbot_response = response["choices"][0]["message"]["content"]

    return chatbot_response

# Main chatbot function
def CustomChatGPT(user_input):
    action = perform_action(user_input)

    messages.append({"role": "user", "content": user_input})

    if action == "SYMPTOM_CHECK":
        symptom = user_input  # Use user input as the symptom for demonstration purposes
        ChatGPT_reply = perform_symptom_check(symptom)
    elif action == "GET_HEALTH_TIPS":
        num_tips_requested = 1  # Default number of tips to provide
        num_tips_match = re.search(r'\b\d+\b', user_input)
        if num_tips_match:
            num_tips_requested = int(num_tips_match.group())

        num_tips_available = len(health_tips_list)
        num_tips_to_provide = min(num_tips_requested, num_tips_available)

        if num_tips_to_provide == 0:
            ChatGPT_reply = "I'm sorry, I currently don't have any health tips available."
        else:
            health_tips = get_health_tips(num_tips=num_tips_to_provide)
            ChatGPT_reply = f"Sure! Here are {num_tips_to_provide} health tips:\n"
            ChatGPT_reply += "\n".join(health_tips)
            if num_tips_requested > num_tips_available:
                ChatGPT_reply += f"\n\nI currently have {num_tips_available} health tips available, so I can provide up to {num_tips_available} tips at the moment."
    elif action == "NEARBY_HOSPITALS":
        # Ask the user for their location
        ChatGPT_reply = "Please provide your location for finding nearby hospitals. For example, you can say 'This is my location ' Your Location ' '"
    
    elif action == "NEARBY_HELPLINE":
        # Ask the user for their location
        ChatGPT_reply = "Please provide your location for finding nearby helpline numbers. For example, you can say 'This is my location ' Your Location ''"
        
    elif action == "NEARBY_HOSPITALS_AND_HELPLINE":
        # User provided location, extract location from input
        location_match = re.search(r'in\s+(.*)', user_input, re.IGNORECASE)
        if location_match:
            address = location_match.group(1).strip()
            # Geocode the user's address to get latitude and longitude
            location = geocode_address(address)
            if location:
                nearby_hospitals = get_nearby_places(location, "hospital")
                nearby_helpline_numbers = get_nearby_places(location, "helpline")
                ChatGPT_reply = f"Here are some nearby hospitals: {', '.join(nearby_hospitals)}\n"
                ChatGPT_reply += f"And here are some nearby helpline numbers: {', '.join(nearby_helpline_numbers)}"
            else:
                ChatGPT_reply = "I'm sorry, I couldn't find a valid location in your input. Please provide your location to get nearby hospitals and helpline numbers."
        else:
            ChatGPT_reply = "I'm sorry, I couldn't find a valid location in your input. Please provide your location to get nearby hospitals and helpline numbers."
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        ChatGPT_reply = response["choices"][0]["message"]["content"]

    messages.append({"role": "assistant", "content": ChatGPT_reply})

    return ChatGPT_reply

# Create the Gradio interface for the healthcare assistant
healthcare_interface = gradio.Interface(
    fn=CustomChatGPT,
    inputs="text",
    outputs="text",
    title="Healthcare Assistant",
    theme="default",
    description="Ask me anything about health!",
    examples=[
        ["What are the symptoms of the common cold?"],
        ["What is the recommended daily water intake?"],
        ["How can I prevent the flu?"],
    ],
)

# Define the main function to launch the website
def main():
    healthcare_interface.launch(share=True)

if __name__ == "__main__":
    main()
