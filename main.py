import subprocess
import os

def run_streamlit_app():
    """
    Finds and runs the Streamlit application `app.py` using subprocess.
    """
    app_path = "app.py"

    if not os.path.exists(app_path):
        print(f"Error: Could not find the application file at '{app_path}'")
        return

    print(f"Launching Streamlit application from '{app_path}'...")
    print("You can view the app in your browser.")
    print("Press Ctrl+C in this terminal to stop the application.")

    try:
        subprocess.run(["streamlit", "run", app_path], check=True)
    except FileNotFoundError:
        print("\nError: 'streamlit' command not found.")
        print("Please ensure you have installed the required packages by running:")
        print("pip install -r requirements.txt")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the Streamlit app: {e}")

if __name__ == "__main__":
    run_streamlit_app()
