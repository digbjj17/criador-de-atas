# Schema do JSON de Dados da Ata de Reunião

O script `generate_minutes_pdf.py` recebe um arquivo JSON com a seguinte estrutura:

```json
{
  "meeting_number": "015/2026",
  "meeting_type": "Reunião de Projeto",
  "date": "28 de março de 2026",
  "start_time": "14:00",
  "end_time": "15:30",
  "location": "Sala de Reuniões 3 — Sede TECSA",
  "project": "Edifício Corporate Tower",
  "called_by": {
    "name": "Carlos Silva",
    "role": "Gerente de Projetos"
  },
  "participants": [
    {
      "name": "Carlos Silva",
      "role": "Gerente de Projetos",
      "company": "TECSA",
      "present": true
    },
    {
      "name": "Ana Martins",
      "role": "Engenheira Civil",
      "company": "TECSA",
      "present": true
    }
  ],
  "agenda": [
    "Atualização do cronograma da obra",
    "Revisão do orçamento do 2º trimestre",
    "Definição de fornecedores de estrutura metálica"
  ],
  "discussions": [
    {
      "agenda_item": 1,
      "title": "Atualização do cronograma da obra",
      "summary": "Texto resumindo a discussão sobre este item...",
      "positions": "Posicionamentos relevantes dos participantes...",
      "decision": "Decisão ou deliberação tomada..."
    }
  ],
  "actions": [
    {
      "number": 1,
      "description": "Solicitar cotação a três fornecedores alternativos",
      "responsible": "Ana Martins",
      "deadline": "04/04/2026",
      "status": "Pendente"
    }
  ],
  "next_meeting": {
    "date": "11 de abril de 2026",
    "time": "14:00",
    "location": "Sala de Reuniões 3 — Sede TECSA",
    "preliminary_agenda": "Avaliação das cotações recebidas"
  },
  "redactor": {
    "name": "Ana Martins",
    "role": "Engenheira Civil"
  },
  "coordinator": {
    "name": "Carlos Silva",
    "role": "Gerente de Projetos"
  }
}
```

## Campos Obrigatórios

| Campo | Tipo | Descrição |
|-------|------|-----------|
| meeting_type | string | Tipo: "Reunião de Diretoria", "Reunião de Projeto", "Reunião Técnica", "Reunião Comercial", "Reunião Geral" |
| date | string | Data da reunião por extenso |
| start_time | string | Horário de início (HH:MM) |
| location | string | Local da reunião |
| participants | array | Lista de participantes |
| agenda | array | Lista de itens da pauta |
| discussions | array | Deliberações por item da pauta |
| actions | array | Lista de ações definidas |

## Campos Opcionais

| Campo | Tipo | Descrição | Padrão |
|-------|------|-----------|--------|
| meeting_number | string | Número da ata (XXX/AAAA) | Gerado automaticamente |
| end_time | string | Horário de término | "" |
| project | string | Projeto/Obra relacionado | "" |
| called_by | object | Quem convocou a reunião | null |
| next_meeting | object | Dados da próxima reunião | null |
| redactor | object | Redator da ata | null |
| coordinator | object | Coordenador/Presidente da reunião | null |
