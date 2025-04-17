#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
#from dotenv import dotenv_values
#import os
#import mtranslate as mt
#
#env_vars = dotenv_values(".env")
#
#InputLanguage = env_vars.get("InputLnaguage")
#
#HtmlCode = '''<!DOCTYPE html>
#<html lang="en">
#<head>
#    <title>Speech Recognition</title>
#</head>
#<body>
#    <button id="start" onclick="startRecognition()">Start Recognition</button>
#    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
#    <p id="output"></p>
#    <script>
#        const output = document.getElementById('output');
#        let recognition;
#
#        function startRecognition() {
#            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
#            recognition.lang = '';
#            recognition.continuous = true;
#
#            recognition.onresult = function(event) {
#                const transcript = event.results[event.results.length - 1][0].transcript;
#                output.textContent += transcript;
#            };
#
#            recognition.onend = function() {
#                recognition.start();
#            };
#            recognition.start();
#        }
#
#        function stopRecognition() {
#            recognition.stop();
#            output.innerHTML = "";
#        }
#    </script>
#</body>
#</html>'''
#
#HtmlCode= str(HtmlCode).replace("recognition.lang = '';",f"recognition.lang='{InputLanguage}';")
#
#with open(r"Data\Voice.html","w") as f:
#    f.write(HtmlCode)
#
#current_dir = os.getcwd()
#
#Link = f"{current_dir}/Data/Voice.html"
#
#chrome_options = Options()
#user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
#chrome_options.add_argument(f'user-agent={user_agent}')
#chrome_options.add_argument("--use-fake-ui-for-media-stream")
#chrome_options.add_argument("--use-fake-device-for-media-stream")
#chrome_options.add_argument("--headless=new")
#
#Service=Service(ChromeDriverManager().install())
#driver = webdriver.Chrome(service=Service,options = chrome_options)
#
#TempDirPath = rf"{current_dir}/Frontend/Files"
#
#def SetAssistantStatus(Status):
#    with open(rf'{TempDirPath}/status.data',"w",encoding='utf-8') as file:
#        file.write(Status)
#
#def QueryModifier(Query):
#    new_query=Query.lower().strip()
#    query_words= new_query.split()
#    question_words=["how","what","who","where","when","why","which","whose","whom","can you","what's","where's","how's"]
#    
#    if any(word + " "  in new_query for word in question_words):
#        if query_words[-1][-1] in ['.','?','!']:
#            new_query=new_query[:-1] + "?"
#        else:
#         new_query += "?"
#    else:
#        if query_words[-1][-1] in ['.','?','!']:
#            new_query=new_query[:-1] + "."
#        else:
#             new_query += "."
#    return new_query.capitalize()
#
#def UniversalTranslator(Text):
#    english_translation = mt.translate(Text,"en","auto")
#    return english_translation.capitalize()
#
#def SpeechRecognition():
#    driver.get("file:///" + Link)
#
#    driver.find_element(by=By.ID,value="start").click
#
#    while True:
#        try:
#            Text = driver.find_element(by=By.ID,value="output").text
#
#            if Text:
#                driver.find_element(by=By.ID,value="end").click()
#
#                if  InputLanguage.lower()=="en" or "en" in InputLanguage.lower():
#                    return QueryModifier(Text)
#                else:
#                    SetAssistantStatus("Translating...")
#                    return  QueryModifier(UniversalTranslator(Text))
#        except Exception as e:
#            pass
#
#if __name__=="__main__":
#    while True:
#        Text = SpeechRecognition()
#        print(Text)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import time

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-US")  # Default to English if not set

# Create HTML file with speech recognition
HtmlCode = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start">Start Recognition</button>
    <button id="end">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;
        let finalTranscript = '';

        document.getElementById('start').addEventListener('click', () => {{
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = '{InputLanguage}';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            recognition.onresult = (event) => {{
                const transcript = event.results[0][0].transcript;
                finalTranscript += transcript + ' ';
                output.textContent = finalTranscript;
            }};

            recognition.onerror = (event) => {{
                console.error('Recognition error:', event.error);
            }};

            recognition.start();
            console.log('Recognition started');
        }});

        document.getElementById('end').addEventListener('click', () => {{
            if (recognition) {{
                recognition.stop();
                console.log('Recognition stopped');
            }}
        }});
    </script>
</body>
</html>'''

# Ensure directories exist
os.makedirs("Data", exist_ok=True)
html_path = os.path.join("Data", "Voice.html")
with open(html_path, "w") as f:
    f.write(HtmlCode)

# Chrome options setup
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
# Run in non-headless mode for debugging
# chrome_options.add_argument("--headless=new")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# Initialize driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def speech_recognition(timeout=10):
    """Capture speech input with a timeout"""
    try:
        file_url = f"file://{os.path.abspath(html_path)}"
        driver.get(file_url)
        time.sleep(1)  # Wait for page to load
        
        print("Starting speech recognition...")
        driver.find_element(By.ID, "start").click()
        
        start_time = time.time()
        last_text = ""
        
        while time.time() - start_time < timeout:
            current_text = driver.find_element(By.ID, "output").text.strip()
            if current_text and current_text != last_text:
                print(f"Interim text: {current_text}")
                last_text = current_text
            
            if current_text and time.time() - start_time > 2:  # Minimum 2 seconds of speech
                driver.find_element(By.ID, "end").click()
                return current_text
            
            time.sleep(0.5)
        
        driver.find_element(By.ID, "end").click()
        return ""
    
    except Exception as e:
        print(f"Error in speech recognition: {e}")
        return ""

if __name__ == "__main__":
    try:
        while True:
            print("\nSpeak now (or press Ctrl+C to exit)...")
            text = speech_recognition()
            if text:
                print(f"\nYou said: {text}")
            else:
                print("No speech detected. Try again.")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        driver.quit()  
