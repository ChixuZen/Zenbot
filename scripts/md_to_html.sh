#!/bin/bash

echo "🔄 Convertendo Markdown para HTML..."

TEMPLATE="docs/template.html"

find docs -name "*.md" | while read file; do
  out="${file%.md}.html"

  echo "➡️  $file → $out"

  pandoc "$file" \
    --template="$TEMPLATE" \
    --metadata title="ZenBot Docs" \
    -s \
    -o "$out"
done

echo "✅ Conversão concluída!"