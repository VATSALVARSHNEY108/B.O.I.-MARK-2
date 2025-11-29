#!/usr/bin/env python3
"""
B.O.I Advanced AGI - Enterprise Intelligence GUI
Full predictive analytics, autonomous planning, goal reasoning
"""

import tkinter as tk
from tkinter import ttk
import threading
import sys
import os
from datetime import datetime
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from modules.core.agi_engine_advanced import create_advanced_agi_engine
except:
    create_advanced_agi_engine = None

try:
    from modules.core.command_executor import CommandExecutor
except:
    CommandExecutor = None


class AdvancedAGIGUI:
    """B.O.I Advanced AGI with predictive + planning + goal reasoning"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("B.O.I - Advanced AGI Enterprise Intelligence")
        self.root.geometry("2000x1200")
        self.root.minsize(1600, 900)
        
        self.agi = None
        self.executor = None
        self.processing = False
        self.command_history = []
        
        self._init_modules()
        self._build_ui()
        self._show_welcome()
    
    def _init_modules(self):
        try:
            if create_advanced_agi_engine:
                self.agi = create_advanced_agi_engine()
        except:
            pass
        try:
            if CommandExecutor:
                self.executor = CommandExecutor()
        except:
            pass
    
    def _build_ui(self):
        main = tk.Frame(self.root, bg="#0f172a")
        main.pack(fill="both", expand=True)
        
        # Header
        header = tk.Frame(main, bg="#0f172a", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🧠 B.O.I ADVANCED AGI", font=("Consolas", 16, "bold"),
                bg="#0f172a", fg="#10b981").pack(side="left", padx=20, pady=15)
        tk.Label(header, text="Predictive • Planning • Autonomous • Goal-Oriented",
                font=("Consolas", 10), bg="#0f172a", fg="#64748b").pack(side="left", padx=20)
        
        # Main content with 3 panels
        content = tk.Frame(main, bg="#0f172a")
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left panel - Input & Chat
        left = tk.Frame(content, bg="#1e293b")
        left.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        tk.Label(left, text="💬 COMMAND", font=("Consolas", 10, "bold"),
                bg="#1e293b", fg="#0ea5e9").pack(anchor="w", padx=10, pady=(10, 5))
        
        self.input_entry = tk.Text(left, font=("Consolas", 11), bg="#0f172a", fg="#e2e8f0",
                                  height=3, wrap="word", insertbackground="#10b981")
        self.input_entry.pack(fill="x", padx=10, pady=5)
        
        send_btn = tk.Button(left, text="▶ EXECUTE WITH AGI ANALYSIS", command=self.send_command,
                            bg="#10b981", fg="white", font=("Consolas", 9, "bold"),
                            relief="flat", padx=20, pady=8)
        send_btn.pack(pady=5)
        
        tk.Label(left, text="📊 OUTPUT", font=("Consolas", 10, "bold"),
                bg="#1e293b", fg="#0ea5e9").pack(anchor="w", padx=10, pady=(10, 5))
        
        self.output_text = tk.Text(left, font=("Consolas", 9), bg="#0f172a", fg="#10b981",
                                  height=15, wrap="word")
        self.output_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Middle panel - Predictions
        mid = tk.Frame(content, bg="#1e293b")
        mid.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(mid, text="🔮 PREDICTIONS", font=("Consolas", 10, "bold"),
                bg="#1e293b", fg="#8b5cf6").pack(anchor="w", padx=10, pady=(10, 5))
        
        self.pred_text = tk.Text(mid, font=("Consolas", 8), bg="#0f172a", fg="#8b5cf6",
                                height=20, wrap="word")
        self.pred_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Right panel - Planning & Goals
        right = tk.Frame(content, bg="#1e293b")
        right.pack(side="left", fill="both", expand=True, padx=(5, 0))
        
        tk.Label(right, text="🎯 GOAL PLANNING", font=("Consolas", 10, "bold"),
                bg="#1e293b", fg="#f59e0b").pack(anchor="w", padx=10, pady=(10, 5))
        
        self.plan_text = tk.Text(right, font=("Consolas", 8), bg="#0f172a", fg="#f59e0b",
                                height=20, wrap="word")
        self.plan_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Footer
        footer = tk.Frame(main, bg="#1e293b", height=40)
        footer.pack(fill="x")
        footer.pack_propagate(False)
        
        tk.Label(footer, text="✓ AGI Ready | 🧠 Advanced Reasoning Enabled | 🔮 Predictions Active",
                font=("Consolas", 9), bg="#1e293b", fg="#64748b").pack(padx=20, pady=10)
    
    def send_command(self):
        cmd = self.input_entry.get("1.0", "end-1c").strip()
        if not cmd or self.processing:
            return
        
        self.input_entry.delete("1.0", "end")
        self.command_history.append(cmd)
        self.processing = True
        
        def execute():
            try:
                if not self.agi:
                    return
                
                # Get predictions
                predictions = self.agi.process_with_predictions(cmd, self.command_history)
                pred_text = f"""🔮 PREDICTION ANALYSIS:
