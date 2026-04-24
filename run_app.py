"""
Simple wrapper to run the Flask app
This is a pre-trained sentiment analysis app that doesn't require model training
"""
import subprocess
import sys

print("Starting Sentiment Analysis Flask App...")
print("=" * 70)

try:
    subprocess.run([sys.executable, "app.py"], cwd=".", check=True)
except KeyboardInterrupt:
    print("\nApp stopped by user")
except Exception as e:
    print(f"Error: {e}")
