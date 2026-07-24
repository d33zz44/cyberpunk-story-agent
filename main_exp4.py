import os
import sys
from datetime import datetime
from config import Config
from agents import WriterAgent, CriticAgent, EditorAgent, PelevinStyleAgent, MinimalistStyleAgent

class StoryOrchestrator:
    def __init__(self):
        Config.ensure_dirs()
        self.writer = WriterAgent()
        self.editor = EditorAgent()
        self.pelevin = PelevinStyleAgent()
        self.minimalist = MinimalistStyleAgent()
        self.critic = CriticAgent()
        self.experiment_log = []
    
    def run_experiment(self, topic: str):
        print(f"\n{'='*60}")
        print(f"ЭКСПЕРИМЕНТ №4: Стилист-минималист")
        print(f"Тема: {topic}")
        print(f"{'='*60}\n")
        
        # Шаг 1: Писатель
        print("ШАГ 1: Писатель создает черновик")
        draft = self.writer.write_initial_draft(topic)
        self._save_draft(draft, "exp4_draft_v1.md")
        
        # Шаг 2: Редактор
        print(" ШАГ 2: Редактор убирает клише")
        edited = self.editor.edit(draft)
        self._save_draft(edited, "exp4_draft_edited.md")
        
        # Шаг 3: Пелевин
        print("ШАГ 3: Стилист 'Пелевин' добавляет философию")
        pelevin_text = self.pelevin.apply_style(edited)
        self._save_draft(pelevin_text, "exp4_draft_pelevin.md")
        
        # Шаг 4: Минималист
        print("ШАГ 4: Стилист-минималист очищает текст")
        minimalist_text = self.minimalist.apply_style(pelevin_text)
        self._save_draft(minimalist_text, "exp4_draft_minimalist.md")
        
        # Шаг 5: Критик
        print(" ШАГ 5: Критик оценивает результат")
        critique, scores = self.critic.analyze(minimalist_text)
        self._save_critique(critique, "exp4_critique.md")
        
        print(f"Оценка критика: {scores.get('total', '?')}/10")
        
        # Статистика
        print(f"Статистика:")
        print(f"  - Оригинал: {len(draft)} символов")
        print(f"  - После редактора: {len(edited)} символов")
        print(f"  - После Пелевина: {len(pelevin_text)} символов")
        print(f"  - После минималиста: {len(minimalist_text)} символов")
        print(f"  - Сокращение: {len(pelevin_text) - len(minimalist_text)} символов ({round((len(pelevin_text) - len(minimalist_text)) / len(pelevin_text) * 100)}%)")
        
        self._save_draft(minimalist_text, "exp4_final_story.md")
        
        print(f"Эксперимент №4 завершен!")
        return minimalist_text, scores
    
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
    
    final_story, scores = orchestrator.run_experiment(topic)
    
    print("\n" + "="*60)
    print("ФИНАЛЬНЫЙ РАССКАЗ (первые 500 символов)")
    print("="*60)
    print(final_story[:500] + "...")
    print("="*60)

if __name__ == "__main__":
    main()
