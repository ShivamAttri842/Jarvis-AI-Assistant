import speech_recognition as sr
import pyttsx3 as py
import datetime
import requests  
import os  
import webbrowser  
import pywhatkit 
import pyautogui 
import time  
import psutil
import subprocess
import eel
import threading

# Initialize the Speech Recognition
r = sr.Recognizer()

engine = py.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

# Hotword
hotword = "jarvis"  # Change this to your desired hotword

def say(text):
    engine.say(text)
    engine.runAndWait()

def listen_for_hotword():
    with sr.Microphone() as source:
        print("Listening for hotword...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        if hotword.lower() in command:
            return True
    except sr.UnknownValueError:
        pass
    return False

# Function to run the Eel application
def start_eel():
    eel.init('Jarvis-AI-Assistant')
    eel.start('index.html', size=(800, 600))

# Run Eel in a separate thread
eel_thread = threading.Thread(target=start_eel)
eel_thread.start()

# Function to listen for command after hotword
def listen():
    while True:
        if listen_for_hotword():
            say("Yes Sir")
            break
        else:
            print("Please say the hotword to activate me.")
    while True:
        with sr.Microphone() as source:
            print("Listening for command...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=10)

        try:
            print('Recognizing...')
            say("Recognizing...")

            command = r.recognize_google(audio).lower()
            print(command)

            if hotword.lower() in command:
                continue
            else:
                return command

        except sr.UnknownValueError:
            return ""

# Define intent recognition
def recognize_intent(command):
    intent = None

    intents = {
        "weather_intent": ["weather", "forecast", "temperature"],
        "news_intent": ["news", "headlines"],
        "music_intent": ["play", "music", "play music"],
        "search_intent": ["search", "find", "look up"],
        "calculator_intent": ["calculate", "math", "mathematics"],
        "open_app_intent": ["open", "launch", "start"],
        "close_app_intent": ["close", "quit", "exit"],
        "volume_intent": ["volume", "sound", "loudness"],
        # Add more intents and keywords as needed
    }

    for intent_name, keywords in intents.items():
        for keyword in keywords:
            if keyword in command:
                intent = intent_name
                break

    return intent

# Function to greet the user
def greet_user():
    current_time = datetime.datetime.now()
    if current_time.hour < 12:
        return "Good morning! Sir"
    elif 12 <= current_time.hour < 17:
        return "Good afternoon! Sir"
    elif 17 <= current_time.hour < 20:
        return "Good evening! Sir"
    else:
        return " "

# Function To Calculate Mathematical Expression
def Calculate(expression):
    try:
        result = eval(expression)
        print(result)

    except Exception as e:
        print("Please write the expression again")

OPENWEATHER_API_ID = "4450649825b5fee22f5bb1d2f35d6714"                     
# Function to get weather report
def get_weather_report(city):
    try:
        # Make sure to handle potential errors in the API request
        res = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_ID}&units=metric"
        )
        res.raise_for_status()  # Raise an HTTPError for bad responses
        data = res.json()

        weather = data["weather"][0]["main"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]

        return weather, f"{temperature}℃", f"{feels_like}℃"
    except requests.RequestException as e:
        # Handle any request exceptions (e.g., network issues, API errors)
        print(f"Error during API request: {e}")
        return None