━━━━━━━━━━━━━━━━━━━━━━━━
Command: {cmd}

📈 Next Predicted Command:
  → {predictions['predicted_next']}
  📊 Confidence: {predictions['prediction_confidence']:.0%}

🎯 User Intent:
  • Intent: {predictions['user_intent']['intent']}
  • Category: {predictions['user_intent']['category']}
  • Urgency: {predictions['user_intent']['urgency']}

🔮 Predicted Outcome:
  • Result: {predictions['predicted_outcome']['likely_result']}
  • Confidence: {predictions['predicted_outcome']['confidence']:.0%}
  • Time: {predictions['predicted_outcome']['estimated_time']}
  • Risk: {predictions['predicted_outcome']['risk_level']}
"""
                
                # Get planning
                planning = self.agi.autonomous_plan_execution(cmd)
                plan_text = f"""🎯 AUTONOMOUS PLAN:
━━━━━━━━━━━━━━━━━━━━━━━━
Goal: {planning['goal']}

📋 Execution Plan:
  • Steps: {len(planning['execution_steps'])}
  • Duration: {planning['plan']['estimated_duration']}
  • Success Rate: {planning['plan']['success_rate']:.0%}
  
🔄 Execution Steps:
"""
                for i, step in enumerate(planning['execution_steps'], 1):
                    plan_text += f"  {i}. {step}\n"
                
                plan_text += f"\n⚙️ Configuration:
  • Monitoring: {planning['monitoring']}
  • Safety: {planning['safety_checks']}
  • Autonomous: {planning['autonomous_status']}"
                
                # Get goal analysis
                goal_analysis = self.agi.goal_oriented_execution(cmd)
                output_text = f"""✅ GOAL-ORIENTED EXECUTION:
━━━━━━━━━━━━━━━━━━━━━━━━
Goal: {goal_analysis['goal']}

📊 Analysis:
  • Type: {goal_analysis['analysis']['type']}
  • Complexity: {goal_analysis['analysis']['complexity']}
  • Success Probability: {goal_analysis['success_probability']:.0%}

🔧 Prerequisites:
"""
                for prereq in goal_analysis['analysis']['prerequisites']:
                    output_text += f"  ✓ {prereq}\n"
                
                output_text += f"\n🎯 Success Criteria:\n"
                for criterion in goal_analysis['analysis']['success_criteria']:
                    output_text += f"  ✓ {criterion}\n"
                
                output_text += f"\n⚠️ Risk Assessment:\n"
                for risk in goal_analysis['analysis']['failure_modes']:
                    output_text += f"  ⚠️ {risk}\n"
                
                # Update display
                self.root.after(0, lambda: self._update_displays(output_text, pred_text, plan_text))
            
            finally:
                self.processing = False
        
        threading.Thread(target=execute, daemon=True).start()
    
    def _update_displays(self, output, preds, plans):
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", output)
        self.pred_text.delete("1.0", "end")
        self.pred_text.insert("1.0", preds)
        self.plan_text.delete("1.0", "end")
        self.plan_text.insert("1.0", plans)
    
    def _show_welcome(self):
        welcome = """🚀 B.O.I ADVANCED AGI SYSTEM ONLINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Predictive Analytics: ENABLED
   → Predict next commands
   → Intent analysis
   → Outcome forecasting

✅ Autonomous Planning: ENABLED
   → Goal decomposition
   → Multi-step execution
   → Intelligent sequencing

✅ Goal Reasoning: ENABLED
   → Analyze objectives
   → Risk assessment
   → Optimization discovery

✅ Context Chaining: ENABLED
   → Multi-turn memory
   → Relationship mapping
   → Pattern detection

Type your command and press "EXECUTE WITH AGI ANALYSIS"
"""
        self.output_text.insert("1.0", welcome)


def main():
    root = tk.Tk()
    app = AdvancedAGIGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
