import os
import json
from datetime import datetime
from typing import Optional, Dict, List, Any
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class AIFeatures:
    """
    Comprehensive AI Features Module
    Provides access to various AI capabilities including chatbots, text generation,
    language processing, image generation, data analysis, computer vision, and voice/audio.
    """
    
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        
        self.conversation_history_file = "ai_conversations.json"
        self.conversation_history = self.load_conversation_history()
    
    def load_conversation_history(self) -> dict:
        """Load conversation history from file"""
        if os.path.exists(self.conversation_history_file):
            try:
                with open(self.conversation_history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_conversation_history(self):
        """Save conversation history to file"""
        try:
            with open(self.conversation_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving conversation history: {e}")
    
    def get_client(self):
        """Get or initialize the Gemini client"""
        if self.client is None:
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY not set")
            self.client = genai.Client(api_key=self.api_key)
        return self.client

    def conversational_ai(self, message: str, context: str = "general") -> str:
        """
        Conversational AI - General purpose chatbot
        """
        try:
            client = self.get_client()
            
            if context not in self.conversation_history:
                self.conversation_history[context] = []
            
            self.conversation_history[context].append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })
            
            history_context = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in self.conversation_history[context][-5:]
            ])
            
            prompt = f"""You are a helpful, friendly AI assistant. Respond naturally to the user's message.
            
Previous conversation:
{history_context}

User: {message}

Provide a helpful, conversational response:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            reply = response.text
            
            self.conversation_history[context].append({
                "role": "assistant",
                "content": reply,
                "timestamp": datetime.now().isoformat()
            })
            
            self.save_conversation_history()
            
            return reply
            
        except Exception as e:
            return f"Error in conversational AI: {str(e)}"

    def customer_service_bot(self, query: str, company_context: str = "") -> str:
        """
        Customer Service Bot - Specialized for customer support
        """
        try:
            client = self.get_client()
            
            prompt = f"""You are a professional customer service representative.

Company Context: {company_context if company_context else "General customer service"}

Customer Query: {query}

Provide a helpful, professional, and empathetic response addressing the customer's concern:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in customer service bot: {str(e)}"

    def educational_assistant(self, topic: str, question: str, level: str = "intermediate") -> str:
        """
        Educational Assistant - Helps with learning and education
        """
        try:
            client = self.get_client()
            
            prompt = f"""You are an educational assistant helping students learn.

Topic: {topic}
Learning Level: {level}
Student Question: {question}

Provide a clear, educational explanation with examples. Break down complex concepts into simple terms:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in educational assistant: {str(e)}"

    def domain_expert(self, domain: str, question: str) -> str:
        """
        Domain Expert - Specialized knowledge in specific fields
        """
        try:
            client = self.get_client()
            
            prompt = f"""You are an expert in {domain}. Provide detailed, accurate information based on deep domain knowledge.

Question: {question}

Provide an expert-level response with specific details, facts, and insights:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in domain expert: {str(e)}"

    def story_writer(self, prompt: str, genre: str = "general", length: str = "medium") -> str:
        """
        Story Writer - Create creative stories
        """
        try:
            client = self.get_client()
            
            length_guide = {
                "short": "Write a brief story (200-300 words)",
                "medium": "Write a story (500-800 words)",
                "long": "Write a detailed story (1000-1500 words)"
            }
            
            instruction = f"""You are a creative story writer.

Genre: {genre}
Story Prompt: {prompt}

{length_guide.get(length, length_guide['medium'])}

Write an engaging, well-structured story:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=instruction
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in story writer: {str(e)}"

    def content_creator(self, topic: str, content_type: str = "blog post", tone: str = "professional") -> str:
        """
        Content Creator - Generate various types of content
        """
        try:
            client = self.get_client()
            
            prompt = f"""You are a skilled content creator.

Content Type: {content_type}
Topic: {topic}
Tone: {tone}

Create engaging, high-quality content for the specified type and tone:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in content creator: {str(e)}"

    def article_generator(self, title: str, keywords: Optional[List[str]] = None, word_count: int = 800) -> str:
        """
        Article Generator - Generate full articles
        """
        try:
            client = self.get_client()
            
            keywords_str = ", ".join(keywords) if keywords else "relevant keywords"
            
            prompt = f"""You are a professional article writer.

Article Title: {title}
Target Keywords: {keywords_str}
Target Word Count: {word_count} words

Write a well-researched, informative article with proper structure (introduction, body, conclusion):"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in article generator: {str(e)}"

    def copywriting_assistant(self, product: str, goal: str = "persuade") -> str:
        """
        Copywriting Assistant - Create persuasive marketing copy
        """
        try:
            client = self.get_client()
            
            prompt = f"""You are an expert copywriter.

Product/Service: {product}
Goal: {goal}

