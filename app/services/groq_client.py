"""
Groq API client for generating motivational quotes.
"""

from typing import Optional

import requests

from app.config import settings
from app.utils import get_french_date_info, sanitize_quote


class GroqClient:
    """Client for interacting with Groq LLM API."""
    
    def __init__(self):
        """Initialize Groq client with API configuration."""
        self.api_key = settings.GROQ_API_KEY
        self.api_url = settings.GROQ_API_URL
        self.model = settings.GROQ_MODEL
        self.temperature = settings.GROQ_TEMPERATURE
        self.max_tokens = settings.GROQ_MAX_TOKENS
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables")
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for Groq API."""
        return (
            "Tu es un expert en citations motivationnelles ultra-positives et énergisantes. "
            "Tu connais les meilleures citations de personnalités inspirantes : "
            "Nelson Mandela, Steve Jobs, Oprah Winfrey, Albert Einstein, Maya Angelou, "
            "Tony Robbins, Les Brown, et bien d'autres. "
            "Tu adaptes ces citations en français de manière naturelle, énergique et ultra-positive. "
            "Tu ne mentionnes JAMAIS de termes négatifs comme échec, difficulté, problème, obstacle, peur, doute, etc. "
            "Tu te concentres uniquement sur la positivité, l'énergie, le succès, la force, la joie, la détermination."
        )
    
    def _build_user_prompt(self) -> str:
        """Build the user prompt with current date for variety."""
        date_str, day_of_year = get_french_date_info()
        
        return (
            f"Nous sommes le {date_str} (jour {day_of_year} de l'année). "
            "Génère UNE SEULE citation motivationnelle ultra-positive et énergisante en français. "
            "Contraintes strictes :\n"
            "- Maximum 200 caractères\n"
            "- Citation d'une personnalité célèbre (auteur, entrepreneur, leader, coach, etc.)\n"
            "- Style ultra-positif, énergique, puissant, motivant pour démarrer la journée\n"
            "- Format : Citation suivie de \"— Nom de l'auteur\"\n"
            "- INTERDICTION ABSOLUE de mentionner : échec, difficulté, problème, obstacle, peur, doute, négativité, défis négatifs\n"
            "- Seulement des messages sur : succès, force, énergie, détermination, joie, passion, victoire, excellence, croissance, possibilités infinies\n"
            "- Exemple positif : \"Crois en tes rêves et ils se réaliseront. L'énergie suit l'intention. — Tony Robbins\"\n"
            "- Ne pas répéter les mêmes citations chaque jour (utilise la date pour varier)\n"
            "- Pas de guillemets autour de la citation complète\n"
            "- 1-2 emojis énergiques si approprié (💪 ✨ 🚀 ⭐)"
        )
    
    
    def generate_quote(self) -> str:
        """
        Generate a motivational quote using Groq LLM API.
        
        Returns:
            str: The generated motivational quote
            
        Raises:
            Exception: If API call fails or returns invalid response
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self._build_system_prompt()},
                {"role": "user", "content": self._build_user_prompt()},
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        
        try:
            print("🤖 Calling Groq API to generate motivational quote...")
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            quote = data["choices"][0]["message"]["content"]
            quote = sanitize_quote(quote)
            
            print(f"✨ Generated quote: {quote}")
            return quote
            
        except requests.exceptions.Timeout:
            print("❌ Groq API request timed out")
            raise Exception("Request to Groq API timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error calling Groq API: {e}")
            raise Exception(f"Failed to generate quote: {str(e)}")
        except (KeyError, IndexError) as e:
            print(f"❌ Invalid response from Groq API: {e}")
            raise Exception(f"Invalid response format from Groq API: {str(e)}")


def get_groq_client() -> GroqClient:
    """Factory function to get Groq client instance."""
    return GroqClient()

