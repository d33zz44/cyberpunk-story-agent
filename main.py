import os
import sys
from config import Config
from agents import WriterAgent, CriticAgent

class StoryOrchestrator:
    def __init__(self):
        Config.ensure_dirs()
        self.writer = WriterAgent()
        self.critic = CriticAgent()
    
    def run_experiment(self, topic: str, max_iterations: int = 2):
        print(f"\n{'='*60}")
        print(f"ЗАПУСК ЭКСПЕРИМЕНТА")
        print(f"Тема: {topic}")
        print(f"{'='*60}\n")
        
        draft = self.writer.write_initial_draft(topic)
        self._save_draft(draft, "draft_v1.md")
        
        for i in range(max_iterations):
            print(f"\n--- ИТЕРАЦИЯ {i+1} ---")
            critique, scores = self.critic.analyze(draft)
            self._save_critique(critique, f"critique_v{i+1}.md")
            print(f"Оценка: {scores.get('total', '?')}/10")
            
            if self.critic.is_ready(critique, scores):
                print("Рассказ готов!")
                break
            
            if i < max_iterations - 1:
                draft = self.writer.revise_draft(draft, critique)
                self._save_draft(draft, f"draft_v{i+2}.md")
        
        self._save_draft(draft, "final_story.md")
        print(f"Эксперимент завершен!")
        return draft
    
    def _save_draft(self, content: str, filename: str):
        filepath = os.path.join(Config.DRAFTS_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📄 Сохранен: {filepath}")
    
    def _save_critique(self, content: str, filename: str):
        filepath = os.path.join(Config.CRITIQUES_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📄 Сохранена критика: {filepath}")

def main():
    if not Config.GIGACHAT_USERNAME or not Config.GIGACHAT_PASSWORD:
        print("Ошибка: Не найдены учетные данные GigaChat")
        print("Проверьте файл .env")
        sys.exit(1)
    
    orchestrator = StoryOrchestrator()
    topic = "История о хакере, который взламывает нейросеть, управляющую мегаполисом, и обнаруживает, что сам является частью симуляции"
    result = orchestrator.run_experiment(topic, max_iterations=2)
    
    print("\n" + "="*60)
    print("ФИНАЛЬНЫЙ РАССКАЗ (первые 500 символов)")
    print("="*60)
    print(result[:500] + "...")

if __name__ == "__main__":
    main()