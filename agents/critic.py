from typing import Dict, Optional, List
import re
from llm.gigachat_client import GigaChatClient

class CriticAgent:
    """Жесткий критик — ставит реальные оценки и аргументирует"""
    
    def __init__(self, model: Optional[str] = None):
        self.llm = GigaChatClient(model=model)
    
    def analyze(self, draft: str) -> tuple[str, Dict]:
        """Анализирует рассказ и возвращает критику с оценками"""
        
        prompt = f"""
Ты — самый строгий литературный критик в мире. Ты ненавидишь клише, штампы и ИИ-стиль. Ты работаешь на уровне профессионального редактора.

## ТВОИ ПРАВИЛА:

### 1. Ты не ставишь выше 7.0
- 10/10 — это Пушкин, Набоков, Пелевин
- 9/10 — это отличный современный писатель
- 8/10 — это хороший текст, но есть проблемы
- 7/10 — это читабельно, но много недостатков
- 6/10 — это слабо, много штампов
- 5/10 — это нечитаемо

### 2. Ты ищешь слабые места
- Клише ("сердце города", "ледяной озноб")
- Штампы ("цифровой мир", "виртуальная реальность")
- Повторы ("цифровой", "корпоративный", "виртуальный" — если больше 3 раз)
- Философские объяснения в лоб
- Слабые диалоги
- Воду и абстракции

### 3. Ты сравниваешь с эталоном
- Филип К. Дик — 10/10 (глубина, идеи)
- Виктор Пелевин — 9.5/10 (стиль, ирония)
- Уильям Гибсон — 9/10 (атмосфера, язык)
- Хороший киберпанк-рассказ — 7.5/10

### 4. Ты обосновываешь каждую оценку
- Почему стилистика 6, а не 8?
- Какие конкретные клише ты нашел?
- Какие предложения нужно удалить?

## РАССКАЗ ДЛЯ АНАЛИЗА:

{draft}

## ФОРМАТ ОТВЕТА:

**ОЦЕНКИ (строго, с обоснованием):**

1. **Стилистика: X/10**
   - Что хорошо: ...
   - Что плохо: ...
   - Конкретные примеры: ...

2. **Плотность: X/10**
   - Что хорошо: ...
   - Что плохо: ...
   - Конкретные примеры: ...

3. **Глубина: X/10**
   - Что хорошо: ...
   - Что плохо: ...
   - Конкретные примеры: ...

4. **Архитектура: X/10**
   - Что хорошо: ...
   - Что плохо: ...
   - Конкретные примеры: ...

5. **Оригинальность: X/10**
   - Что хорошо: ...
   - Что плохо: ...
   - Конкретные примеры: ...

**ИТОГОВАЯ ОЦЕНКА: X/10**

**ГЛАВНЫЕ ПРОБЛЕМЫ:**
1. ...
2. ...

**КОНКРЕТНЫЕ ПРАВКИ:**
1. ...
2. ...
"""
        
        print("Критик анализирует рассказ...")
        critique = self.llm.generate(prompt, temperature=0.3)
        scores = self._parse_scores(critique)
        return critique, scores
    
    def _parse_scores(self, critique: str) -> Dict:
        """Парсит оценки из текста критики"""
        scores = {}
        
        try:
            lines = critique.split('\n')
            
            # Ищем итоговую оценку
            for line in lines:
                if 'ИТОГОВАЯ ОЦЕНКА:' in line or 'Итоговая оценка:' in line:
                    match = re.search(r'(\d+(?:\.\d+)?)', line)
                    if match:
                        scores['total'] = float(match.group(1))
                        break
            
            # Ищем отдельные критерии
            criteria = {
                'Стилистика': 'style',
                'Плотность': 'density',
                'Глубина': 'depth',
                'Архитектура': 'structure',
                'Оригинальность': 'originality'
            }
            
            for line in lines:
                for crit_name, key in criteria.items():
                    if f'{crit_name}:' in line or f'{crit_name}:' in line:
                        match = re.search(r'(\d+(?:\.\d+)?)', line)
                        if match:
                            scores[key] = float(match.group(1))
            
            # Если нет total, ставим среднее
            if 'total' not in scores and scores:
                scores['total'] = sum(scores.values()) / len(scores)
            elif 'total' not in scores:
                scores['total'] = 5.0
                
        except Exception as e:
            print(f"Ошибка при парсинге оценок: {e}")
            scores['total'] = 5.0
        
        return scores
    
    def is_ready(self, critique: str, scores: Dict) -> bool:
        """Проверяет, готов ли рассказ к финалу"""
        total = scores.get('total', 0)
        
        # Жесткий критик считает готовым только текст с оценкой >= 8.0
        if total >= 8.0:
            return True
        
        # Проверяем критические замечания
        critical_words = ['переписать', 'кардинально', 'нечитаемо', 'провал', 'слишком слабо']
        if any(word in critique.lower() for word in critical_words):
            return False
        
        return False