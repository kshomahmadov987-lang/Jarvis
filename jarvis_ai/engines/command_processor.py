"""
Command Processor for Jarvis AI
Handles natural language processing and command matching
"""

import re
from typing import Dict, List, Optional, Callable, Tuple


class CommandProcessor:
    """
    Processes and matches voice commands to handlers.
    Supports pattern matching and fuzzy matching.
    """
    
    def __init__(self):
        """Initialize command processor."""
        self.commands: Dict[str, Callable] = {}
        self.patterns: Dict[re.Pattern, Callable] = {}
        self.aliases: Dict[str, str] = {}
        
    def register_command(self, phrase: str, handler: Callable, aliases: List[str] = None):
        """
        Register a command with optional aliases.
        
        Args:
            phrase: Primary command phrase
            handler: Function to execute
            aliases: List of alternative phrases
        """
        self.commands[phrase.lower()] = handler
        
        if aliases:
            for alias in aliases:
                self.aliases[alias.lower()] = phrase.lower()
                
    def register_pattern(self, pattern: str, handler: Callable):
        """
        Register a regex pattern for dynamic command matching.
        
        Args:
            pattern: Regex pattern string
            handler: Function that takes matched groups as arguments
        """
        self.patterns[re.compile(pattern, re.IGNORECASE)] = handler
        
    def process(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        Process input text and find matching command.
        
        Args:
            text: Input text to process
            
        Returns:
            Tuple of (success, matched_command)
        """
        text = text.lower().strip()
        
        # Check direct command match
        if text in self.commands:
            return True, text
            
        # Check aliases
        if text in self.aliases:
            canonical = self.aliases[text]
            if canonical in self.commands:
                return True, canonical
                
        # Check regex patterns
        for pattern, handler in self.patterns.items():
            match = pattern.match(text)
            if match:
                try:
                    handler(*match.groups())
                    return True, f"pattern:{pattern.pattern}"
                except Exception as e:
                    print(f"[COMMAND] Pattern handler error: {e}")
                    
        return False, None
        
    def get_similarity(self, s1: str, s2: str) -> float:
        """
        Calculate similarity between two strings.
        Uses simple character overlap ratio.
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            Similarity score between 0 and 1
        """
        if not s1 or not s2:
            return 0.0
            
        s1, s2 = s1.lower(), s2.lower()
        
        # Simple word overlap
        words1 = set(s1.split())
        words2 = set(s2.split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0
        
    def suggest_command(self, text: str, threshold: float = 0.3) -> List[str]:
        """
        Suggest similar commands based on input text.
        
        Args:
            text: Input text
            threshold: Minimum similarity threshold
            
        Returns:
            List of suggested command phrases
        """
        suggestions = []
        
        for command in self.commands.keys():
            similarity = self.get_similarity(text, command)
            if similarity >= threshold:
                suggestions.append((command, similarity))
                
        # Sort by similarity
        suggestions.sort(key=lambda x: x[1], reverse=True)
        
        return [cmd for cmd, _ in suggestions[:5]]
        
    def extract_parameters(self, text: str) -> Dict[str, str]:
        """
        Extract common parameters from command text.
        
        Args:
            text: Command text
            
        Returns:
            Dictionary of extracted parameters
        """
        params = {}
        
        # Extract time references
        time_patterns = [
            r'at (\d+:\d+\s*(?:am|pm)?)',
            r'in (\d+)\s*(minutes?|hours?|days?)',
            r'on (\w+day|\w+day\s+\d+)',
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                params['time'] = match.group(0)
                break
                
        # Extract location
        location_patterns = [
            r'in ([\w\s]+?)(?:\s*(?:at|on|for)|$)',
            r'at ([\w\s]+?)(?:\s*(?:in|on|for)|$)',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                params['location'] = match.group(1).strip()
                break
                
        return params
