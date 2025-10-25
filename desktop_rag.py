"""
🧠 Smart Desktop RAG (Retrieval Augmented Generation)
AI-powered system to interact with all desktop data intelligently
"""

import os
import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import mimetypes
from gemini_controller import get_client
from google.genai import types


class DesktopRAG:
    """
    Smart RAG system for desktop data:
    - Index all desktop files and folders
    - Extract text content from various file types
    - Semantic search with AI
    - Answer questions about desktop content
    - Summarize documents and folders
    - Find relevant files intelligently
    """
    
    def __init__(self):
        """Initialize Desktop RAG system"""
        self.index_file = "desktop_index.json"
        self.index = self._load_index()
        self.supported_text_extensions = {
            '.txt', '.md', '.py', '.js', '.html', '.css', '.json', 
            '.csv', '.xml', '.yaml', '.yml', '.log', '.ini', '.cfg',
            '.java', '.cpp', '.c', '.h', '.rs', '.go', '.rb', '.php',
            '.sh', '.bat', '.ps1', '.sql', '.r', '.jsx', '.tsx', '.vue'
        }
        print("🧠 Smart Desktop RAG initialized")
        print(f"   📊 Indexed files: {len(self.index)}")
    
    def _load_index(self) -> Dict:
        """Load existing index from disk"""
        try:
            if os.path.exists(self.index_file):
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load index: {e}")
        return {}
    
    def _save_index(self):
        """Save index to disk"""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2, ensure_ascii=False)
            print(f"✅ Index saved: {len(self.index)} files indexed")
        except Exception as e:
            print(f"❌ Failed to save index: {e}")
    
    def _extract_text_content(self, file_path: str) -> Optional[str]:
        """Extract text content from various file types"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            # Text-based files
            if file_ext in self.supported_text_extensions:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(50000)  # Limit to 50KB per file
                    return content
            
            # Binary files - just get metadata
            return None
            
        except Exception as e:
            return None
    
    def index_directory(self, directory: str, max_files: int = 1000, 
                       recursive: bool = True) -> Dict:
        """
        Index all files in a directory
        
        Args:
            directory: Path to directory to index
            max_files: Maximum number of files to index
            recursive: Include subdirectories
        """
        print(f"\n🔍 Indexing directory: {directory}")
        print(f"   📁 Recursive: {recursive}")
        print(f"   📊 Max files: {max_files}")
        
        indexed_count = 0
        skipped_count = 0
        start_time = time.time()
        
        try:
            path = Path(directory).expanduser()
            
            if not path.exists():
                return {
                    "success": False,
                    "error": f"Directory not found: {directory}"
                }
            
            # Get file iterator
            if recursive:
                file_iter = path.rglob("*")
            else:
                file_iter = path.glob("*")
            
            for file_path in file_iter:
                if indexed_count >= max_files:
                    print(f"⚠️  Reached max files limit ({max_files})")
                    break
                
                if not file_path.is_file():
                    continue
                
                # Skip hidden files and system files
                if file_path.name.startswith('.') or file_path.name.startswith('~'):
                    skipped_count += 1
                    continue
                
                # Skip very large files (>10MB)
                try:
                    if file_path.stat().st_size > 10 * 1024 * 1024:
                        skipped_count += 1
                        continue
                except:
                    continue
                
                # Extract content and metadata
                file_key = str(file_path.absolute())
                content = self._extract_text_content(str(file_path))
                
                file_stats = file_path.stat()
                
                self.index[file_key] = {
                    "path": str(file_path),
                    "name": file_path.name,
                    "extension": file_path.suffix.lower(),
                    "size": file_stats.st_size,
                    "modified": datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                    "created": datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                    "content": content[:5000] if content else None,  # First 5KB
                    "has_content": content is not None,
                    "indexed_at": datetime.now().isoformat()
                }
                
                indexed_count += 1
                
                if indexed_count % 100 == 0:
                    print(f"   📊 Indexed {indexed_count} files...")
            
            # Save index
            self._save_index()
            
            elapsed = time.time() - start_time
            
            return {
                "success": True,
                "indexed_files": indexed_count,
                "skipped_files": skipped_count,
                "total_in_index": len(self.index),
                "time_taken": f"{elapsed:.2f}s",
                "directory": directory
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "indexed_files": indexed_count
            }
    
    def quick_index_common_folders(self) -> Dict:
        """Index common user folders (Desktop, Documents, Downloads)"""
        print("\n🏠 Quick indexing common folders...")
        
        home = Path.home()
        common_folders = [
            home / "Desktop",
            home / "Documents", 
            home / "Downloads",
            home / "Pictures",
            home / "Videos"
        ]
        
        results = []
        total_indexed = 0
        
        for folder in common_folders:
            if folder.exists():
                print(f"\n📂 Indexing {folder.name}...")
                result = self.index_directory(str(folder), max_files=500, recursive=True)
                results.append({
                    "folder": folder.name,
                    "result": result
                })
                if result.get("success"):
                    total_indexed += result.get("indexed_files", 0)
        
        return {
            "success": True,
            "total_files_indexed": total_indexed,
            "folders_indexed": len([r for r in results if r["result"].get("success")]),
            "details": results
        }
    
    def search_files(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search files by name, content, or metadata
        
        Args:
            query: Search query
            max_results: Maximum number of results
        """
        print(f"\n🔍 Searching for: '{query}'")
        
        query_lower = query.lower()
        matches = []
        
        for file_key, file_data in self.index.items():
            score = 0
            
            # Name match
            if query_lower in file_data["name"].lower():
                score += 10
            
            # Extension match
            if query_lower in file_data["extension"]:
                score += 5
            
            # Content match
            if file_data.get("content") and query_lower in file_data["content"].lower():
                score += 20
                
                # Count occurrences
                occurrences = file_data["content"].lower().count(query_lower)
                score += min(occurrences * 2, 20)
            
            if score > 0:
                matches.append({
                    **file_data,
                    "relevance_score": score
                })
        
        # Sort by relevance
        matches.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return matches[:max_results]
    
    def ask_about_files(self, question: str) -> Dict:
        """
        Ask AI a question about your desktop files
        
        Args:
            question: Natural language question about files
        """
        print(f"\n💬 Question: {question}")
        
        # Get relevant files based on keywords
        keywords = question.lower().split()
        relevant_files = []
        
        for file_key, file_data in self.index.items():
            relevance = 0
            
            for keyword in keywords:
                if len(keyword) < 3:
                    continue
                
                if keyword in file_data["name"].lower():
                    relevance += 2
                if file_data.get("content") and keyword in file_data["content"].lower():
                    relevance += 3
            
            if relevance > 0:
                relevant_files.append({
                    "path": file_data["path"],
                    "name": file_data["name"],
                    "size": file_data["size"],
                    "modified": file_data["modified"],
                    "content_preview": file_data.get("content", "")[:500] if file_data.get("content") else "No text content",
                    "relevance": relevance
                })
        
        relevant_files.sort(key=lambda x: x["relevance"], reverse=True)
        top_files = relevant_files[:20]
        
        # Build context for AI
        context = f"Desktop File Index Summary:\n"
        context += f"- Total files indexed: {len(self.index)}\n"
        context += f"- Relevant files found: {len(top_files)}\n\n"
        
        if top_files:
            context += "Most Relevant Files:\n"
            for i, file_info in enumerate(top_files[:10], 1):
                context += f"\n{i}. {file_info['name']}\n"
                context += f"   Path: {file_info['path']}\n"
                context += f"   Size: {file_info['size']} bytes\n"
                context += f"   Modified: {file_info['modified']}\n"
                context += f"   Preview: {file_info['content_preview'][:200]}...\n"
        
        # Ask Gemini
        try:
            client = get_client()
            
            prompt = f"""Based on the user's desktop file index, answer this question:

QUESTION: {question}

DESKTOP FILE CONTEXT:
{context}

Provide a helpful, accurate answer based on the indexed files. If you need more information, suggest what additional indexing or searches might help. Be specific about file names, paths, and content when relevant."""

            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            answer = response.text
            
            return {
                "success": True,
                "question": question,
                "answer": answer,
                "files_analyzed": len(top_files),
                "relevant_files": [f["path"] for f in top_files[:5]]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "question": question
            }
    
    def summarize_folder(self, folder_path: str) -> Dict:
        """
        AI-powered summary of a folder's contents
        
        Args:
            folder_path: Path to folder to summarize
        """
        print(f"\n📊 Summarizing folder: {folder_path}")
        
        # Get files in this folder
        folder_files = []
        
        for file_key, file_data in self.index.items():
            if folder_path in file_data["path"]:
                folder_files.append(file_data)
        
        if not folder_files:
            return {
                "success": False,
                "error": f"No indexed files found in {folder_path}. Try indexing first."
            }
        
        # Build summary context
        context = f"Folder: {folder_path}\n"
        context += f"Total files: {len(folder_files)}\n\n"
        
        # File types
        extensions = {}
        total_size = 0
        
        for file_data in folder_files:
            ext = file_data["extension"] or "no extension"
            extensions[ext] = extensions.get(ext, 0) + 1
            total_size += file_data["size"]
        
        context += "File Types:\n"
        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
            context += f"  {ext}: {count} files\n"
        
        context += f"\nTotal Size: {total_size / (1024*1024):.2f} MB\n\n"
        
        # Sample file names and content
        context += "Sample Files:\n"
        for file_data in folder_files[:20]:
            context += f"  - {file_data['name']}"
            if file_data.get("content"):
                context += f" (Preview: {file_data['content'][:100]}...)"
            context += "\n"
        
        # Ask Gemini to summarize
        try:
            client = get_client()
            
            prompt = f"""Analyze and summarize this folder:

{context}

Provide:
1. Overall purpose/theme of the folder
2. Main file types and what they're for
3. Organization quality (well-organized or messy)
4. Suggestions for better organization
5. Notable files or patterns
6. Potential cleanup opportunities"""

            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return {
                "success": True,
                "folder": folder_path,
                "file_count": len(folder_files),
                "total_size_mb": f"{total_size / (1024*1024):.2f}",
                "file_types": extensions,
                "summary": response.text
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def find_duplicates_smart(self) -> Dict:
        """Find duplicate files using AI-powered content analysis"""
        print("\n🔍 Finding duplicate files (smart analysis)...")
        
        # Group by name (without extension)
        name_groups = {}
        
        for file_key, file_data in self.index.items():
            name_base = Path(file_data["name"]).stem.lower()
            
            if name_base not in name_groups:
                name_groups[name_base] = []
            
            name_groups[name_base].append(file_data)
        
        # Find potential duplicates
        duplicates = []
        
        for name_base, files in name_groups.items():
            if len(files) > 1:
                # Check if content is similar
                for i, file1 in enumerate(files):
                    for file2 in files[i+1:]:
                        # Same size is a strong indicator
                        if file1["size"] == file2["size"]:
                            duplicates.append({
                                "file1": file1["path"],
                                "file2": file2["path"],
                                "name": name_base,
                                "size": file1["size"],
                                "confidence": "high"
                            })
                        # Similar name
                        elif file1["name"].lower() == file2["name"].lower():
                            duplicates.append({
                                "file1": file1["path"],
                                "file2": file2["path"],
                                "name": name_base,
                                "size_diff": abs(file1["size"] - file2["size"]),
                                "confidence": "medium"
                            })
        
        return {
            "success": True,
            "duplicates_found": len(duplicates),
            "duplicates": duplicates[:50],  # Limit results
            "potential_savings_mb": sum(d.get("size", 0) for d in duplicates) / (1024*1024)
        }
    
    def get_index_stats(self) -> Dict:
        """Get statistics about the current index"""
        if not self.index:
            return {
                "total_files": 0,
                "message": "No files indexed yet. Run quick index first."
            }
        
        extensions = {}
        total_size = 0
        with_content = 0
        
        for file_data in self.index.values():
            ext = file_data["extension"] or "no extension"
            extensions[ext] = extensions.get(ext, 0) + 1
            total_size += file_data["size"]
            if file_data.get("has_content"):
                with_content += 1
        
        return {
            "total_files": len(self.index),
            "files_with_text_content": with_content,
            "total_size_mb": f"{total_size / (1024*1024):.2f}",
            "file_types": dict(sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10]),
            "last_updated": max(
                (file_data["indexed_at"] for file_data in self.index.values()),
                default="Never"
            )
        }


def create_desktop_rag():
    """Factory function to create DesktopRAG instance"""
    return DesktopRAG()


# Example usage
if __name__ == "__main__":
    rag = create_desktop_rag()
    
    print("\n=== Desktop RAG Demo ===\n")
    
    # Index common folders
    result = rag.quick_index_common_folders()
    print(f"\n✅ Indexed {result['total_files_indexed']} files")
    
    # Get stats
    stats = rag.get_index_stats()
    print(f"\n📊 Index Stats:")
    print(f"   Total files: {stats['total_files']}")
    print(f"   Total size: {stats['total_size_mb']} MB")
    
    # Search example
    matches = rag.search_files("python")
    print(f"\n🔍 Found {len(matches)} files matching 'python'")
    
    # Ask question
    answer = rag.ask_about_files("What Python files do I have?")
    if answer["success"]:
        print(f"\n💬 AI Answer:\n{answer['answer']}")
