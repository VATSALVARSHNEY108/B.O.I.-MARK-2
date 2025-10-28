"""
Self-Operating Computer - Gemini Vision Edition
Inspired by OthersideAI's self-operating-computer but powered by Google Gemini Vision
Autonomously controls the computer by viewing the screen and executing actions
"""

import os
import json
import time
import pyautogui
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

class SelfOperatingComputer:
    """Autonomous computer controller using Gemini Vision"""
    
    def __init__(self, api_key: Optional[str] = None, verbose: bool = False):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")
        
        self.client = genai.Client(api_key=self.api_key)
        self.verbose = verbose
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        self.session_history = []
        self.max_iterations = 30
        self.current_iteration = 0
        
        screen_width, screen_height = pyautogui.size()
        self.screen_size = {"width": screen_width, "height": screen_height}
        
        self.system_prompt = """You are a self-operating computer agent powered by Gemini Vision.

Your task is to accomplish user objectives by viewing the screen and deciding on mouse/keyboard actions.

CAPABILITIES:
- View screenshots to understand current state
- Move mouse to specific coordinates
- Click (left, right, middle)
- Type text
- Press keyboard keys and shortcuts
- Scroll up/down
- Wait for page loads

OUTPUT FORMAT (JSON):
{
    "thought": "What I observe and what I'm planning to do",
    "action": "ACTION_TYPE",
    "parameters": {
        "x": 100,
        "y": 200,
        "text": "example",
        "key": "enter"
    },
    "progress": "Percentage complete (0-100)",
    "completed": false
}

AVAILABLE ACTIONS:
1. move_mouse: Move cursor to position
   - parameters: {"x": int, "y": int}

2. click: Click at current position or specific location
   - parameters: {"button": "left|right|middle", "x": int [optional], "y": int [optional], "clicks": 1|2}

3. type_text: Type text at current cursor
   - parameters: {"text": "string to type"}

4. press_key: Press a keyboard key
   - parameters: {"key": "enter|tab|escape|backspace|delete|space|up|down|left|right|..."}

5. hotkey: Press key combination
   - parameters: {"keys": ["ctrl", "c"]} or {"keys": ["cmd", "space"]}

6. scroll: Scroll the screen
   - parameters: {"direction": "up|down", "amount": 3}

7. wait: Wait for seconds
   - parameters: {"seconds": 2}

8. complete: Mark objective as complete
   - parameters: {"summary": "Brief summary of what was accomplished"}

IMPORTANT GUIDELINES:
- ALWAYS output valid JSON only, no other text
- Be precise with coordinates based on screen size: {screen_width}x{screen_height}
- For clicking elements, look carefully at their position in the screenshot
- Wait after clicks/navigation to let pages load
- If stuck, try alternative approaches
- Set "completed": true when objective is fully accomplished
- Use "progress" to track completion percentage
- Think step-by-step and explain your reasoning in "thought"

SAFETY:
- Never delete important files without explicit permission
- Avoid actions that could harm the system
- If unsure, ask for clarification

Screen Resolution: {screen_width}x{screen_height}
"""

    def _log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = "🔍" if level == "INFO" else "⚠️" if level == "WARN" else "❌"
        print(f"[{timestamp}] {prefix} {message}")
        
        if self.verbose:
            self.session_history.append({
                "timestamp": timestamp,
                "level": level,
                "message": message
            })

    def capture_screen(self) -> str:
        """Capture screenshot and return filepath"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"screen_{timestamp}.png"
        filepath = self.screenshot_dir / filename
        
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        
        self._log(f"Screenshot saved: {filename}")
        return str(filepath)

    def encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_screen_and_decide(self, objective: str, screenshot_path: str) -> Dict:
        """Use Gemini Vision to analyze screen and decide next action"""
        
        self._log(f"Analyzing screen... (Iteration {self.current_iteration + 1}/{self.max_iterations})")
        
        formatted_prompt = self.system_prompt.replace(
            "{screen_width}", str(self.screen_size["width"])
        ).replace(
            "{screen_height}", str(self.screen_size["height"])
        )
        
        iteration_context = ""
        if self.current_iteration > 0:
            recent_history = self.session_history[-3:] if len(self.session_history) >= 3 else self.session_history
            iteration_context = f"\n\nRecent actions:\n{json.dumps(recent_history, indent=2)}"
        
        user_message = f"""OBJECTIVE: {objective}

