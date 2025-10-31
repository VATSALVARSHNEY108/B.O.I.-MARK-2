"""
Advanced AI Integration Module
Provides integration methods for the Advanced AI tab in GUI
"""

import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
from multimodal_ai_core import create_multimodal_ai, MultiModalInput
from contextual_memory_enhanced import create_contextual_memory_enhanced
from correction_learning import create_correction_learning
from predictive_actions_engine import create_predictive_actions_engine


class AdvancedAIIntegration:
    """
    Integrates all advanced AI features into the GUI
    """
    
    def __init__(self, gui_instance):
        """
        Initialize advanced AI systems
        
        Args:
            gui_instance: Reference to the main GUI application
        """
        self.gui = gui_instance
        
        try:
            self.multimodal_ai = create_multimodal_ai()
            print("✅ Multi-Modal AI initialized")
        except Exception as e:
            self.multimodal_ai = None
            print(f"⚠️ Multi-Modal AI initialization failed: {e}")
        
        try:
            self.contextual_memory = create_contextual_memory_enhanced()
            print("✅ Contextual Memory initialized")
        except Exception as e:
            self.contextual_memory = None
            print(f"⚠️ Contextual Memory initialization failed: {e}")
        
        try:
            self.correction_learning = create_correction_learning()
            print("✅ Correction Learning initialized")
        except Exception as e:
            self.correction_learning = None
            print(f"⚠️ Correction Learning initialization failed: {e}")
        
        try:
            self.predictive_engine = create_predictive_actions_engine()
            print("✅ Predictive Engine initialized")
        except Exception as e:
            self.predictive_engine = None
            print(f"⚠️ Predictive Engine initialization failed: {e}")
    
    def append_output(self, text: str, tag: str = "info"):
        """Append text to advanced AI output console"""
        if not hasattr(self.gui, 'advanced_ai_output'):
            return
        
        self.gui.advanced_ai_output.config(state='normal')
        self.gui.advanced_ai_output.insert(tk.END, text, tag)
        self.gui.advanced_ai_output.see(tk.END)
        self.gui.advanced_ai_output.config(state='disabled')
    
    def analyze_screen(self):
        """Analyze current screen with multi-modal AI"""
        if not self.multimodal_ai:
            self.append_output("❌ Multi-Modal AI not available\n", "error")
            return
        
        self.append_output("\n🧠 Analyzing current screen...\n", "info")
        
        try:
            result = self.multimodal_ai.capture_and_analyze(
                text_or_voice="Analyze what's on my screen",
                is_voice=False,
                take_screenshot=True
            )
            
            if result.get("success"):
                response = self.multimodal_ai.get_context_aware_response(
                    MultiModalInput(
                        text="Analyze what's on my screen",
                        screenshot_path=result.get("screenshot_path")
                    )
                )
                self.append_output(f"{response}\n\n", "success")
            else:
                self.append_output(f"❌ Analysis failed: {result.get('message')}\n", "error")
        
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")
    
    def voice_vision_analysis(self):
        """Combined voice and vision analysis"""
        self.append_output("\n🎤👁️ Voice + Vision feature coming soon!\n", "info")
        self.append_output("This will combine voice commands with screen analysis.\n", "info")
    
    def mm_statistics(self):
        """Show multi-modal AI statistics"""
        if not self.multimodal_ai:
            self.append_output("❌ Multi-Modal AI not available\n", "error")
            return
        
        self.append_output("\n📊 Multi-Modal AI Statistics\n", "info")
        
        try:
            stats = self.multimodal_ai.get_statistics()
            self.append_output(f"Total Interactions: {stats['total_interactions']}\n", "success")
            self.append_output(f"Modalities Used:\n", "info")
            for mod, count in stats['modalities_used'].items():
                self.append_output(f"  - {mod}: {count}\n", "success")
            self.append_output(f"Vision Usage: {stats['vision_usage_rate']:.1f}%\n", "success")
            self.append_output(f"Voice Usage: {stats['voice_usage_rate']:.1f}%\n\n", "success")
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")
    
    def remember_something(self):
        """Remember information"""
        if not self.contextual_memory:
            self.append_output("❌ Contextual Memory not available\n", "error")
            return
        
        content = simpledialog.askstring("Remember Something", "What should I remember?")
        if not content:
            return
        
        category = simpledialog.askstring("Category", "Category (general/preference/fact/pattern):", initialvalue="general")
        
        try:
            mem_id = self.contextual_memory.remember(content, category or "general", importance=0.7)
            self.append_output(f"\n📝 Remembered: {content}\n", "success")
            self.append_output(f"Category: {category}, ID: {mem_id[:8]}\n\n", "info")
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")
    
    def recall_memories(self):
        """Recall stored memories"""
        if not self.contextual_memory:
            self.append_output("❌ Contextual Memory not available\n", "error")
            return
        
        query = simpledialog.askstring("Recall Memories", "Search for (leave empty for recent memories):")
        
        try:
            memories = self.contextual_memory.recall(query=query, limit=10)
            
            self.append_output(f"\n🔍 Found {len(memories)} memories\n\n", "info")
            
            for i, mem in enumerate(memories, 1):
                self.append_output(f"{i}. {mem.content}\n", "success")
                self.append_output(f"   Category: {mem.category}, Importance: {mem.importance:.2f}\n", "info")
                self.append_output(f"   Accessed: {mem.access_count} times\n\n", "info")
        
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")
    
    def update_preferences(self):
        """Update user preferences"""
        if not self.contextual_memory:
            self.append_output("❌ Contextual Memory not available\n", "error")
            return
        
        pref_key = simpledialog.askstring("Preference Key", "Preference key (e.g., communication_style):")
        if not pref_key:
            return
        
        pref_value = simpledialog.askstring("Preference Value", f"Value for {pref_key}:")
        if not pref_value:
            return
        
        try:
            self.contextual_memory.update_preference(pref_key, pref_value)
            self.append_output(f"\n⚙️ Updated preference: {pref_key} = {pref_value}\n\n", "success")
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")
    
    def memory_statistics(self):
        """Show memory statistics"""
        if not self.contextual_memory:
            self.append_output("❌ Contextual Memory not available\n", "error")
            return
        
        try:
            stats = self.contextual_memory.get_statistics()
            
            self.append_output("\n📊 Memory System Statistics\n\n", "info")
            self.append_output(f"Total Memories: {stats['total_memories']}\n", "success")
            self.append_output(f"Avg Importance: {stats['avg_importance']:.2f}\n", "success")
            self.append_output(f"Session Interactions: {stats['session_interactions']}\n", "success")
            self.append_output(f"Session Duration: {stats['session_duration_minutes']:.1f} minutes\n", "success")
            
            if stats['memories_by_category']:
                self.append_output(f"\nMemories by Category:\n", "info")
                for cat, count in stats['memories_by_category'].items():
                    self.append_output(f"  - {cat}: {count}\n", "success")
            
            self.append_output("\n", "info")
        
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")
    
    def record_correction(self):
        """Record a correction"""
        if not self.correction_learning:
            self.append_output("❌ Correction Learning not available\n", "error")
            return
        
        original = simpledialog.askstring("Original Response", "What was the original (incorrect) response?")
        if not original:
            return
        
        corrected = simpledialog.askstring("Corrected Response", "What should it have been?")
        if not corrected:
            return
        
        corr_type = simpledialog.askstring("Correction Type", "Type (command/response/action/general):", initialvalue="general")
        
        try:
            corr_id = self.correction_learning.record_correction(
                original_response=original,
                corrected_response=corrected,
                correction_type=corr_type or "general"
            )
            
            self.append_output(f"\n✏️ Correction Recorded\n", "success")
            self.append_output(f"ID: {corr_id}\n", "info")
            self.append_output(f"Type: {corr_type}\n\n", "info")
        
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")
    
    def learning_report(self):
        """Show learning report"""
        if not self.correction_learning:
            self.append_output("❌ Correction Learning not available\n", "error")
            return
        
        try:
            report = self.correction_learning.get_learning_report()
            
            self.append_output("\n📈 Learning Report\n\n", "info")
            
            if report.get('status'):
                self.append_output(f"{report['status']}\n\n", "warning")
                return
            
            self.append_output(f"Total Corrections: {report['total_corrections_all_time']}\n", "success")
            self.append_output(f"Recent (30 days): {report['recent_corrections_30_days']}\n", "success")
            self.append_output(f"Learning Velocity: {report['learning_velocity']}/day\n", "success")
            self.append_output(f"Improvement Rate: {report['improvement_rate']}%\n", "success")
            self.append_output(f"Patterns Learned: {report['patterns_learned']}\n", "success")
            
            if report.get('most_corrected_areas'):
                self.append_output(f"\nMost Corrected Areas:\n", "warning")
                for area in report['most_corrected_areas'][:5]:
                    self.append_output(f"  - {area['area']}: {area['count']} corrections\n", "warning")
            
            self.append_output("\n", "info")
        
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")
    
    def apply_learning(self):
        """Apply learned corrections"""
        if not self.correction_learning:
            self.append_output("❌ Correction Learning not available\n", "error")
            return
        
        proposed = simpledialog.askstring("Proposed Response", "Enter a proposed response to improve:")
        if not proposed:
            return
        
        try:
            result = self.correction_learning.apply_learning(proposed)
            
            self.append_output("\n🎯 Learning Applied\n\n", "info")
            self.append_output(f"Corrections Applied: {result['corrections_applied']}\n", "success")
            
            if result['corrections_applied'] > 0:
                self.append_output(f"Improved Response:\n{result['improved_response']}\n\n", "success")
                self.append_output(f"Notes: {result['learning_notes']}\n\n", "info")
            else:
                self.append_output("No applicable corrections found.\n\n", "warning")
        
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")
    
    def get_predictions(self):
        """Get predicted next actions"""
        if not self.predictive_engine:
            self.append_output("❌ Predictive Engine not available\n", "error")
            return
        
        try:
            predictions = self.predictive_engine.predict_next_actions(max_predictions=5)
            
            self.append_output("\n🔮 Predicted Next Actions\n\n", "prediction")
            
            if not predictions:
                self.append_output("No predictions available yet. Use the system more to build patterns!\n\n", "info")
                return
            
            for i, pred in enumerate(predictions, 1):
                confidence_emoji = "🔴" if pred.confidence > 0.7 else "🟡" if pred.confidence > 0.4 else "🟢"
                self.append_output(f"{i}. {confidence_emoji} {pred.action}\n", "prediction")
                self.append_output(f"   Confidence: {pred.confidence*100:.0f}%\n", "info")
                self.append_output(f"   Reason: {pred.reasoning}\n\n", "info")
        
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")
    
    def proactive_suggestions(self):
        """Get proactive suggestions"""
        if not self.predictive_engine:
            self.append_output("❌ Predictive Engine not available\n", "error")
            return
        
        try:
            suggestions = self.predictive_engine.get_proactive_suggestions()
            
            self.append_output("\n💡 Proactive Suggestions\n\n", "prediction")
            
            if not suggestions:
                self.append_output("No suggestions at this time.\n\n", "info")
                return
            
            for i, sug in enumerate(suggestions, 1):
                self.append_output(f"{i}. {sug['emoji']} {sug['action']}\n", "prediction")
                self.append_output(f"   {sug['reason']} ({sug['confidence']}% confidence)\n\n", "info")
        
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")
    
    def prediction_accuracy(self):
        """Show prediction accuracy metrics"""
        if not self.predictive_engine:
            self.append_output("❌ Predictive Engine not available\n", "error")
            return
        
        try:
            metrics = self.predictive_engine.get_accuracy_metrics()
            stats = self.predictive_engine.get_statistics()
            
            self.append_output("\n📊 Prediction Accuracy Metrics\n\n", "info")
            
            self.append_output(f"Total Predictions: {metrics['total_predictions']}\n", "success")
            self.append_output(f"Correct Predictions: {metrics['correct_predictions']}\n", "success")
            self.append_output(f"Accuracy: {metrics['accuracy']}%\n\n", "success")
            
            self.append_output(f"Actions Recorded: {stats['total_actions_recorded']}\n", "info")
            self.append_output(f"Unique Actions: {stats['unique_actions']}\n", "info")
            self.append_output(f"Sequences Learned: {stats['sequences_learned']}\n", "info")
            self.append_output(f"Time Patterns: {stats['time_patterns']}\n", "info")
            self.append_output(f"Context Patterns: {stats['context_patterns']}\n\n", "info")
        
        except Exception as e:
            self.append_output(f"❌ Error: {str(e)}\n", "error")
    
    def clear_output(self):
        """Clear the advanced AI output console"""
        if hasattr(self.gui, 'advanced_ai_output'):
            self.gui.advanced_ai_output.config(state='normal')
            self.gui.advanced_ai_output.delete(1.0, tk.END)
            self.gui.advanced_ai_output.config(state='disabled')


def create_advanced_ai_integration(gui_instance):
    """Factory function"""
    return AdvancedAIIntegration(gui_instance)
