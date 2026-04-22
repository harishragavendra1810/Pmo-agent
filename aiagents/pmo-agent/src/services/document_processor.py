"""Document processor for PMO Agent."""
import logging
from typing import Optional


logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Process various document types."""
    
    @staticmethod
    def process_meeting_transcript(transcript: str) -> str:
        """
        Process meeting transcript and extract key information.
        
        Args:
            transcript: Raw meeting transcript
            
        Returns:
            Processed transcript with key points
        """
        # Simple processing - in production, could use more sophisticated NLP
        lines = transcript.split('\n')
        processed_lines = []
        
        for line in lines:
            if line.strip():
                # Remove timestamps and speaker names for basic processing
                if ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        processed_lines.append(parts[1].strip())
                else:
                    processed_lines.append(line.strip())
        
        return '\n'.join(processed_lines)
    
    @staticmethod
    def process_sow_document(sow_content: str) -> str:
        """
        Process SOW document.
        
        Args:
            sow_content: Raw SOW content
            
        Returns:
            Processed SOW content
        """
        # Extract key sections for processing
        # In production, could parse and extract specific sections
        return sow_content.strip()
    
    @staticmethod
    def process_email_thread(email_content: str) -> str:
        """
        Process email thread.
        
        Args:
            email_content: Raw email content
            
        Returns:
            Processed email content
        """
        # Remove email headers, signatures, etc.
        lines = email_content.split('\n')
        processed = []
        skip_headers = False
        
        for line in lines:
            # Skip common email headers
            if line.startswith('From:') or line.startswith('To:') or line.startswith('Date:'):
                skip_headers = True
                continue
            if skip_headers and line.strip() == '':
                skip_headers = False
                continue
            if not skip_headers and line.strip():
                processed.append(line.strip())
        
        return '\n'.join(processed)
    
    @staticmethod
    async def extract_action_items(text: str) -> list[str]:
        """
        Extract action items from text.
        
        Args:
            text: Input text
            
        Returns:
            List of action items
        """
        action_items = []
        keywords = ['action item:', 'todo:', 'task:', 'needs to:', 'should:']
        
        lines = text.split('\n')
        for line in lines:
            lower_line = line.lower()
            for keyword in keywords:
                if keyword in lower_line:
                    item = line.replace(keyword, '').strip()
                    if item:
                        action_items.append(item)
        
        return action_items