Current iteration: {self.current_iteration + 1}/{self.max_iterations}
{iteration_context}

Analyze the screenshot and decide the next action to accomplish the objective.
Remember: Output ONLY valid JSON, nothing else."""

        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_uri(
                                file_uri=screenshot_path,
                                mime_type="image/png"
                            ) if screenshot_path.startswith("http") else types.Part.from_bytes(
                                data=open(screenshot_path, "rb").read(),
                                mime_type="image/png"
                            ),
                            types.Part.from_text(text=user_message)
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction=formatted_prompt,
                    temperature=0.3,
                )
            )
            
            response_text = response.text.strip() if response and response.text else ""
            
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            decision = json.loads(response_text)
            
            required_fields = ["thought", "action", "parameters"]
            for field in required_fields:
                if field not in decision:
                    raise ValueError(f"Missing required field: {field}")
            
            return decision
            
        except json.JSONDecodeError as e:
            self._log(f"JSON parsing error: {e}", "ERROR")
            self._log(f"Raw response: {response_text[:200]}...", "ERROR")
            return {
                "thought": "Failed to parse response",
                "action": "wait",
                "parameters": {"seconds": 1},
                "completed": False
            }
        except Exception as e:
            self._log(f"Error analyzing screen: {str(e)}", "ERROR")
            return {
                "thought": f"Error: {str(e)}",
                "action": "wait",
                "parameters": {"seconds": 1},
                "completed": False
            }

    def execute_action(self, decision: Dict) -> bool:
        """Execute the decided action. Returns True if should continue."""
        
        action = decision.get("action", "").lower()
        params = decision.get("parameters", {})
        thought = decision.get("thought", "")
        progress = decision.get("progress", "Unknown")
        
        self._log(f"💭 Thought: {thought}")
        self._log(f"📊 Progress: {progress}%")
        self._log(f"⚡ Action: {action} | Params: {params}")
        
        self.session_history.append({
            "iteration": self.current_iteration,
            "thought": thought,
            "action": action,
            "parameters": params,
            "progress": progress
        })
        
        try:
            if action == "move_mouse":
                x, y = params.get("x", 0), params.get("y", 0)
                pyautogui.moveTo(x, y, duration=0.3)
                
            elif action == "click":
                button = params.get("button", "left")
                clicks = params.get("clicks", 1)
                x = params.get("x")
                y = params.get("y")
                
                if x is not None and y is not None:
                    pyautogui.click(x, y, clicks=clicks, button=button)
                else:
                    pyautogui.click(clicks=clicks, button=button)
                    
            elif action == "type_text":
                text = params.get("text", "")
                pyautogui.write(text, interval=0.05)
                
            elif action == "press_key":
                key = params.get("key", "")
                pyautogui.press(key)
                
            elif action == "hotkey":
                keys = params.get("keys", [])
                pyautogui.hotkey(*keys)
                
            elif action == "scroll":
                direction = params.get("direction", "down")
                amount = params.get("amount", 3)
                scroll_amount = -amount * 100 if direction == "down" else amount * 100
                pyautogui.scroll(scroll_amount)
                
            elif action == "wait":
                seconds = params.get("seconds", 1)
                time.sleep(seconds)
                
            elif action == "complete":
                summary = params.get("summary", "Objective completed")
                self._log(f"✅ COMPLETE: {summary}", "INFO")
                return False
                
            else:
                self._log(f"Unknown action: {action}", "WARN")
                time.sleep(0.5)
            
            time.sleep(0.5)
            return True
            
        except Exception as e:
            self._log(f"Error executing action {action}: {str(e)}", "ERROR")
            time.sleep(1)
            return True

    def operate(self, objective: str) -> Dict:
        """
        Main loop: Autonomously work towards the objective
        Returns summary of the session
        """
        self._log(f"🎯 Starting self-operating mode")
        self._log(f"📋 Objective: {objective}")
        self._log(f"🖥️  Screen: {self.screen_size['width']}x{self.screen_size['height']}")
        self._log("-" * 60)
        
        start_time = time.time()
        self.current_iteration = 0
        self.session_history = []
        
        try:
            while self.current_iteration < self.max_iterations:
                screenshot_path = self.capture_screen()
                
                decision = self.analyze_screen_and_decide(objective, screenshot_path)
                
                if decision.get("completed", False):
                    self._log("✅ Objective marked as completed by AI", "INFO")
                    break
                
                should_continue = self.execute_action(decision)
                
                if not should_continue:
                    break
                
                self.current_iteration += 1
                self._log("-" * 60)
                
            else:
                self._log(f"⚠️  Reached maximum iterations ({self.max_iterations})", "WARN")
        
        except KeyboardInterrupt:
            self._log("🛑 Stopped by user", "WARN")
        except Exception as e:
            self._log(f"❌ Fatal error: {str(e)}", "ERROR")
        
        duration = time.time() - start_time
        
        summary = {
            "objective": objective,
            "iterations": self.current_iteration,
            "duration_seconds": round(duration, 2),
            "completed": self.current_iteration < self.max_iterations,
            "history": self.session_history
        }
        
        self._log("=" * 60)
        self._log(f"📊 Session Summary:")
        self._log(f"   Total iterations: {summary['iterations']}")
        self._log(f"   Duration: {summary['duration_seconds']}s")
        self._log(f"   Status: {'✅ Completed' if summary['completed'] else '⏸️  Incomplete'}")
        
        return summary

    def operate_with_voice(self) -> Dict:
        """Start self-operating mode with voice input for the objective"""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            print("\n🎤 Voice Input Mode")
            print("Please state your objective when ready...")
            print("(Listening...)\n")
            
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
            print("🔄 Processing voice input...")
            objective = recognizer.recognize_google(audio)
            
            print(f"\n✅ Understood objective: '{objective}'")
            print("Starting in 3 seconds...\n")
            time.sleep(3)
            
            return self.operate(objective)
            
        except ImportError:
            print("❌ Voice support requires: pip install SpeechRecognition pyaudio")
            return {}
        except sr.WaitTimeoutError:
            print("❌ No speech detected. Please try again.")
            return {}
        except sr.UnknownValueError:
            print("❌ Could not understand audio. Please try again.")
            return {}
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return {}
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {}

def main():
    """CLI interface for self-operating computer"""
    print("=" * 70)
    print("🤖 SELF-OPERATING COMPUTER - Gemini Vision Edition")
    print("=" * 70)
    print("\nAutonomous computer control powered by Google Gemini Vision")
    print("Inspired by OthersideAI's self-operating-computer\n")
    
    try:
        computer = SelfOperatingComputer(verbose=True)
        
        print("Choose input mode:")
        print("1. Text input")
        print("2. Voice input")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            objective = input("\n📝 Enter your objective: ").strip()
            if objective:
                print()
                result = computer.operate(objective)
                
                save_log = input("\n💾 Save session log? (y/n): ").strip().lower()
                if save_log == 'y':
                    log_path = f"session_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(log_path, 'w') as f:
                        json.dump(result, f, indent=2)
                    print(f"✅ Log saved to: {log_path}")
            else:
                print("❌ No objective provided")
                
        elif choice == "2":
            print()
            result = computer.operate_with_voice()
            
            if result:
                save_log = input("\n💾 Save session log? (y/n): ").strip().lower()
                if save_log == 'y':
                    log_path = f"session_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(log_path, 'w') as f:
                        json.dump(result, f, indent=2)
                    print(f"✅ Log saved to: {log_path}")
        
        elif choice == "3":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
