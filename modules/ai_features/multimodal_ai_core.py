"""
Unified Multi-Modal AI System
Seamlessly combines Vision + Voice + Text inputs for intelligent understanding
"""

import os
import json
import base64
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from google import genai
from gui_automation import GUIAutomation

class MultiModalInput:
    """Represents a multi-modal input combining vision, voice, and text"""
    
    def __init__(self, text: Optional[str] = None, 
                 voice_transcript: Optional[str] = None,
                 screenshot_path: Optional[str] = None,
                 audio_context: Optional[Dict] = None):
        self.text = text
        self.voice_transcript = voice_transcript
        self.screenshot_path = screenshot_path
        self.audio_context = audio_context or {}
        self.timestamp = datetime.now().isoformat()
        self.modalities_used = self._identify_modalities()
    
    def _identify_modalities(self) -> List[str]:
        """Identify which modalities are present"""
        modalities = []
        if self.text:
            modalities.append("text")
        if self.voice_transcript:
            modalities.append("voice")
        if self.screenshot_path:
            modalities.append("vision")
        return modalities
    
    def get_primary_input(self) -> str:
        """Get the primary text input (voice or text)"""
        return self.voice_transcript or self.text or ""
    
    def has_vision(self) -> bool:
        """Check if vision input is available"""
        return bool(self.screenshot_path and os.path.exists(self.screenshot_path))
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            "text": self.text,
            "voice_transcript": self.voice_transcript,
            "screenshot_path": self.screenshot_path,
            "audio_context": self.audio_context,
            "timestamp": self.timestamp,
            "modalities": self.modalities_used
        }


