import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GIGACHAT_USERNAME = os.getenv('GIGACHAT_USERNAME')
    GIGACHAT_PASSWORD = os.getenv('GIGACHAT_PASSWORD')
    GIGACHAT_MODEL = os.getenv('GIGACHAT_MODEL', 'GigaChat-2-Pro')
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 4000))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.8))
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    WORKSPACE_DIR = os.path.join(BASE_DIR, 'workspace')
    DRAFTS_DIR = os.path.join(WORKSPACE_DIR, 'drafts')
    CRITIQUES_DIR = os.path.join(WORKSPACE_DIR, 'critiques')
    MEMORY_DIR = os.path.join(WORKSPACE_DIR, 'memory')
    REPORTS_DIR = os.path.join(WORKSPACE_DIR, 'reports')
    
    @classmethod
    def ensure_dirs(cls):
        dirs = [cls.WORKSPACE_DIR, cls.DRAFTS_DIR, cls.CRITIQUES_DIR, 
                cls.MEMORY_DIR, cls.REPORTS_DIR]
        for d in dirs:
            os.makedirs(d, exist_ok=True)