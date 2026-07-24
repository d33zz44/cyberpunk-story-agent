import os
import sys
from datetime import datetime
from config import Config
from agents import WriterAgent, CriticAgent, EditorAgent

class StoryOrchestrator:
    def __init__(self):
        Config.ensure_dirs()
        self.writer = WriterAgent()
        self.editor = EditorAgent()
        self.critic = CriticAgent()
        self.experiment_log = []
    
    def run_experiment(self, topic: str, max_iterations: int = 1):
        print(f"{'='*60}")
        print(f"ЭКСПЕРИМЕНТ №2: Добавление редактора")
        print(f"Тема: {topic}")
        print(f"{'='*60}\n")
        
        # Шаг 1: Писатель создает черновик
        print("ШАГ 1: Писатель создает черновик")
        draft = self.writer.write_initial_draft(topic)
        self._save_draft(draft, "exp2_draft_v1.md")
        
        # Шаг 2: Редактор правит текст
        print("ШАГ 2: Редактор убирает клише и штампы")
        edited_draft = self.editor.edit(draft)
        self._save_draft(edited_draft, "exp2_draft_edited.md")
        
        # Шаг 3: Критик оценивает
        print("ШАГ 3: Критик оценивает отредактированный текст")
        critique, scores = self.critic.analyze(edited_draft)
        self._save_critique(critique, "exp2_critique.md")
        
        print(f"Оценка критика: {scores.get('total', '?')}/10")
        
        # Сравнение длин
        print(f"Статистика:")
        print(f"  - Оригинал: {len(draft)} символов")
        print(f"  - После редактора: {len(edited_draft)} символов")
        print(f"  - Сокращение: {len(draft) - len(edited_draft)} символов")
        
        # Сохраняем финал
        self._save_draft(edited_draft, "exp2_final_story.md")
        
        print(f"Эксперимент №2 завершен!")
        return edited_draft, scores
    
    def _save_draft(self, content: str, filename: str):
        filepath = os.path.join(Config.DRAFTS_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Сохранен: {filepath}")
    
    def _save_critique(self, content: str, filename: str):
        filepath = os.path.join(Config.CRITIQUES_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Сохранена критика: {filepath}")

def main():
    if not Config.GIGACHAT_USERNAME or not Config.GIGACHAT_PASSWORD:
        print("Ошибка: Не найдены учетные данные GigaChat")
        print("Проверьте файл .env")
        sys.exit(1)
    
    orchestrator = StoryOrchestrator()
    
    topic = "История о хакере, который взламывает нейросеть, управляющую мегаполисом, и обнаруживает, что сам является частью симуляции"
    
    final_story, scores = orchestrator.run_experiment(topic, max_iterations=1)
    
    print("\n" + "="*60)
    print("ФИНАЛЬНЫЙ РАССКАЗ (первые 500 символов)")
    print("="*60)
    print(final_story[:500] + "...")
    print("="*60)

if __name__ == "__main__":
    main()