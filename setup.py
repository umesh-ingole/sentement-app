#!/usr/bin/env python3
"""
Automated Setup Script for Sentiment Analysis API
Handles environment setup, dependency installation, and model training
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class SetupManager:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.venv_dir = self.project_dir / "venv"
        self.python = sys.executable
        self.is_windows = platform.system() == "Windows"
        self.colors = {
            'header': '\033[95m',
            'blue': '\033[94m',
            'cyan': '\033[96m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'end': '\033[0m',
            'bold': '\033[1m',
        }
    
    def print_header(self, text):
        """Print section header"""
        print(f"\n{self.colors['header']}{self.colors['bold']}{'='*70}{self.colors['end']}")
        print(f"{self.colors['header']}{self.colors['bold']}{text}{self.colors['end']}")
        print(f"{self.colors['header']}{self.colors['bold']}{'='*70}{self.colors['end']}\n")
    
    def print_success(self, text):
        """Print success message"""
        print(f"{self.colors['green']}✓ {text}{self.colors['end']}")
    
    def print_error(self, text):
        """Print error message"""
        print(f"{self.colors['red']}✗ {text}{self.colors['end']}")
    
    def print_info(self, text):
        """Print info message"""
        print(f"{self.colors['cyan']}ℹ {text}{self.colors['end']}")
    
    def run_command(self, command, description):
        """Run shell command"""
        print(f"{self.colors['yellow']}→ {description}...{self.colors['end']}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=False,
                check=True
            )
            self.print_success(description)
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"{description} failed")
            return False
    
    def check_python_version(self):
        """Check Python version"""
        self.print_header("Checking Python Version")
        version = sys.version_info
        print(f"Python: {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3 or (version.major == 3 and version.minor < 9):
            self.print_error("Python 3.9 or higher required")
            return False
        
        self.print_success(f"Python {version.major}.{version.minor} OK")
        return True
    
    def create_venv(self):
        """Create virtual environment"""
        self.print_header("Creating Virtual Environment")
        
        if self.venv_dir.exists():
            self.print_info("Virtual environment already exists")
            return True
        
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", str(self.venv_dir)],
                check=True
            )
            self.print_success("Virtual environment created")
            return True
        except Exception as e:
            self.print_error(f"Failed to create venv: {e}")
            return False
    
    def get_activation_command(self):
        """Get venv activation command"""
        if self.is_windows:
            return f"{self.venv_dir}\\Scripts\\activate.bat && "
        else:
            return f"source {self.venv_dir}/bin/activate && "
    
    def install_dependencies(self):
        """Install Python dependencies"""
        self.print_header("Installing Dependencies")
        
        activation = self.get_activation_command()
        requirements_file = self.project_dir / "requirements_production.txt"
        
        if not requirements_file.exists():
            self.print_error(f"Requirements file not found: {requirements_file}")
            return False
        
        command = f"{activation}pip install -r {requirements_file}"
        
        return self.run_command(
            command,
            "Installing dependencies"
        )
    
    def train_model(self):
        """Train BERT model"""
        self.print_header("Training BERT Model")
        
        model_dir = self.project_dir / "bert_model"
        if model_dir.exists():
            self.print_info("Model already exists at bert_model/")
            response = input("Retrain? (y/N): ").strip().lower()
            if response != 'y':
                self.print_success("Skipping training")
                return True
        
        activation = self.get_activation_command()
        command = f"{activation}python train_production.py"
        
        return self.run_command(command, "Training BERT model")
    
    def test_api(self):
        """Test API"""
        self.print_header("Testing API")
        
        self.print_info("Starting API in background...")
        activation = self.get_activation_command()
        
        # This would require more complex subprocess management
        self.print_info("Run 'python app_production.py' to start the API")
        self.print_info("Run 'python test_api.py' in another terminal to test")
        return True
    
    def print_next_steps(self):
        """Print next steps"""
        self.print_header("✅ Setup Complete!")
        
        print("Next steps:\n")
        print(f"{self.colors['bold']}1. Start the API:{self.colors['end']}")
        activation = self.get_activation_command()
        print(f"   {activation}python app_production.py\n")
        
        print(f"{self.colors['bold']}2. Test in another terminal:{self.colors['end']}")
        print(f"   {activation}python test_api.py\n")
        
        print(f"{self.colors['bold']}3. Try a prediction:{self.colors['end']}")
        print("   curl -X POST http://localhost:5000/predict \\")
        print("     -H 'Content-Type: application/json' \\")
        print("     -d '{\"text\": \"I love this!\"}'\n")
        
        print(f"{self.colors['bold']}4. Documentation:{self.colors['end']}")
        print("   - QUICKSTART.md: Get started fast")
        print("   - README.md: Full documentation")
        print("   - SETUP_GUIDE.md: Detailed setup\n")
    
    def run(self):
        """Run complete setup"""
        print(f"\n{self.colors['cyan']}{self.colors['bold']}")
        print("╔" + "="*68 + "╗")
        print("║" + " "*10 + "SENTIMENT ANALYSIS API - SETUP WIZARD" + " "*21 + "║")
        print("╚" + "="*68 + "╝")
        print(f"{self.colors['end']}\n")
        
        steps = [
            ("Python Version", self.check_python_version),
            ("Virtual Environment", self.create_venv),
            ("Dependencies", self.install_dependencies),
            ("Model Training", self.train_model),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                self.print_error(f"Setup failed at: {step_name}")
                return 1
        
        self.print_next_steps()
        return 0


def main():
    """Main entry point"""
    try:
        setup = SetupManager()
        return setup.run()
    except KeyboardInterrupt:
        print(f"\n\n{'*'*70}")
        print("Setup interrupted by user")
        print(f"{'*'*70}\n")
        return 1
    except Exception as e:
        print(f"\n\n{'*'*70}")
        print(f"Setup error: {e}")
        print(f"{'*'*70}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