Write compelling marketing copy that engages and converts. Include headlines, body copy, and call-to-action:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in copywriting assistant: {str(e)}"

    def technical_writer(self, topic: str, audience: str = "technical") -> str:
        """
        Technical Writer - Create technical documentation
        """
        try:
            client = self.get_client()
            
            prompt = f"""You are a technical writer creating clear, accurate documentation.

Topic: {topic}
Target Audience: {audience}

Write comprehensive technical documentation with clear explanations, examples, and proper structure:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in technical writer: {str(e)}"

    def text_translator(self, text: str, target_language: str, source_language: str = "auto") -> str:
        """
        Text Translator - Translate text between languages
        """
        try:
            client = self.get_client()
            
            prompt = f"""Translate the following text to {target_language}.
{f'Source language: {source_language}' if source_language != 'auto' else 'Detect the source language automatically.'}

Text to translate:
{text}

Provide only the translation:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in text translator: {str(e)}"

    def sentiment_analysis(self, text: str) -> str:
        """
        Sentiment Analysis - Analyze emotional tone of text
        """
        try:
            client = self.get_client()
            
            prompt = f"""Analyze the sentiment of the following text and provide a detailed analysis.

Text: {text}

Provide:
1. Overall sentiment (positive/negative/neutral)
2. Sentiment score (-1.0 to 1.0)
3. Key emotions detected
4. Confidence level

Return the analysis in JSON format:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in sentiment analysis: {str(e)}"

    def text_summarizer(self, text: str, length: str = "medium") -> str:
        """
        Text Summarizer - Create summaries of long text
        """
        try:
            client = self.get_client()
            
            length_guide = {
                "brief": "1-2 sentences",
                "medium": "1 paragraph (3-5 sentences)",
                "detailed": "2-3 paragraphs with key points"
            }
            
            prompt = f"""Summarize the following text in {length_guide.get(length, length_guide['medium'])}.

Text:
{text}

Summary:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in text summarizer: {str(e)}"

    def language_detector(self, text: str) -> str:
        """
        Language Detector - Identify the language of text
        """
        try:
            client = self.get_client()
            
            prompt = f"""Identify the language of the following text. Provide the language name and ISO code.

Text: {text}

Response format: Language Name (ISO Code) - Confidence Level"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in language detector: {str(e)}"

    def content_moderator(self, text: str) -> str:
        """
        Content Moderator - Check content for inappropriate material
        """
        try:
            client = self.get_client()
            
            prompt = f"""Analyze the following text for content moderation.

Text: {text}

Check for:
1. Inappropriate language
2. Hate speech
3. Violence
4. Sensitive topics
5. Overall safety rating

Provide a moderation report in JSON format:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in content moderator: {str(e)}"

    def image_description_generator(self, concept: str, style: str = "realistic") -> str:
        """
        AI Art Creator - Generate detailed image descriptions for AI art
        """
        try:
            client = self.get_client()
            
            prompt = f"""Create a detailed prompt for AI image generation.

Concept: {concept}
Style: {style}

Generate a comprehensive, detailed description that an AI image generator could use. Include:
- Main subject
- Style and mood
- Lighting and atmosphere
- Colors and composition
- Artistic details

Image generation prompt:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in image description generator: {str(e)}"

    def style_transfer_description(self, content: str, style: str) -> str:
        """
        Style Transfer - Generate descriptions for style transfer
        """
        try:
            client = self.get_client()
            
            prompt = f"""Create a detailed description for applying style transfer.

Content: {content}
Target Style: {style}

Describe how the content should be transformed in the specified style:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in style transfer: {str(e)}"

    def analyze_data_patterns(self, data_description: str) -> str:
        """
        Pattern Recognition - Analyze patterns in data
        """
        try:
            client = self.get_client()
            
            prompt = f"""Analyze the following data for patterns.

Data Description: {data_description}

Identify:
1. Key patterns and trends
2. Anomalies or outliers
3. Correlations
4. Insights and recommendations

Provide detailed analysis:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in pattern recognition: {str(e)}"

    def trend_analysis(self, data_description: str, time_period: str = "") -> str:
        """
        Trend Analysis - Analyze trends over time
        """
        try:
            client = self.get_client()
            
            prompt = f"""Perform trend analysis on the following data.

Data: {data_description}
{f'Time Period: {time_period}' if time_period else ''}

Analyze:
1. Overall trend direction
2. Significant changes
3. Seasonal patterns
4. Future predictions
5. Key insights

Provide comprehensive trend analysis:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in trend analysis: {str(e)}"

    def predictive_modeling(self, scenario: str, variables: Optional[List[str]] = None) -> str:
        """
        Predictive Modeling - Make predictions based on scenarios
        """
        try:
            client = self.get_client()
            
            vars_str = ", ".join(variables) if variables else "relevant variables"
            
            prompt = f"""Create a predictive model for the following scenario.

Scenario: {scenario}
Key Variables: {vars_str}

Provide:
1. Prediction methodology
2. Expected outcomes
3. Confidence levels
4. Risk factors
5. Recommendations

Detailed prediction:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in predictive modeling: {str(e)}"

    def data_insights(self, data_description: str) -> str:
        """
        Data Insights - Extract actionable insights from data
        """
        try:
            client = self.get_client()
            
            prompt = f"""Extract actionable insights from the following data.

