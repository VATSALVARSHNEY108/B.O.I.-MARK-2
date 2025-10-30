"""
Enhanced Contextual Memory System
Remembers across sessions with deep contextual understanding
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict

class MemoryEntry:
    """Represents a single memory entry"""
    
    def __init__(self, content: str, category: str, importance: float = 0.5,
                 metadata: Optional[Dict] = None):
        self.id = datetime.now().isoformat() + "_" + str(hash(content))[:8]
        self.content = content
        self.category = category
        self.importance = importance
        self.created_at = datetime.now().isoformat()
        self.last_accessed = datetime.now().isoformat()
        self.access_count = 0
        self.metadata = metadata or {}
    
    def access(self):
        """Mark memory as accessed"""
        self.last_accessed = datetime.now().isoformat()
        self.access_count += 1
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "content": self.content,
            "category": self.category,
            "importance": self.importance,
            "created_at": self.created_at,
            "last_accessed": self.last_accessed,
            "access_count": self.access_count,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create from dictionary"""
        entry = cls(
            content=data["content"],
            category=data["category"],
            importance=data.get("importance", 0.5),
            metadata=data.get("metadata", {})
        )
        entry.id = data["id"]
        entry.created_at = data["created_at"]
        entry.last_accessed = data.get("last_accessed", entry.created_at)
        entry.access_count = data.get("access_count", 0)
        return entry


