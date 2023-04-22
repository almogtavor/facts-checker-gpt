import abc
import os
import openai
from dotenv import load_dotenv

load_dotenv()


class Singleton(abc.ABCMeta, type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Call method for the singleton metaclass."""
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class AbstractSingleton(abc.ABC, metaclass=Singleton):
    pass


class Config(metaclass=Singleton):
    """
    Configuration class to store the state of bools for different scripts access.
    """

    def __init__(self):
        """Initialize the Config class"""
        self.debug_mode = False
        self.continuous_mode = False
        self.continuous_limit = 0
        self.speak_mode = False
        self.skip_reprompt = False

        self.ai_settings_file = os.getenv("AI_SETTINGS_FILE", "ai_settings.yaml")
        self.fast_token_limit = int(os.getenv("FAST_TOKEN_LIMIT", 4000))
        self.smart_token_limit = int(os.getenv("SMART_TOKEN_LIMIT", 8000))
        self.browse_chunk_max_length = int(os.getenv("BROWSE_CHUNK_MAX_LENGTH", 8192))
        self.browse_summary_max_token =  int(os.getenv("BROWSE_SUMMARY_MAX_TOKEN", 300))

        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.temperature = float(os.getenv("TEMPERATURE", "1"))
        self.execute_local_commands = os.getenv('EXECUTE_LOCAL_COMMANDS', 'False') == 'True'

        self.chatbot_agent_1_model = os.getenv("CHATBOT_AGENT1_MODEL", "gpt-4")
        self.chatbot_agent_2_model = os.getenv("CHATBOT_AGENT2_MODEL", "gpt-3.5-turbo")
        self.fact_checker_agent_model = os.getenv("FACT_CHECKER_AGENT_MODEL", "gpt-3.5-turbo")
        self.agent_3_model = os.getenv("AGENT3_MODEL")

        self.alpaca_model_path = os.getenv("ALPACA_MODEL_PATH")
        self.alpaca_executable_path = os.getenv("ALPACA_EXECUTABLE_PATH")

        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.custom_search_engine_id = os.getenv("CUSTOM_SEARCH_ENGINE_ID")

        # User agent headers to use when browsing web
        # Some websites might just completely deny request with an error code if no user agent was found.
        self.user_agent = os.getenv("USER_AGENT", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36")
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = os.getenv("REDIS_PORT", "6379")
        self.redis_password = os.getenv("REDIS_PASSWORD", "")
        self.wipe_redis_on_start = os.getenv("WIPE_REDIS_ON_START", "True") == 'True'
        self.memory_index = os.getenv("MEMORY_INDEX", 'facts-checker-gpt')
        # Note that indexes must be created on db 0 in redis, this is not configurable.

        self.memory_backend = os.getenv("MEMORY_BACKEND", 'local')
        # Initialize the OpenAI API client
        openai.api_key = self.openai_api_key