# To Close Application
def close_specific_app(app_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if app_name.lower() in proc.info['name'].lower():
            try:
                process = psutil.Process(proc.info['pid'])
                process.terminate()
                say(f"Closing {app_name}.")
                return True
            except Exception as e:
                say(f"Failed to close {app_name}.")
                return False
    say(f"{app_name} is not currently running.")
    return False

if __name__ == "__main__":
    say("Initializing Jarvis.")
    say(greet_user())
    say("I am Jarvis. Your personal voice assistant")
    say("How can I assists you today...")
    while True:
        command = listen()
        intent = recognize_intent(command)

        # To tell Weather Report
        if intent == "weather_intent":
            try:
                # Handle weather-related commands
                print(" You want to know the weather. I'll find that for you.")
                city = "Rohtak"
                print(f"Getting weather report for your city {city}")

                weather_info = get_weather_report(city)

                if weather_info:
                    weather, temperature, feels_like = weather_info
                    say(f"The current temperature is {temperature}, but it feels like {feels_like}")
                    say(f"Also, the weather report talks about {weather}")
                    say("For your convenience, I am printing it on the screen, sir.")
                    print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
                else:
                    print(": Failed to retrieve weather information.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        # To tell News
        elif intent == "news_intent":
            say("You want to know the latest news. Let me fetch that for you.")
            search_url = f"https://www.google.com/search?rlz=1C1YTUH_en-GBIN1081IN1081&oq=google+conv&gs_lcrp=EgZjaHJvbWUqBwgEEAAYgAQyBggAEEUYOTINCAEQABiDARixAxiABDIMCAIQABgUGIcCGIAEMgcIAxAAGIAEMgcIBBAAGIAEMgcIBRAAGIAEMgcIBhAAGIAEMgcIBxAAGIAEMgcICBAAGIAEMgcICRAAGIAE0gEIOTk0OWowajeoAgCwAgA&sourceid=chrome&ie=UTF-8&cs=0&csui=1&gsas=1&csuio=6&csuip=15&q=India%27s+top+10+news+in+English&mstk=AUzJOivMg2Vop2zlYweepzttTiRoK5djU-QPvjds8M9Jaf3wQ1efvQqtoV4POmaZjOCAfmwa3l7o9FrAcEauY4vvbbecOre33BJwFFpMS60l1zBwfpUUEqs6hUZfltrpTpDXKTrmJg4-kHcmbMwx7kpXfC8Be_yiQXd85D1g0VEtzbdq-NDLh1kuyLAeh8-oWJGpQUUVzUmL6drIwGszxTju1bkCi5OFSDcn8QQutrV2F29btKtwGDOlAQKAY5bzL9KU&csuir=1"
            webbrowser.open(search_url)

        # To play Music
        elif intent == "music_intent":
            search_music = command.replace("music_intent", "").strip()
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome")
            music_query = search_music
            pywhatkit.playonyt(music_query)

        # To Search on Google
        elif "google search"in command:
            search_query = command.replace("google search", "").strip()
            search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(search_url)
            response = "I've opened a Google search for you."

        elif "youtube search" in command:
            search_query = command.replace("youtube search", "").strip()
            search_url = f"https://www.youtube.com/search?q={search_query}"
            webbrowser.open(search_url)
            response = "I've opened a youtube search for you."

        # To Calculate Something
        elif intent == "calculator_intent":
            # Handle calculator-related commands
            say("What math expression would you like me to calculate?")
            math_expression = listen()
            Calculate(math_expression)

        # To Open Any Application
        elif intent == "open_app_intent":
            # Handle app opening commands
            if "chrome" in command.lower():
                say("Opening Chrome.")
                os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome")  
            elif "facebook" in command.lower():
                say("Opening YouTube.")
                webbrowser.open("https://facebook.com")
            elif "linkedin" in command.lower():
                say("Opening YouTube.")
                webbrowser.open("https://linkedin.com")
            elif "youtube" in command.lower():
                say("Opening YouTube.")
                webbrowser.open("https://youtube.com")
            elif "settings" in command.lower():
                say("Opening Settings.")
                os.system("start ms-settings:")
            elif "control panel" in command.lower():
                say("Opening Control Panel.")
                os.system("control")
            elif "command prompt" in command.lower():
                say("Opening Command Prompt.")
                os.system("cmd")
            elif "file explorer" in command.lower():
                say("Opening File Explorer.")
                os.system("explorer")
            elif "calculator" in command.lower():
                say("Opening Calculator.")
                os.startfile("C:\\Windows\\System32\\calc.exe")
            # Add more applications to open as needed
            else:
                say("Sorry, I couldn't recognize the application you want to open.")

        # To Close Any Application
        elif intent == "close_app_intent":
            # Handle app closing commands
            if "chrome" in command.lower():
                if close_specific_app("chrome.exe"):
                    say("Closing Google Chrome.")
                    subprocess.run(f'taskkill /f /im chrome.exe', shell=True, check=True)
            elif "settings" in command.lower():
                if close_specific_app("ImmersiveControlPanel.exe"):
                    say("Closing Settings.")
                    subprocess.run(f'taskkill /f /im ImmersiveControlPanel.exe', shell=True, check=True)
            elif "control panel" in command.lower():
                if close_specific_app("control.exe"):
                    say("Closing Control Panel.")
                    subprocess.run(f'taskkill /f /im control.exe', shell=True, check=True)
            elif "command prompt" in command.lower():
                if close_specific_app("cmd.exe"):
                    say("Closing Command Prompt.")
                    subprocess.run(f'taskkill /f /im cmd.exe', shell=True, check=True)
            elif "file explorer" in command.lower():
                if close_specific_app("explorer.exe"):
                    say("Closing File Explorer.")
                    subprocess.run(f'taskkill /f /im explorer.exe', shell=True, check=True)
            elif "notepad" in command.lower():
                if close_specific_app("notepad.exe"):
                    say("Closing Notepad.")
                    subprocess.run(f'taskkill /f /im notepad.exe', shell=True, check=True)
            elif "calculator" in command.lower():
                if close_specific_app("calc.exe"):
                    say("Closing Calculator.")
                    subprocess.run(f'taskkill /f /im calc.exe', shell=True, check=True)
            # Add more applications to close as needed
            else:
                say("Sorry, I couldn't recognize the application you want to close.")
                                                                                                        
        # To Increase or Decrease Volume 
        elif intent == "volume_intent":
            # Handle volume control commands
            if "volume up" in command or "increase volume" in command:
                for _ in range(30):
                    pyautogui.press("volumeup")
            elif "volume down" in command or "decrease volume" in command:
                for _ in range(30):
                    pyautogui.press("volumedown")

        # To Stop Jarvis for some time
        elif "pause" in command.lower() or "sleep" in command.lower() or "rest" in command.lower():
            # Handle pausing Jarvis
            say("For how much time would you like me to pause? (Specify the number of minutes)")
            try:
                minutes = int(input("Enter time in minutes (Only Number): "))  # Corrected the missing closing parenthesis
                seconds = minutes * 60
                say(f"Jarvis will be paused for {minutes} minutes.")
                time.sleep(seconds)
                say("I'm back! How can I assist you?")

            except ValueError:
                say("Invalid input. Please enter a valid number of minutes.")

        # To Stop Permanently
        elif any(keyword in command.lower() for keyword in ["goodbye", "good bye", "exit"]):
            # Handle exit commands
            say("Goodbye Sir")
            print("Goodbye, Sir")
            break

        # To Maximize this window
        elif 'maximise this window' or 'maximise the window' in command.lower():
            pyautogui.hotkey('win', 'up')
        # To Minimize the window
        elif 'minimise this window' or 'minimise the window' in command.lower():
            pyautogui.hotkey('win', 'down')
        # To Open New Window
        elif 'open new window' or 'open a new tab' in command.lower():
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome")
            pyautogui.hotkey('ctrl', 'n')
        # To Open Incognito Window
        elif 'open incognito window' or 'open incognito tab' in command.lower():
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome")
            pyautogui.hotkey('ctrl', 'shift', 'n')
        # To Open History Of Chrome
        elif 'open history' in command.lower():
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome")
            pyautogui.hotkey('ctrl', 'h')
        # To Open Download History
        elif 'open downloads' in command.lower():
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome")
            pyautogui.hotkey('ctrl', 'j')
        # To Clear Browsing History
        elif 'clear browsing history' in command.lower():
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome")
            pyautogui.hotkey('ctrl', 'shift', 'delete')
        # To Open Previous tab
        elif 'previous tab' in command.lower():
            pyautogui.hotkey('ctrl', 'shift', 'tab')
        # To Open Next Tab
        elif 'next tab' in command.lower():
            pyautogui.hotkey('ctrl', 'tab')
        # To reload the site
        elif "reload" in command.lower():
            pyautogui.hotkey('ctrl', 'r')
        # To pause youtube video
        elif "pause" in command.lower() :
            pyautogui.hotkey('k')
            if "resume" in command.lower():
                pyautogui.hotkey('k')
        # To Thank
        elif "thank you" in command.lower() or "thanks" in command.lower():
            say("Welcome Sir")

        else:
            print("command is not acceptable")
            say("command is not acceptable")