class MultiModalAI:
    """
    Unified Multi-Modal AI System
    
    Combines vision, voice, and text inputs for coherent understanding
    Features:
    - Seamless integration of all modalities
    - Context-aware processing
    - Intelligent routing
    - Cross-modal understanding
    """
    
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except:
                pass
        
        self.gui = GUIAutomation()
        self.history_file = "multimodal_history.json"
        self.history = self._load_history()
        
        print("🧠 Multi-Modal AI System initialized")
    
    def _load_history(self) -> List[Dict]:
        """Load multi-modal interaction history"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_history(self):
        """Save interaction history"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history[-100:], f, indent=2)
        except Exception as e:
            print(f"Error saving multimodal history: {e}")
    
    def process(self, input_data: MultiModalInput) -> Dict:
        """
        Process multi-modal input and generate intelligent response
        
        Args:
            input_data: MultiModalInput object containing various modalities
        
        Returns:
            Dict with analysis, understanding, and recommended actions
        """
        print(f"\n🧠 Processing Multi-Modal Input (Modalities: {', '.join(input_data.modalities_used)})")
        
        if not self.client:
            return {
                "success": False,
                "message": "Gemini AI not configured. Set GEMINI_API_KEY.",
                "understanding": {},
                "actions": []
            }
        
        try:
            analysis = self._analyze_multimodal(input_data)
            
            self.history.append({
                "input": input_data.to_dict(),
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            })
            self._save_history()
            
            return {
                "success": True,
                "understanding": analysis,
                "primary_intent": analysis.get("intent", "unknown"),
                "recommended_actions": analysis.get("actions", []),
                "context": analysis.get("context", {}),
                "confidence": analysis.get("confidence", 0.0)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Multi-modal processing failed: {str(e)}",
                "understanding": {},
                "actions": []
            }
    
    def _analyze_multimodal(self, input_data: MultiModalInput) -> Dict:
        """
        Core multi-modal analysis using Gemini AI
        Combines all available modalities for comprehensive understanding
        """
        
        primary_text = input_data.get_primary_input()
        
        if input_data.has_vision():
            return self._analyze_with_vision(input_data, primary_text)
        else:
            return self._analyze_text_only(primary_text, input_data)
    
    def _analyze_with_vision(self, input_data: MultiModalInput, text: str) -> Dict:
        """Analyze with vision + text/voice"""
        
        if not input_data.screenshot_path:
            return self._analyze_text_only(text, input_data)
        
        with open(input_data.screenshot_path, 'rb') as f:
            image_data = f.read()
        
        modality_info = " + ".join(input_data.modalities_used).upper()
        
        prompt = f"""You are an advanced multi-modal AI assistant analyzing {modality_info} input.

**User Input ({"Voice" if input_data.voice_transcript else "Text"}):**
{text}

**Visual Context:**
<analyzing current screenshot>

**Task:**
Provide comprehensive multi-modal understanding combining visual and verbal information.

**Output Format (JSON):**
{{
    "intent": "primary user intent/goal",
    "context": {{
        "visual_state": "what's visible on screen",
        "current_activity": "what user is doing",
        "environment": "application/website context",
        "ui_elements": ["key interactive elements visible"]
    }},
    "understanding": {{
        "verbal_request": "what user asked for",
        "visual_relevance": "how screen relates to request",
        "combined_meaning": "complete understanding from both modalities",
        "implicit_needs": ["things user needs but didn't explicitly ask for"]
    }},
    "actions": [
        {{
            "type": "automation|information|analysis|navigation",
            "description": "what to do",
            "priority": "high|medium|low",
            "requires_vision": true|false
        }}
    ],
    "confidence": 0.95,
    "suggestions": ["proactive suggestions based on full context"]
}}

Provide detailed, actionable analysis combining ALL modalities."""
        
        try:
            if not self.client:
                return {"intent": "error", "context": {}, "understanding": {}, "actions": [], "confidence": 0.0}
            
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[
                    {
                        "parts": [
                            {"text": prompt},
                            {"inline_data": {"mime_type": "image/png", "data": base64.b64encode(image_data).decode()}}
                        ]
                    }
                ]
            )
            
            result_text = response.text.strip()
            
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            result_text = result_text.strip()
            
            try:
                return json.loads(result_text)
            except json.JSONDecodeError:
                return {
                    "intent": "unknown",
                    "context": {"error": "JSON parsing failed"},
                    "understanding": {"raw_response": result_text},
                    "actions": [],
                    "confidence": 0.5
                }
                
        except Exception as e:
            return {
                "intent": "error",
                "context": {"error": str(e)},
                "understanding": {},
                "actions": [],
                "confidence": 0.0
            }
    
    def _analyze_text_only(self, text: str, input_data: MultiModalInput) -> Dict:
        """Analyze text/voice only (no vision)"""
        
        modality = "Voice" if input_data.voice_transcript else "Text"
        audio_context_str = ""
        if input_data.audio_context:
            audio_context_str = f"\n**Audio Context:** {json.dumps(input_data.audio_context, indent=2)}"
        
        prompt = f"""You are an advanced AI assistant analyzing {modality} input.

**User Input:**
{text}{audio_context_str}

**Task:**
Understand user intent and provide actionable recommendations.

**Output Format (JSON):**
{{
    "intent": "primary user intent/goal",
    "context": {{
        "input_type": "{modality.lower()}",
        "complexity": "simple|moderate|complex",
        "domain": "system|productivity|communication|etc"
    }},
    "understanding": {{
        "explicit_request": "what user explicitly asked for",
        "implicit_needs": ["inferred needs"],
        "ambiguities": ["unclear aspects if any"]
    }},
    "actions": [
        {{
            "type": "automation|information|analysis",
            "description": "what to do",
            "priority": "high|medium|low"
        }}
    ],
    "confidence": 0.95,
    "suggestions": ["proactive recommendations"]
}}

Provide detailed analysis."""
        
        try:
            if not self.client:
                return {"intent": "error", "context": {}, "understanding": {}, "actions": [], "confidence": 0.0}
            
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            
            result_text = response.text.strip()
            
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            result_text = result_text.strip()
            
            try:
                return json.loads(result_text)
            except json.JSONDecodeError:
                return {
                    "intent": "unknown",
                    "context": {"error": "JSON parsing failed"},
                    "understanding": {"raw_response": result_text},
                    "actions": [],
                    "confidence": 0.5
                }
                
        except Exception as e:
            return {
                "intent": "error",
                "context": {"error": str(e)},
                "understanding": {},
                "actions": [],
                "confidence": 0.0
            }
    
    def get_context_aware_response(self, input_data: MultiModalInput, include_history: bool = True) -> str:
        """
        Generate context-aware natural language response combining all modalities
        
        Args:
            input_data: Multi-modal input
            include_history: Whether to include conversation history
        
        Returns:
            Natural language response
        """
        analysis = self.process(input_data)
        
        if not analysis.get("success"):
            return f"❌ {analysis.get('message', 'Processing failed')}"
        
        understanding = analysis.get("understanding", {})
        actions = analysis.get("recommended_actions", [])
        confidence = analysis.get("confidence", 0.0)
        
        modalities_str = ", ".join(input_data.modalities_used)
        
        response = f"🧠 Multi-Modal Analysis ({modalities_str})\n\n"
        
        if understanding.get("combined_meaning"):
            response += f"**Understanding:** {understanding['combined_meaning']}\n\n"
        elif understanding.get("explicit_request"):
            response += f"**Understanding:** {understanding['explicit_request']}\n\n"
        
        if understanding.get("context"):
            ctx = understanding["context"]
            if ctx.get("visual_state"):
                response += f"**Screen:** {ctx['visual_state']}\n"
            if ctx.get("current_activity"):
                response += f"**Activity:** {ctx['current_activity']}\n\n"
        
        if actions:
            response += "**Recommended Actions:**\n"
            for i, action in enumerate(actions[:3], 1):
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(action.get("priority", "medium"), "⚪")
                response += f"{i}. {priority_emoji} {action.get('description', 'Unknown action')}\n"
            response += "\n"
        
        if understanding.get("suggestions"):
            response += "**Suggestions:**\n"
            for suggestion in understanding["suggestions"][:3]:
                response += f"💡 {suggestion}\n"
        
        response += f"\n**Confidence:** {confidence*100:.0f}%"
        
        return response
    
    def capture_and_analyze(self, text_or_voice: str, is_voice: bool = False, 
                           take_screenshot: bool = True) -> Dict:
        """
        Convenience method: Capture current state and analyze
        
        Args:
            text_or_voice: Input text or voice transcript
            is_voice: Whether input is from voice
            take_screenshot: Whether to capture screenshot
        
        Returns:
            Analysis results
        """
        screenshot_path = None
        if take_screenshot:
            screenshot_path = self.gui.screenshot("multimodal")
        
        input_data = MultiModalInput(
            text=text_or_voice if not is_voice else None,
            voice_transcript=text_or_voice if is_voice else None,
            screenshot_path=screenshot_path
        )
        
        return self.process(input_data)
    
    def get_statistics(self) -> Dict:
        """Get usage statistics"""
        if not self.history:
            return {
                "total_interactions": 0,
                "modalities_used": {},
                "common_intents": []
            }
        
        modality_counts = {}
        intent_counts = {}
        
        for entry in self.history:
            modalities = entry.get("input", {}).get("modalities", [])
            for mod in modalities:
                modality_counts[mod] = modality_counts.get(mod, 0) + 1
            
            intent = entry.get("analysis", {}).get("intent", "unknown")
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        common_intents = sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_interactions": len(self.history),
            "modalities_used": modality_counts,
            "common_intents": [{"intent": intent, "count": count} for intent, count in common_intents],
            "vision_usage_rate": modality_counts.get("vision", 0) / len(self.history) * 100 if self.history else 0,
            "voice_usage_rate": modality_counts.get("voice", 0) / len(self.history) * 100 if self.history else 0
        }


def create_multimodal_ai():
    """Factory function to create MultiModalAI instance"""
    return MultiModalAI()


if __name__ == "__main__":
    print("🧠 Multi-Modal AI System - Test Mode\n")
    
    mmai = create_multimodal_ai()
    
    test_input = MultiModalInput(
        text="What's on my screen?",
        screenshot_path="screenshot.png" if os.path.exists("screenshot.png") else None
    )
    
    result = mmai.process(test_input)
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Intent: {result.get('primary_intent')}")
        print(f"Confidence: {result.get('confidence')}")
    
    stats = mmai.get_statistics()
    print(f"\nStatistics: {stats}")
