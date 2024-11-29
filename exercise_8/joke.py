import requests

def fetch_python_joke():
    # Define the API endpoint and parameters
    url = "https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw&contains=python"
    params = {
        'category/ categories ': 'Programming',
        "language": "en - English",
        'flags': 'nsfw',
        'response format': 'json',
        'joke type': 'single, twopart',
        'search string': 'python',
        'ID range': '0 - 1367',
        'Amount': '1',
    }
    
    try:
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Parse the JSON response
        data = response.json()
        
        if data.get("error"):  # Check for API errors
            print("Error fetching the joke:", data["message"])
        else:
            # Check if the joke is single or two-part
            if data["type"] == "single":
                print(data["joke"])  # Print single-line joke
            elif data["type"] == "twopart":
                print(f"{data['setup']} - {data['delivery']}")  # Print two-part joke
    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching the joke:", e)

# Run the function
fetch_python_joke()
