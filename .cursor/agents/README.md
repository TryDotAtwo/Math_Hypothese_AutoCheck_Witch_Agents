# Subagents для мультимодельного анализа гипотез

Запуск параллельного анализа гипотезы H-001:

```
Запусти в параллель analyzer-claude, analyzer-gpt, analyzer-gemini, analyzer-composer, analyzer-grok, analyzer-kimi, analyzer-codex.

Каждый должен прочитать docs/hypotheses/H-001_произведение_собственных_значений_XXX_цепочки.md и связанные карточки,
заполнить сводку по docs/reports/_template.md и сохранить в docs/reports/H-001_{своё_имя}.md
```

**Важно:** Включи Max Mode и Multiple models в селекторе Composer, чтобы каждый агент использовал свою frontier-модель.
