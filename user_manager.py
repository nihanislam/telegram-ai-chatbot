from config import DEFAULT_MODEL, DEFAULT_SYSTEM_PROMPT, MAX_CONVERSATION_HISTORY
import logging

logger = logging.getLogger(__name__)

class UserManager:
    def __init__(self):
        self.users = {}
    
    def get_user(self, user_id: int):
        """Get or create user data"""
        if user_id not in self.users:
            self.users[user_id] = {
                'model': DEFAULT_MODEL,
                'system_prompt': DEFAULT_SYSTEM_PROMPT,
                'conversation': [],
                'message_count': 0,
                'temperature': 0.7
            }
            logger.info(f"New user created: {user_id}")
        return self.users[user_id]
    
    def set_model(self, user_id: int, model: str):
        user = self.get_user(user_id)
        user['model'] = model
        logger.info(f"User {user_id} changed model to {model}")
    
    def set_system_prompt(self, user_id: int, prompt: str):
        user = self.get_user(user_id)
        user['system_prompt'] = prompt
        user['conversation'] = []  # Reset conversation
        logger.info(f"User {user_id} updated system prompt")
    
    def set_temperature(self, user_id: int, temperature: float):
        user = self.get_user(user_id)
        user['temperature'] = max(0.0, min(2.0, temperature))
        logger.info(f"User {user_id} set temperature to {temperature}")
    
    def add_message(self, user_id: int, role: str, content: str):
        user = self.get_user(user_id)
        user['conversation'].append({"role": role, "content": content})
        user['message_count'] += 1
        
        # Keep conversation history manageable
        if len(user['conversation']) > MAX_CONVERSATION_HISTORY:
            user['conversation'] = user['conversation'][-MAX_CONVERSATION_HISTORY:]
    
    def get_messages(self, user_id: int):
        user = self.get_user(user_id)
        return [
            {"role": "system", "content": user['system_prompt']},
            *user['conversation']
        ]
    
    def reset_conversation(self, user_id: int):
        user = self.get_user(user_id)
        user['conversation'] = []
        logger.info(f"User {user_id} reset conversation")
    
    def get_stats(self, user_id: int):
        user = self.get_user(user_id)
        return {
            'message_count': user['message_count'],
            'conversation_length': len(user['conversation']),
            'current_model': user['model'],
            'temperature': user['temperature']
        }
    
    def export_conversation(self, user_id: int):
        """Export conversation history as text"""
        user = self.get_user(user_id)
        export = f"System Prompt: {user['system_prompt']}\n\n"
        export += "=" * 50 + "\n\n"
        
        for msg in user['conversation']:
            role = "You" if msg['role'] == 'user' else "AI"
            export += f"{role}: {msg['content']}\n\n"
        
        return export