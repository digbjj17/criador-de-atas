#!/usr/bin/env python3
"""
TECSA Meeting Data Extractor
Extrai informações estruturadas de uma transcrição de reunião usando LLM.

Uso:
    python3 extract_meeting_data.py --transcript transcricao.txt --output dados_ata.json

Dependências:
    pip3 install openai
"""

import argparse
import json
import os
import sys
from datetime import datetime


def extract_meeting_data(transcript_text: str) -> dict:
    """Envia a transcrição ao LLM e extrai dados estruturados da reunião."""
    from openai import OpenAI

    client = OpenAI()

    system_prompt = """Você é um assistente especializado em extrair informações de transcrições de reuniões corporativas da empresa TECSA (construção civil e engenharia).

A partir da transcrição fornecida, extraia e estruture as seguintes informações em formato JSON:

1. **meeting_type**: Identifique o tipo de reunião. Opções: "Reunião de Diretoria", "Reunião de Projeto", "Reunião Técnica", "Reunião Comercial", "Reunião Geral". Se não for possível determinar, use "Reunião Geral".

2. **date**: Data da reunião por extenso (ex: "28 de março de 2026"). Se não mencionada, use a data de hoje.

3. **start_time**: Horário de início no formato HH:MM. Se não mencionado, deixe vazio.

4. **end_time**: Horário de término no formato HH:MM. Se não mencionado, deixe vazio.

5. **location**: Local da reunião (sala, endereço ou "Remoto/Online"). Se não mencionado, deixe "Não informado".

6. **project**: Nome do projeto ou obra relacionado. Se não aplicável, deixe vazio.

7. **called_by**: Objeto com "name" e "role" de quem convocou a reunião. Se não identificável, deixe null.

8. **participants**: Array de objetos com "name", "role" (cargo/função), "company" (empresa, usar "TECSA" para internos), "present" (true/false). Identifique todos os participantes mencionados na transcrição.

9. **agenda**: Array de strings com os tópicos discutidos na reunião, em ordem.

10. **discussions**: Array de objetos para cada item da pauta, contendo:
    - "agenda_item": número do item (inteiro)
    - "title": título do tópico
    - "summary": resumo objetivo da discussão (2-4 parágrafos)
    - "positions": posicionamentos relevantes dos participantes (quem disse o quê)
    - "decision": decisão ou deliberação tomada (se houver)

11. **actions**: Array de objetos com ações definidas:
    - "number": número sequencial
    - "description": descrição da ação
    - "responsible": nome do responsável
    - "deadline": prazo no formato DD/MM/AAAA (se mencionado, senão "A definir")
    - "status": "Pendente"

12. **next_meeting**: Objeto com "date", "time", "location", "preliminary_agenda". Se não definida, deixe null.

Regras importantes:
- Seja objetivo e profissional no resumo das discussões
- Capture todas as decisões tomadas, mesmo que informais
- Identifique ações mesmo quando não explicitamente atribuídas (infira o responsável pelo contexto)
- Se um trecho for inaudível ou confuso, marque como "[trecho inaudível]"
- Mantenha a linguagem formal e em português brasileiro
- Não invente informações que não estejam na transcrição

Retorne APENAS o JSON válido, sem markdown, sem explicações adicionais."""

    user_prompt = f"""Analise a seguinte transcrição de reunião e extraia as informações estruturadas conforme solicitado:

---
TRANSCRIÇÃO DA REUNIÃO:
---
{transcript_text}
---

Retorne o JSON estruturado com todos os campos solicitados."""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=8000,
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)
    return result


def validate_and_complete(data: dict) -> dict:
    """Valida e completa campos obrigatórios com valores padrão."""
    today = datetime.now()

    # Garantir campos obrigatórios
    if not data.get("meeting_type"):
        data["meeting_type"] = "Reunião Geral"

    if not data.get("date"):
        data["date"] = today.strftime("%d de %B de %Y").replace(
            "January", "janeiro"
        ).replace("February", "fevereiro").replace("March", "março").replace(
            "April", "abril"
        ).replace("May", "maio").replace("June", "junho").replace(
            "July", "julho"
        ).replace("August", "agosto").replace("September", "setembro").replace(
            "October", "outubro"
        ).replace("November", "novembro").replace("December", "dezembro")

    if not data.get("start_time"):
        data["start_time"] = ""

    if not data.get("end_time"):
        data["end_time"] = ""

    if not data.get("location"):
        data["location"] = "Não informado"

    if not data.get("project"):
        data["project"] = ""

    if not data.get("meeting_number"):
        data["meeting_number"] = f"001/{today.year}"

    if not data.get("participants"):
        data["participants"] = []

    if not data.get("agenda"):
        data["agenda"] = []

    if not data.get("discussions"):
        data["discussions"] = []

    if not data.get("actions"):
        data["actions"] = []

    # Numerar ações se não numeradas
    for i, action in enumerate(data["actions"], 1):
        if not action.get("number"):
            action["number"] = i
        if not action.get("status"):
            action["status"] = "Pendente"

    return data


def main():
    parser = argparse.ArgumentParser(
        description="Extrator de Dados de Reunião TECSA"
    )
    parser.add_argument(
        "--transcript",
        required=True,
        help="Caminho para o arquivo de transcrição (.txt)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Caminho para o arquivo JSON de saída",
    )

    args = parser.parse_args()

    if not os.path.exists(args.transcript):
        print(f"Erro: Arquivo de transcrição não encontrado: {args.transcript}", file=sys.stderr)
        sys.exit(1)

    # Ler transcrição
    with open(args.transcript, "r", encoding="utf-8") as f:
        transcript_text = f.read()

    if not transcript_text.strip():
        print("Erro: Arquivo de transcrição está vazio.", file=sys.stderr)
        sys.exit(1)

    print(f"Transcrição carregada: {len(transcript_text)} caracteres")
    print("Extraindo informações da reunião via LLM...")

    # Extrair dados
    meeting_data = extract_meeting_data(transcript_text)

    # Validar e completar
    meeting_data = validate_and_complete(meeting_data)

    # Salvar JSON
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(meeting_data, f, ensure_ascii=False, indent=2)

    print(f"Dados extraídos com sucesso: {args.output}")
    print(f"  - Participantes: {len(meeting_data.get('participants', []))}")
    print(f"  - Itens de pauta: {len(meeting_data.get('agenda', []))}")
    print(f"  - Deliberações: {len(meeting_data.get('discussions', []))}")
    print(f"  - Ações definidas: {len(meeting_data.get('actions', []))}")


if __name__ == "__main__":
    main()
