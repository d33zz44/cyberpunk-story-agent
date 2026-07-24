from typing import Optional
from llm.gigachat_client import GigaChatClient

class WriterAgent:
    """Агент-писатель"""
    
    def __init__(self, model: Optional[str] = None):
        self.llm = GigaChatClient(model=model)
    
    def write_initial_draft(self, topic: str) -> str:
        """Пишет первый черновик рассказа"""
        
        prompt = f"""
Ты — профессиональный писатель в жанре киберпанк. Напиши короткий рассказ (2000-3000 слов) на тему:

## Тема
{topic}

## Требования к стилю
- Мрачная, атмосферная эстетика киберпанка
- Минимум описаний, максимум действия
- Диалоги естественные, с подтекстом
- Избегай клише: "неоновый дождь", "холодный металл"
- Показывай, а не рассказывай

## Структура
1. Завязка (10%)
2. Развитие (50%)
3. Кульминация (25%)
4. Развязка (15%)

Напиши рассказ прямо сейчас, без вступлений.
"""
        print(" Писатель создает черновик...")
        draft = self.llm.generate(prompt, temperature=0.85)
        return draft
    
    def revise_draft(self, draft: str, critique: str) -> str:
        """Переписывает рассказ с учетом критики"""
        
        prompt = f"""
Ты — профессиональный писатель. Вот твой рассказ:

{draft}

## Критика и замечания
{critique}

Перепиши рассказ, исправляя все указанные недостатки. Сохрани сильные стороны.
Напиши исправленную версию.
"""
        print("Писатель правит рассказ...")
        new_draft = self.llm.generate(prompt, temperature=0.8)
        return new_draft