Data: {data_description}

Provide:
1. Key findings
2. Actionable recommendations
3. Business implications
4. Next steps

Generate comprehensive insights:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in data insights: {str(e)}"

    def statistical_analysis(self, data_description: str) -> str:
        """
        Statistical Analysis - Perform statistical analysis
        """
        try:
            client = self.get_client()
            
            prompt = f"""Perform statistical analysis on the following data.

Data: {data_description}

Provide:
1. Descriptive statistics
2. Distribution analysis
3. Correlation analysis
4. Statistical significance
5. Interpretation

Detailed statistical analysis:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in statistical analysis: {str(e)}"

    def image_recognition_guide(self, image_description: str) -> str:
        """
        Image Recognition - Guide for recognizing objects in images
        """
        try:
            client = self.get_client()
            
            prompt = f"""Provide guidance for image recognition task.

Image Description: {image_description}

Describe:
1. Objects that should be recognized
2. Key features to look for
3. Recognition approach
4. Expected results

Image recognition guidance:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in image recognition: {str(e)}"

    def object_detection_guide(self, scenario: str) -> str:
        """
        Object Detection - Guide for detecting specific objects
        """
        try:
            client = self.get_client()
            
            prompt = f"""Create an object detection strategy.

Scenario: {scenario}

Provide:
1. Objects to detect
2. Detection criteria
3. Bounding box specifications
4. Confidence thresholds
5. Implementation approach

Object detection guide:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in object detection: {str(e)}"

    def scene_analysis_guide(self, scene_type: str) -> str:
        """
        Scene Analysis - Analyze and understand scenes
        """
        try:
            client = self.get_client()
            
            prompt = f"""Provide scene analysis guidance.

Scene Type: {scene_type}

Describe:
1. Key elements in the scene
2. Spatial relationships
3. Context and setting
4. Important details
5. Analysis approach

Scene analysis guide:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in scene analysis: {str(e)}"

    def generate_speech_text(self, topic: str, duration_minutes: int = 5, tone: str = "professional") -> str:
        """
        Voice Synthesis Content - Generate text for speech synthesis
        """
        try:
            client = self.get_client()
            
            prompt = f"""Create a speech script for text-to-speech synthesis.

Topic: {topic}
Duration: {duration_minutes} minutes
Tone: {tone}

Generate a natural-sounding script with:
1. Clear pronunciation
2. Appropriate pacing
3. Natural pauses
4. Engaging delivery

Speech script:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in speech text generation: {str(e)}"

    def audio_analysis_guide(self, audio_type: str) -> str:
        """
        Audio Analysis - Guide for analyzing audio content
        """
        try:
            client = self.get_client()
            
            prompt = f"""Provide audio analysis guidance.

Audio Type: {audio_type}

Describe:
1. Key features to analyze
2. Analysis metrics
3. Quality assessment criteria
4. Expected patterns
5. Interpretation methods

Audio analysis guide:"""
            
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Error in audio analysis: {str(e)}"

    def list_ai_features(self) -> dict:
        """
        List all available AI features organized by category
        """
        return {
            "Chatbots": [
                "conversational_ai - General purpose conversational AI",
                "customer_service_bot - Customer support assistant",
                "educational_assistant - Learning and education help",
                "domain_expert - Specialized domain knowledge"
            ],
            "Text Generation": [
                "story_writer - Create creative stories",
                "content_creator - Generate various content types",
                "article_generator - Write full articles",
                "copywriting_assistant - Marketing copy creation",
                "technical_writer - Technical documentation"
            ],
            "Language Processing": [
                "text_translator - Translate between languages",
                "sentiment_analysis - Analyze emotional tone",
                "text_summarizer - Summarize long text",
                "language_detector - Identify language",
                "content_moderator - Content safety checking"
            ],
            "Image Generation": [
                "image_description_generator - AI art prompts",
                "style_transfer_description - Style transfer guidance"
            ],
            "Data Analysis": [
                "analyze_data_patterns - Pattern recognition",
                "trend_analysis - Analyze trends over time",
                "predictive_modeling - Make predictions",
                "data_insights - Extract actionable insights",
                "statistical_analysis - Statistical analysis"
            ],
            "Computer Vision": [
                "image_recognition_guide - Image recognition guidance",
                "object_detection_guide - Object detection strategies",
                "scene_analysis_guide - Scene understanding"
            ],
            "Voice & Audio": [
                "generate_speech_text - Speech synthesis scripts",
                "audio_analysis_guide - Audio analysis guidance"
            ]
        }


def create_ai_features():
    """Factory function to create AIFeatures instance"""
    return AIFeatures()
