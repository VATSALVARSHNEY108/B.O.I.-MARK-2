#!/usr/bin/env python3
"""
B.O.I Interconnection Dashboard
Visual display of feature network and workflow recommendations
"""

import tkinter as tk
from tkinter import ttk
import threading
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from modules.core.agi_interconnected import create_interconnected_agi
except:
    create_interconnected_agi = None


class InterconnectionDashboard:
    """Dashboard showing feature network interconnections"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("B.O.I - Feature Interconnection Dashboard")
        self.root.geometry("2200x1400")
        self.agi = None
        self._init_agi()
        self._build_ui()
        self._show_network_overview()
    
    def _init_agi(self):
        try:
            if create_interconnected_agi:
                self.agi = create_interconnected_agi()
        except:
            pass
    
    def _build_ui(self):
        main = tk.Frame(self.root, bg="#0f172a")
        main.pack(fill="both", expand=True)
        
        header = tk.Frame(main, bg="#0f172a", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🌐 B.O.I FEATURE INTERCONNECTION NETWORK", 
                font=("Consolas", 16, "bold"), bg="#0f172a", fg="#10b981").pack(side="left", padx=20, pady=15)
        
        # Main content
        content = tk.Frame(main, bg="#0f172a")
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left: Feature Search & Analysis
        left = tk.Frame(content, bg="#1e293b")
        left.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        tk.Label(left, text="🔍 FEATURE SEARCH", font=("Consolas", 11, "bold"),
                bg="#1e293b", fg="#0ea5e9").pack(anchor="w", padx=10, pady=(10, 5))
        
        search_frame = tk.Frame(left, bg="#1e293b")
        search_frame.pack(fill="x", padx=10, pady=5)
        
        self.search_entry = tk.Entry(search_frame, font=("Consolas", 10), bg="#0f172a", fg="#e2e8f0")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        tk.Button(search_frame, text="Analyze", command=self.analyze_feature,
                 bg="#10b981", fg="white", font=("Consolas", 9, "bold"), relief="flat").pack(side="left")
        
        tk.Label(left, text="📊 ANALYSIS RESULTS", font=("Consolas", 10, "bold"),
                bg="#1e293b", fg="#0ea5e9").pack(anchor="w", padx=10, pady=(10, 5))
        
        self.analysis_text = tk.Text(left, font=("Consolas", 8), bg="#0f172a", fg="#10b981",
                                    height=20, wrap="word")
        self.analysis_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Middle: Network Visualization
        mid = tk.Frame(content, bg="#1e293b")
        mid.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(mid, text="🌐 NETWORK OVERVIEW", font=("Consolas", 11, "bold"),
                bg="#1e293b", fg="#8b5cf6").pack(anchor="w", padx=10, pady=(10, 5))
        
        self.network_text = tk.Text(mid, font=("Consolas", 8), bg="#0f172a", fg="#8b5cf6",
                                   height=20, wrap="word")
        self.network_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Right: Workflow Recommendations
        right = tk.Frame(content, bg="#1e293b")
        right.pack(side="left", fill="both", expand=True, padx=(5, 0))
        
        tk.Label(right, text="🎯 WORKFLOW RECOMMENDATIONS", font=("Consolas", 11, "bold"),
                bg="#1e293b", fg="#f59e0b").pack(anchor="w", padx=10, pady=(10, 5))
        
        workflow_frame = tk.Frame(right, bg="#1e293b")
        workflow_frame.pack(fill="x", padx=10, pady=5)
        
        self.workflow_goal = tk.Entry(workflow_frame, font=("Consolas", 10), bg="#0f172a", fg="#e2e8f0")
        self.workflow_goal.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        tk.Button(workflow_frame, text="Suggest", command=self.suggest_workflow,
                 bg="#f59e0b", fg="white", font=("Consolas", 9, "bold"), relief="flat").pack(side="left")
        
        self.workflow_text = tk.Text(right, font=("Consolas", 8), bg="#0f172a", fg="#f59e0b",
                                    height=20, wrap="word")
        self.workflow_text.pack(fill="both", expand=True, padx=10, pady=5)
    
    def analyze_feature(self):
        """Analyze feature interconnections"""
        if not self.agi:
            return
        
        feature = self.search_entry.get().strip()
        if not feature:
            return
        
        result = self.agi.analyze_with_interconnections(feature)
        
        output = f"""✅ FEATURE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature: {feature}

📦 Primary Features Found: {len(result['primary_features'])}
"""
        for feat in result['primary_features']:
            output += f"  • {feat}\n"
        
        output += f"\n🔗 Interconnections:\n"
        for feat, network in result['interconnections'].items():
            output += f"\n  {feat}:\n"
            output += f"    Can feed to: {', '.join(network['can_chain_with'][:3])}\n"
            output += f"    Related tags: {', '.join(network['connections']['related_tags'][:3])}\n"
        
        output += f"\n💡 Suggested Workflows:\n"
        for i, wf in enumerate(result['suggested_workflows'][:3], 1):
            output += f"  {i}. {' → '.join(wf['workflow'])}\n"
        
        output += f"\n⚡ Optimizations:\n"
        for opt in result['optimization']:
            output += f"  • {opt}\n"
        
        self.analysis_text.delete("1.0", "end")
        self.analysis_text.insert("1.0", output)
    
    def suggest_workflow(self):
        """Get workflow recommendations"""
        if not self.agi:
            return
        
        goal = self.workflow_goal.get().strip()
        if not goal:
            return
        
        workflow = self.agi.create_smart_workflow(goal)
        
        output = f"""🎯 SMART WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Goal: {workflow['goal']}

📋 Recommended Workflow:
"""
        for i, step in enumerate(workflow['workflow'], 1):
            output += f"  {i}. {step}\n"
        
        output += f"\n📊 Statistics:
  • Steps: {workflow['steps']}
  • Interconnections: {workflow['interconnections']}
  • Expected: {workflow['expected_outcome']}

✅ Status: {'Recommended' if workflow['recommended'] else 'Custom'}
"""
        
        self.workflow_text.delete("1.0", "end")
        self.workflow_text.insert("1.0", output)
    
    def _show_network_overview(self):
        """Show network overview"""
        if not self.agi:
            return
        
        analysis = self.agi.interconnect.analyze_interconnections()
        registry = self.agi.interconnect.registry
        
        output = f"""🌐 NETWORK STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Total Features: {analysis['total_features']}
🏷️  Categories: {analysis['total_categories']}
🔗 Connections: {analysis['total_connections']}
📈 Interconnectivity: {analysis['interconnectivity']} connections/feature
🌳 Network Density: {analysis['network_density']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📂 CATEGORIES:
"""
        for cat, features in registry.categories.items():
            output += f"  • {cat.upper()}: {len(features)} features\n"
        
        output += f"\n🔗 TOP CONNECTIONS:\n"
        top_connections = sorted(
            [(feat, len(cons)) for feat, cons in registry.graph.items()],
            key=lambda x: x[1],
            reverse=True
        )
        for feat, con_count in top_connections[:10]:
            output += f"  • {feat}: {con_count} connections\n"
        
        self.network_text.delete("1.0", "end")
        self.network_text.insert("1.0", output)


def main():
    root = tk.Tk()
    app = InterconnectionDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
