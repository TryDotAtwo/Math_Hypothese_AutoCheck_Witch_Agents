# Инструкции для агентов

## Мультимодельный анализ гипотез

При запросе «запусти мультимодельный анализ H-001» или «анализ всеми моделями»:

### Обязательные ограничения
- **ЧИТАТЬ** hypotheses, concepts, proofs, insights, dialogues — опора на имеющиеся карточки
- **ПИСАТЬ** только в `docs/reports/H-XXX_{model}.md` — свой отчёт
- **НЕ изменять** hypotheses, concepts, proofs, insights, dialogues, domains

### Как запустить
1. В Composer: включи **Max Mode** (переключатель в селекторе модели)
2. Включи **Multiple models** — выбери 6–8 frontier-моделей (Claude, GPT, Gemini, Composer, Grok, Kimi, Codex)
3. Промпт: «Запусти в параллель analyzer-claude, analyzer-gpt, analyzer-gemini, analyzer-composer, analyzer-grok, analyzer-kimi, analyzer-codex. Каждый анализирует H-001 и пишет только в docs/reports/H-001_{своё_имя}.md»

### Subagents
Конфигурация в `.cursor/agents/`. Правило: `.cursor/rules/multimodel-analysis.mdc`