class ContextualMemoryEnhanced:
    """
    Enhanced Contextual Memory System
    
    Features:
    - Long-term cross-session memory
    - User preferences and personality
    - Contextual understanding
    - Importance-based retention
    - Semantic organization
    - Automatic consolidation
    """
    
    def __init__(self):
        self.memory_file = "enhanced_memory.json"
        self.preferences_file = "user_preferences_enhanced.json"
        self.session_file = "current_session.json"
        
        self.long_term_memory: List[MemoryEntry] = []
        self.user_preferences: Dict = {}
        self.current_session: Dict = {}
        
        self._load_all()
        
        self.current_session = {
            "session_id": datetime.now().isoformat(),
            "start_time": datetime.now().isoformat(),
            "interactions": [],
            "context_stack": []
        }
        
        print("🧠 Enhanced Contextual Memory initialized")
    
    def _load_all(self):
        """Load all memory data"""
        self._load_long_term_memory()
        self._load_preferences()
    
    def _load_long_term_memory(self):
        """Load long-term memory"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.long_term_memory = [MemoryEntry.from_dict(entry) for entry in data]
            except:
                self.long_term_memory = []
        else:
            self.long_term_memory = []
    
    def _load_preferences(self):
        """Load user preferences"""
        if os.path.exists(self.preferences_file):
            try:
                with open(self.preferences_file, 'r') as f:
                    self.user_preferences = json.load(f)
            except:
                self.user_preferences = self._default_preferences()
        else:
            self.user_preferences = self._default_preferences()
    
    def _default_preferences(self) -> Dict:
        """Get default user preferences"""
        return {
            "name": "User",
            "communication_style": "professional",
            "detail_level": "moderate",
            "preferred_times": {
                "work_start": "09:00",
                "work_end": "17:00",
                "preferred_break_times": ["11:00", "15:00"]
            },
            "favorite_apps": [],
            "common_tasks": [],
            "learning_preferences": {
                "receive_suggestions": True,
                "proactive_automation": True,
                "learn_from_corrections": True
            },
            "personality_traits": {
                "formality_level": 0.7,
                "verbosity": 0.5,
                "proactivity": 0.8
            }
        }
    
    def _save_all(self):
        """Save all memory data"""
        try:
            with open(self.memory_file, 'w') as f:
                memory_data = [entry.to_dict() for entry in self.long_term_memory]
                json.dump(memory_data, f, indent=2)
        except Exception as e:
            print(f"Error saving long-term memory: {e}")
        
        try:
            with open(self.preferences_file, 'w') as f:
                json.dump(self.user_preferences, f, indent=2)
        except Exception as e:
            print(f"Error saving preferences: {e}")
        
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.current_session, f, indent=2)
        except Exception as e:
            print(f"Error saving session: {e}")
    
    def remember(self, content: str, category: str = "general", 
                 importance: float = 0.5, metadata: Optional[Dict] = None):
        """
        Store information in long-term memory
        
        Args:
            content: What to remember
            category: Memory category (preference, fact, pattern, interaction, etc.)
            importance: How important (0.0-1.0)
            metadata: Additional contextual information
        """
        entry = MemoryEntry(content, category, importance, metadata)
        self.long_term_memory.append(entry)
        
        self.consolidate_memory()
        
        self._save_all()
        
        return entry.id
    
    def recall(self, query: str = None, category: str = None, 
               limit: int = 10, min_importance: float = 0.0) -> List[MemoryEntry]:
        """
        Recall memories matching criteria
        
        Args:
            query: Search query (searches content)
            category: Filter by category
            limit: Maximum number of results
            min_importance: Minimum importance threshold
        
        Returns:
            List of matching memory entries
        """
        results = []
        
        for entry in self.long_term_memory:
            if category and entry.category != category:
                continue
            
            if entry.importance < min_importance:
                continue
            
            if query:
                query_lower = query.lower()
                if query_lower not in entry.content.lower() and \
                   query_lower not in json.dumps(entry.metadata).lower():
                    continue
            
            entry.access()
            results.append(entry)
        
        results.sort(key=lambda x: (x.importance, x.access_count), reverse=True)
        
        self._save_all()
        
        return results[:limit]
    
    def update_preference(self, key: str, value: Any):
        """Update user preference"""
        keys = key.split(".")
        current = self.user_preferences
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
        
        self.remember(
            f"User preference updated: {key} = {value}",
            category="preference",
            importance=0.8,
            metadata={"preference_key": key, "value": value}
        )
        
        self._save_all()
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference"""
        keys = key.split(".")
        current = self.user_preferences
        
        try:
            for k in keys:
                current = current[k]
            return current
        except (KeyError, TypeError):
            return default
    
    def record_interaction(self, user_input: str, system_response: str, 
                          context: Optional[Dict] = None):
        """Record interaction in current session"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "system": system_response,
            "context": context or {}
        }
        
        self.current_session["interactions"].append(interaction)
        
        if len(self.current_session["interactions"]) > 50:
            self.current_session["interactions"] = self.current_session["interactions"][-50:]
        
        self._save_all()
    
    def get_session_context(self, last_n: int = 5) -> str:
        """Get recent session context as string"""
        interactions = self.current_session.get("interactions", [])[-last_n:]
        
        if not interactions:
            return "No previous interactions in this session."
        
        context = "Recent conversation:\n"
        for i, interaction in enumerate(interactions, 1):
            context += f"{i}. User: {interaction['user'][:100]}\n"
            context += f"   System: {interaction['system'][:100]}\n"
        
        return context
    
    def consolidate_memory(self):
        """
        Consolidate memories - remove low importance, merge duplicates
        Keeps memory manageable
        """
        if len(self.long_term_memory) < 500:
            return
        
        self.long_term_memory.sort(key=lambda x: (x.importance, x.access_count), reverse=True)
        
        self.long_term_memory = self.long_term_memory[:300]
        
        for entry in self.long_term_memory:
            days_old = (datetime.now() - datetime.fromisoformat(entry.created_at)).days
            if days_old > 30 and entry.access_count == 0:
                entry.importance *= 0.5
    
    def get_relevant_context(self, current_input: str, max_items: int = 5) -> Dict:
        """
        Get relevant contextual information for current input
        
        Args:
            current_input: Current user input
            max_items: Maximum contextual items to return
        
        Returns:
            Dict with relevant memories, preferences, and patterns
        """
        relevant_memories = self.recall(query=current_input, limit=max_items, min_importance=0.3)
        
        context = {
            "user_name": self.user_preferences.get("name", "User"),
            "communication_style": self.user_preferences.get("communication_style", "professional"),
            "relevant_memories": [
                {
                    "content": mem.content,
                    "category": mem.category,
                    "importance": mem.importance
                } for mem in relevant_memories
            ],
            "session_history": self.get_session_context(last_n=3),
            "current_context": self.current_session.get("context_stack", [])[-1] if self.current_session.get("context_stack") else None
        }
        
        return context
    
    def learn_pattern(self, pattern_description: str, evidence: List[str]):
        """Learn a behavioral pattern"""
        pattern_content = f"Pattern: {pattern_description}\nEvidence: {', '.join(evidence[:5])}"
        
        self.remember(
            pattern_content,
            category="pattern",
            importance=0.7,
            metadata={
                "pattern": pattern_description,
                "evidence_count": len(evidence),
                "learned_at": datetime.now().isoformat()
            }
        )
    
    def get_patterns(self) -> List[Dict]:
        """Get all learned patterns"""
        pattern_memories = self.recall(category="pattern", limit=20)
        
        return [
            {
                "pattern": mem.metadata.get("pattern", mem.content),
                "importance": mem.importance,
                "learned_at": mem.metadata.get("learned_at"),
                "access_count": mem.access_count
            } for mem in pattern_memories
        ]
    
    def get_statistics(self) -> Dict:
        """Get memory system statistics"""
        categories = defaultdict(int)
        for mem in self.long_term_memory:
            categories[mem.category] += 1
        
        total_interactions = len(self.current_session.get("interactions", []))
        
        session_duration = datetime.now() - datetime.fromisoformat(self.current_session.get("start_time", datetime.now().isoformat()))
        
        return {
            "total_memories": len(self.long_term_memory),
            "memories_by_category": dict(categories),
            "avg_importance": sum(m.importance for m in self.long_term_memory) / len(self.long_term_memory) if self.long_term_memory else 0,
            "most_accessed": max(self.long_term_memory, key=lambda x: x.access_count).content if self.long_term_memory else None,
            "session_interactions": total_interactions,
            "session_duration_minutes": session_duration.total_seconds() / 60,
            "preferences_configured": len(self.user_preferences)
        }
    
    def export_memory(self, filepath: str = "memory_export.json"):
        """Export all memory data"""
        export_data = {
            "long_term_memory": [m.to_dict() for m in self.long_term_memory],
            "user_preferences": self.user_preferences,
            "export_timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filepath
    
    def import_memory(self, filepath: str):
        """Import memory data"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if "long_term_memory" in data:
            imported_memories = [MemoryEntry.from_dict(m) for m in data["long_term_memory"]]
            self.long_term_memory.extend(imported_memories)
        
        if "user_preferences" in data:
            self.user_preferences.update(data["user_preferences"])
        
        self._save_all()


def create_contextual_memory_enhanced():
    """Factory function"""
    return ContextualMemoryEnhanced()


if __name__ == "__main__":
    print("🧠 Enhanced Contextual Memory - Test Mode\n")
    
    memory = create_contextual_memory_enhanced()
    
    memory.remember("User prefers dark mode", "preference", importance=0.8)
    memory.remember("User works best in the morning", "pattern", importance=0.7)
    
    memory.update_preference("communication_style", "friendly")
    
    results = memory.recall(query="dark", limit=5)
    print(f"Found {len(results)} memories about 'dark'")
    
    stats = memory.get_statistics()
    print(f"\nStatistics: {json.dumps(stats, indent=2)}")
