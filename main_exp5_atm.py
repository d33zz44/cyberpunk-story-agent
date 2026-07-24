import os
import sys
from config import Config
from agents import WriterAgent, CriticAgent, EditorAgent, PelevinStyleAgent, MinimalistStyleAgent, AtmosphereStyleAgent

class StoryOrchestrator:
    def __init__(self):
        Config.ensure_dirs()
        self.writer = WriterAgent()
        self.editor = EditorAgent()
        self.pelevin = PelevinStyleAgent()
        self.minimalist = MinimalistStyleAgent()
        self.atmosphere = AtmosphereStyleAgent()
        self.critic = CriticAgent()
    
    def run_experiment(self, topic: str):
        print(f"\n{'='*60}")
        print(f"ЭКСПЕРИМЕНТ №5: Агент-атмосфера")
        print(f"Тема: {topic}")
        print(f"{'='*60}\n")
        
        draft = self.writer.write_initial_draft(topic)
        self._save_draft(draft, "exp5_draft_v1.md")
        
        edited = self.editor.edit(draft)
        self._save_draft(edited, "exp5_draft_edited.md")
        
        pelevin_text = self.pelevin.apply_style(edited)
        self._save_draft(pelevin_text, "exp5_draft_pelevin.md")
        
        minimalist_text = self.minimalist.apply_style(pelevin_text)
        self._save_draft(minimalist_text, "exp5_draft_minimalist.md")
        
        # НОВЫЙ АГЕНТ!
        print("ШАГ 5: Агент-атмосфера создает настроение")
        atmosphere_text = self.atmosphere.apply_style(minimalist_text)
        self._save_draft(atmosphere_text, "exp5_draft_atmosphere.md")
        
        critique, scores = self.critic.analyze(atmosphere_text)
        self._save_critique(critique, "exp5_critique.md")
        
        print(f"Оценка критика: {scores.get('total', '?')}/10")
        
        print(f"Статистика:")
        print(f"  - Оригинал: {len(draft)} символов")
        print(f"  - После минималиста: {len(minimalist_text)} символов")
        print(f"  - После атмосферы: {len(atmosphere_text)} символов")
        
        self._save_draft(atmosphere_text, "exp5_final_story.md")
        
        print(f"Эксперимент №5 завершен!")
        return atmosphere_text, scores
    
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
        sys.exit(1)
    
    orchestrator = StoryOrchestrator()
    topic = "История о хакере, который взламывает нейросеть, управляющую мегаполисом, и обнаруживает, что сам является частью симуляции"
    
    final_story, scores = orchestrator.run_experiment(topic)
    
    print("\n" + "="*60)
    print("ФИНАЛЬНЫЙ РАССКАЗ (первые 600 символов)")
    print("="*60)
    print(final_story[:600] + "...")
    print("="*60)

if __name__ == "__main__":
    main()