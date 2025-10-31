"""
Virtual Language Model - Learn from Screen and Control Desktop
A self-learning AI system that observes the screen, builds knowledge, and controls the desktop
"""

import os
import json
import time
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
from google import genai
from google.genai import types
from gui_automation import GUIAutomation


class VirtualLanguageModel:
    """
    Virtual Language Model that learns from screen observations
    and controls the desktop based on learned knowledge
    """
    
    def __init__(self, gui: GUIAutomation):
        self.gui = gui
        self.api_key = os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            print("⚠️  Warning: GEMINI_API_KEY not found")
            self.client = None
            self.model = None
        else:
            try:
                self.client = genai.Client(api_key=self.api_key)
                self.model = 'gemini-2.0-flash'
            except Exception as e:
                print(f"⚠️  Warning: Failed to initialize Gemini client: {e}")
                self.client = None
                self.model = None
        
        # Knowledge base - the model's "memory"
        self.visual_memory = []  # Screenshots and their interpretations
        self.ui_patterns = {}  # Learned UI patterns (buttons, menus, etc.)
        self.application_knowledge = {}  # What the model knows about apps
        self.action_history = []  # History of actions taken
        self.learned_workflows = []  # Learned multi-step workflows
        
        # Learning parameters
        self.observation_count = 0
        self.successful_actions = 0
        self.failed_actions = 0
        
        # Memory file
        self.memory_file = "vlm_memory.json"
        self.load_memory()
    
    def observe_screen(self, context: str = "general observation") -> Dict[str, Any]:
        """
        Observe the current screen state and learn from it
        
        Args:
            context: Context for this observation (e.g., "after clicking button")
        
        Returns:
            Dictionary with observation results
        """
        print(f"\n👁️  Observing screen: {context}")
        
        if self.gui.demo_mode:
            return {
                "success": False,
                "message": "Demo mode - screen capture not available",
                "demo": True
            }
        
        try:
            # Capture current screen
            screenshot_path = f"observation_{self.observation_count}.png"
            screenshot = self.gui.capture_screen()
            
            if screenshot:
                screenshot.save(screenshot_path)
                print(f"📸 Screenshot saved: {screenshot_path}")
            else:
                return {"success": False, "message": "Could not capture screen"}
            
            # Analyze with AI vision
            analysis = self._analyze_screen_with_ai(screenshot_path, context)
            
            # Store in visual memory
            memory_entry = {
                "id": self.observation_count,
                "timestamp": datetime.now().isoformat(),
                "context": context,
                "screenshot": screenshot_path,
                "analysis": analysis,
                "learned_elements": analysis.get("ui_elements", []),
                "applications": analysis.get("visible_applications", [])
            }
            
            self.visual_memory.append(memory_entry)
            self.observation_count += 1
            
            # Update knowledge base
            self._update_knowledge_base(memory_entry)
            
            # Save memory
            self.save_memory()
            
            print(f"✅ Observation {self.observation_count} recorded and learned")
            return {
                "success": True,
                "observation_id": self.observation_count - 1,
                "analysis": analysis,
                "memory_entry": memory_entry
            }
            
        except Exception as e:
            print(f"❌ Error during observation: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _analyze_screen_with_ai(self, screenshot_path: str, context: str) -> Dict[str, Any]:
        """Analyze screenshot using Gemini AI vision"""
        
        if not self.client:
            return {
                "description": "AI not available",
                "ui_elements": [],
                "visible_applications": [],
                "opportunities": []
            }
        
        try:
            # Read the image
            with open(screenshot_path, 'rb') as f:
                image_data = f.read()
            
            prompt = f"""
You are a Virtual Language Model that learns from screen observations.

Context: {context}

Analyze this screenshot and provide:

1. **Description**: What do you see on the screen?
2. **UI Elements**: List all visible UI elements (buttons, text fields, menus, icons, etc.)
3. **Applications**: What applications are visible or running?
4. **Layout**: Describe the layout and organization
5. **Interaction Opportunities**: What actions could be performed here?
6. **Patterns**: Any recurring UI patterns or design elements?
7. **Text Content**: Any important text visible?

Provide a detailed analysis in JSON format:
{{
    "description": "Brief description of what's on screen",
    "ui_elements": [
        {{"type": "button", "label": "...", "location": "...", "purpose": "..."}},
        ...
    ],
    "visible_applications": ["app1", "app2", ...],
    "layout": "description of layout",
    "interaction_opportunities": [
        {{"action": "...", "element": "...", "expected_result": "..."}},
        ...
    ],
    "patterns": ["pattern1", "pattern2", ...],
    "text_content": ["important text 1", "important text 2", ...],
    "learning_insights": "What can be learned from this screen"
}}
"""
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part(text=prompt),
                            types.Part(
                                inline_data=types.Blob(
                                    mime_type="image/png",
                                    data=image_data
                                )
                            )
                        ]
                    )
                ]
            )
            
            # Parse JSON from response
            response_text = response.text.strip()
            
            # Extract JSON if wrapped in code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            analysis = json.loads(response_text)
            return analysis
            
        except Exception as e:
            print(f"⚠️  AI analysis failed: {str(e)}")
            return {
                "description": "Analysis failed",
                "ui_elements": [],
                "visible_applications": [],
                "error": str(e)
            }
    
    def _update_knowledge_base(self, memory_entry: Dict[str, Any]):
        """Update the knowledge base with new observations"""
        
        analysis = memory_entry.get("analysis", {})
        
        # Learn UI patterns
        for element in analysis.get("ui_elements", []):
            element_type = element.get("type", "unknown")
            if element_type not in self.ui_patterns:
                self.ui_patterns[element_type] = []
            
            self.ui_patterns[element_type].append({
                "label": element.get("label", ""),
                "location": element.get("location", ""),
                "purpose": element.get("purpose", ""),
                "seen_at": memory_entry["timestamp"]
            })
        
        # Learn about applications
        for app in analysis.get("visible_applications", []):
            if app not in self.application_knowledge:
                self.application_knowledge[app] = {
                    "first_seen": memory_entry["timestamp"],
                    "observations": 0,
                    "ui_elements": [],
                    "capabilities": []
                }
            
            self.application_knowledge[app]["observations"] += 1
            self.application_knowledge[app]["last_seen"] = memory_entry["timestamp"]
    
    def learn_workflow(self, workflow_name: str, steps: List[Dict[str, Any]]):
        """
        Learn a multi-step workflow
        
        Args:
            workflow_name: Name of the workflow
            steps: List of steps in the workflow
        """
        workflow = {
            "name": workflow_name,
            "steps": steps,
            "learned_at": datetime.now().isoformat(),
            "execution_count": 0,
            "success_rate": 0.0
        }
        
        self.learned_workflows.append(workflow)
        self.save_memory()
        
        print(f"✅ Learned new workflow: {workflow_name} ({len(steps)} steps)")
    
    def decide_action(self, goal: str) -> Dict[str, Any]:
        """
        Decide what action to take based on learned knowledge and goal
        
        Args:
            goal: What the user wants to achieve
        
        Returns:
            Dictionary with recommended action
        """
        print(f"\n🤔 Deciding action for goal: {goal}")
        
        if not self.client:
            return {
                "action": "observe",
                "reason": "AI not available, need to observe first"
            }
        
        try:
            # Create prompt with all learned knowledge
            knowledge_summary = self._summarize_knowledge()
            
            prompt = f"""
You are a Virtual Language Model that learns from screen observations and controls the desktop.

**Goal**: {goal}

**Your Learned Knowledge**:
{knowledge_summary}

**Recent Observations**: {len(self.visual_memory)} screen states observed
**Known UI Patterns**: {list(self.ui_patterns.keys())}
**Known Applications**: {list(self.application_knowledge.keys())}
**Learned Workflows**: {len(self.learned_workflows)}

Based on your learned knowledge, decide the best action to achieve the goal.

Provide your decision in JSON format:
{{
    "action": "type of action (click, type, launch, observe, etc.)",
    "target": "what to interact with",
    "parameters": {{"param1": "value1", ...}},
    "reasoning": "why this action based on learned knowledge",
    "confidence": 0.0-1.0,
    "alternative_actions": ["action1", "action2", ...],
    "requires_observation": true/false
}}
"""
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            response_text = response.text.strip()
            
            # Extract JSON
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            decision = json.loads(response_text)
            
            print(f"✅ Decision made: {decision['action']}")
            print(f"   Confidence: {decision.get('confidence', 0):.2f}")
            print(f"   Reasoning: {decision.get('reasoning', 'N/A')}")
            
            return decision
            
        except Exception as e:
            print(f"❌ Error making decision: {str(e)}")
            return {
                "action": "observe",
                "reason": f"Error: {str(e)}",
                "confidence": 0.0
            }
    
    def execute_learned_action(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an action based on learned decision
        
        Args:
            decision: Decision dictionary from decide_action()
        
        Returns:
            Execution result
        """
        action_type = decision.get("action", "").lower()
        target = decision.get("target", "")
        params = decision.get("parameters", {})
        
        print(f"\n🎯 Executing learned action: {action_type}")
        
        # Observe before action
        before_obs = self.observe_screen(f"before {action_type}")
        
        result = {"success": False, "action": action_type}
        
        try:
            if action_type == "click":
                # Use learned knowledge to find and click element
                result = self._execute_click(target, params)
            
            elif action_type == "type":
                text = params.get("text", "")
                result = self._execute_type(text)
            
            elif action_type == "launch":
                app = params.get("application", target)
                result = self._execute_launch(app)
            
            elif action_type == "observe":
                result = self.observe_screen("requested observation")
            
            elif action_type == "search":
                query = params.get("query", target)
                result = self._execute_search(query)
            
            else:
                result = {
                    "success": False,
                    "message": f"Unknown action type: {action_type}"
                }
            
            # Observe after action
            after_obs = self.observe_screen(f"after {action_type}")
            
            # Learn from the outcome
            self._learn_from_outcome(decision, before_obs, after_obs, result)
            
            # Record in action history
            self.action_history.append({
                "timestamp": datetime.now().isoformat(),
                "decision": decision,
                "result": result,
                "before": before_obs.get("observation_id"),
                "after": after_obs.get("observation_id")
            })
            
            if result.get("success"):
                self.successful_actions += 1
            else:
                self.failed_actions += 1
            
            self.save_memory()
            
            return result
            
        except Exception as e:
            print(f"❌ Error executing action: {str(e)}")
            self.failed_actions += 1
            return {"success": False, "error": str(e)}
    
    def _execute_click(self, target: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute click action"""
        # Use GUI automation to click
        x = params.get("x", 100)
        y = params.get("y", 100)
        
        if self.gui.demo_mode:
            return {"success": True, "demo": True, "message": f"Would click {target} at ({x}, {y})"}
        
        self.gui.click(x, y)
        time.sleep(0.5)
        return {"success": True, "message": f"Clicked {target}"}
    
    def _execute_type(self, text: str) -> Dict[str, Any]:
        """Execute typing action"""
        if self.gui.demo_mode:
            return {"success": True, "demo": True, "message": f"Would type: {text}"}
        
        self.gui.type_text(text)
        return {"success": True, "message": f"Typed: {text}"}
    
    def _execute_launch(self, app: str) -> Dict[str, Any]:
        """Execute application launch"""
        if self.gui.demo_mode:
            return {"success": True, "demo": True, "message": f"Would launch: {app}"}
        
        self.gui.launch_application(app)
        time.sleep(2)
        return {"success": True, "message": f"Launched: {app}"}
    
    def _execute_search(self, query: str) -> Dict[str, Any]:
        """Execute search action"""
        if self.gui.demo_mode:
            return {"success": True, "demo": True, "message": f"Would search for: {query}"}
        
        self.gui.web_search(query)
        return {"success": True, "message": f"Searched for: {query}"}
    
    def _learn_from_outcome(self, decision: Dict, before: Dict, after: Dict, result: Dict):
        """Learn from the outcome of an action"""
        # This is where the model improves over time
        # Compare before and after states to understand what changed
        
        if result.get("success"):
            print("📚 Learning from successful action...")
            # Store successful pattern for future use
        else:
            print("📚 Learning from failed action...")
            # Store what didn't work to avoid in future
    
    def _summarize_knowledge(self) -> str:
        """Create a summary of all learned knowledge"""
        summary = []
        
        summary.append(f"Total Observations: {len(self.visual_memory)}")
        summary.append(f"UI Pattern Types Known: {len(self.ui_patterns)}")
        summary.append(f"Applications Known: {len(self.application_knowledge)}")
        
        if self.application_knowledge:
            summary.append("\nKnown Applications:")
            for app, data in list(self.application_knowledge.items())[:5]:
                summary.append(f"  - {app}: {data['observations']} observations")
        
        if self.learned_workflows:
            summary.append(f"\nLearned Workflows: {len(self.learned_workflows)}")
            for wf in self.learned_workflows[:3]:
                summary.append(f"  - {wf['name']}: {len(wf['steps'])} steps")
        
        summary.append(f"\nSuccess Rate: {self.successful_actions}/{self.successful_actions + self.failed_actions}")
        
        return "\n".join(summary)
    
    def autonomous_learning_session(self, duration_minutes: int = 5):
        """
        Run an autonomous learning session where the model explores and learns
        
        Args:
            duration_minutes: How long to run the session
        """
        print(f"\n🧠 Starting autonomous learning session ({duration_minutes} minutes)")
        print("=" * 60)
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        learning_goals = [
            "Learn about current screen layout",
            "Identify all interactive elements",
            "Understand application structure",
            "Discover navigation patterns"
        ]
        
        for goal in learning_goals:
            if time.time() >= end_time:
                break
            
            print(f"\n🎯 Learning Goal: {goal}")
            
            # Observe
            obs = self.observe_screen(goal)
            
            if obs.get("success"):
                # Make a decision based on what was learned
                decision = self.decide_action(f"explore and learn about: {goal}")
                
                # Execute if confidence is high enough
                if decision.get("confidence", 0) > 0.5:
                    self.execute_learned_action(decision)
            
            time.sleep(2)
        
        print(f"\n✅ Learning session complete!")
        print(f"   Observations made: {self.observation_count}")
        print(f"   UI patterns learned: {len(self.ui_patterns)}")
        print(f"   Applications discovered: {len(self.application_knowledge)}")
    
    def query_knowledge(self, question: str) -> str:
        """
        Query the learned knowledge base
        
        Args:
            question: Question about learned knowledge
        
        Returns:
            Answer based on learned knowledge
        """
        if not self.client:
            return "AI not available for queries"
        
        knowledge = self._summarize_knowledge()
        
        prompt = f"""
You are a Virtual Language Model with the following learned knowledge:

{knowledge}

Question: {question}

Answer the question based only on your learned knowledge.
If you don't have the information, say so.
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"Error querying knowledge: {str(e)}"
    
    def save_memory(self):
        """Save the model's memory to file"""
        memory_data = {
            "observation_count": self.observation_count,
            "successful_actions": self.successful_actions,
            "failed_actions": self.failed_actions,
            "ui_patterns": self.ui_patterns,
            "application_knowledge": self.application_knowledge,
            "learned_workflows": self.learned_workflows,
            "action_history": self.action_history[-100:],  # Keep last 100
            "visual_memory": [
                {k: v for k, v in m.items() if k != "analysis"}  # Exclude large analysis
                for m in self.visual_memory[-50:]  # Keep last 50
            ]
        }
        
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save memory: {str(e)}")
    
    def load_memory(self):
        """Load the model's memory from file"""
        if not os.path.exists(self.memory_file):
            return
        
        try:
            with open(self.memory_file, 'r') as f:
                memory_data = json.load(f)
            
            self.observation_count = memory_data.get("observation_count", 0)
            self.successful_actions = memory_data.get("successful_actions", 0)
            self.failed_actions = memory_data.get("failed_actions", 0)
            self.ui_patterns = memory_data.get("ui_patterns", {})
            self.application_knowledge = memory_data.get("application_knowledge", {})
            self.learned_workflows = memory_data.get("learned_workflows", [])
            self.action_history = memory_data.get("action_history", [])
            self.visual_memory = memory_data.get("visual_memory", [])
            
            print(f"📚 Loaded memory: {self.observation_count} observations, {len(self.ui_patterns)} patterns")
        except Exception as e:
            print(f"⚠️  Could not load memory: {str(e)}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the model's learning"""
        total_actions = self.successful_actions + self.failed_actions
        success_rate = (self.successful_actions / total_actions * 100) if total_actions > 0 else 0
        
        return {
            "observations": self.observation_count,
            "ui_patterns": len(self.ui_patterns),
            "known_applications": len(self.application_knowledge),
            "learned_workflows": len(self.learned_workflows),
            "total_actions": total_actions,
            "successful_actions": self.successful_actions,
            "failed_actions": self.failed_actions,
            "success_rate": success_rate,
            "knowledge_summary": self._summarize_knowledge()
        }


def main():
    """Test the Virtual Language Model"""
    print("=" * 60)
    print("🧠 VIRTUAL LANGUAGE MODEL - Learn from Screen & Control")
    print("=" * 60)
    
    gui = GUIAutomation()
    vlm = VirtualLanguageModel(gui)
    
    if gui.demo_mode:
        print("\n⚠️  DEMO MODE: Running with simulated actions")
        print("Download and run locally for full functionality\n")
    
    while True:
        print("\n" + "=" * 60)
        print("Options:")
        print("1. Observe current screen")
        print("2. Decide action for a goal")
        print("3. Execute learned action")
        print("4. Query learned knowledge")
        print("5. View statistics")
        print("6. Start autonomous learning session")
        print("7. Save memory")
        print("8. Exit")
        print("=" * 60)
        
        choice = input("\nEnter choice (1-8): ").strip()
        
        if choice == "1":
            context = input("Context (or press Enter): ").strip() or "manual observation"
            result = vlm.observe_screen(context)
            
            if result.get("success"):
                analysis = result.get("analysis", {})
                print(f"\n📊 Analysis:")
                print(f"Description: {analysis.get('description', 'N/A')}")
                print(f"UI Elements: {len(analysis.get('ui_elements', []))}")
                print(f"Applications: {analysis.get('visible_applications', [])}")
        
        elif choice == "2":
            goal = input("Enter your goal: ").strip()
            if goal:
                decision = vlm.decide_action(goal)
                print(f"\n💡 Recommended Action:")
                print(json.dumps(decision, indent=2))
        
        elif choice == "3":
            goal = input("Enter goal to execute: ").strip()
            if goal:
                decision = vlm.decide_action(goal)
                print(f"\n🎯 Executing: {decision.get('action')}")
                result = vlm.execute_learned_action(decision)
                print(f"Result: {result}")
        
        elif choice == "4":
            question = input("Ask about learned knowledge: ").strip()
            if question:
                answer = vlm.query_knowledge(question)
                print(f"\n💬 Answer: {answer}")
        
        elif choice == "5":
            stats = vlm.get_stats()
            print(f"\n📊 Statistics:")
            print(json.dumps(stats, indent=2))
        
        elif choice == "6":
            duration = input("Duration in minutes (default 5): ").strip()
            duration = int(duration) if duration.isdigit() else 5
            vlm.autonomous_learning_session(duration)
        
        elif choice == "7":
            vlm.save_memory()
            print("✅ Memory saved!")
        
        elif choice == "8":
            vlm.save_memory()
            print("\n👋 Goodbye!")
            break


if __name__ == "__main__":
    main()
