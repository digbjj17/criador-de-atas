---
name: tecsa-meeting-minutes
description: Gera atas de reunião padronizadas para a TECSA a partir de áudio gravado pelo Plaud ou outro gravador. A skill transcreve o áudio automaticamente, extrai informações-chave (participantes, pauta, deliberações, ações) e gera um PDF profissional seguindo o manual de identidade visual da TECSA. Use esta skill sempre que o usuário pedir para criar atas de reunião, transcrever reuniões, gerar atas a partir de áudio, documentar reuniões, ou mencionar "ata TECSA", "ata de reunião", "transcrever reunião", "áudio da reunião", "gravação do Plaud", "minuta de reunião", ou qualquer variação que envolva transformar gravações de reunião em documentos formais da TECSA.
---

# Skill de Atas de Reunião TECSA

Esta skill transforma gravações de áudio de reuniões (Plaud ou outros gravadores) em atas formais em PDF, seguindo rigorosamente o manual de identidade visual da TECSA.

## Fluxo de Trabalho

O processo completo tem três etapas: transcrição do áudio, extração inteligente de informações e geração do PDF formatado. Cada etapa é detalhada abaixo.

```
Áudio (.mp3/.wav/.m4a/.webm)
    │
    ▼
Transcrição automática (manus-speech-to-text)
    │
    ▼
Extração inteligente via LLM (OpenAI API)
    │
    ▼
JSON estruturado com dados da ata
    │
    ▼
PDF formatado com identidade visual TECSA
```

## Identidade Visual TECSA — Diretrizes Obrigatórias

Estas diretrizes são extraídas diretamente do Manual de Identidade Visual da TECSA e devem ser seguidas sem exceção. Para detalhes completos, consulte `references/identidade_visual.md`.

### Cores Oficiais

| Elemento | HEX | RGB | Uso |
|----------|-----|-----|-----|
| Azul Escuro TECSA | #003C82 | rgb(0, 60, 130) | Cor primária: títulos, cabeçalhos, destaques |
| Cinza TECSA | #8A8C8E | rgb(138, 140, 142) | Cor secundária: subtítulos, linhas, elementos de apoio |
| Preto TECSA | #231F20 | rgb(35, 31, 32) | Texto corrido do corpo |
| Branco | #FFFFFF | rgb(255, 255, 255) | Fundos, texto sobre fundo escuro |

### Tipografia

Fonte substituta **Montserrat** (Google Fonts, sans-serif), que possui características visuais muito semelhantes à Proxima Nova oficial da TECSA:

| Elemento | Fonte | Peso | Tamanho |
|----------|-------|------|---------|
| Título "ATA DE REUNIÃO" | Montserrat | Bold (700) | 22pt |
| Dados da reunião (tipo, data, local) | Montserrat | SemiBold (600) | 12pt |
| Títulos de seção | Montserrat | Bold (700) | 14pt |
| Corpo do texto | Montserrat | Regular (400) | 11pt |
| Cabeçalho/Rodapé | Montserrat | Regular (400) | 8pt |
| Tabelas | Montserrat | Regular (400) | 10pt |

### Logotipo

O logotipo da TECSA está disponível em `assets/logo_tecsa_color.png`. Regras de uso:

- Sempre usar a versão completa (símbolo + nome) no cabeçalho
- Respeitar a área de respiro ao redor do logotipo
- Nunca distorcer, alterar cores ou adicionar efeitos

## Estrutura da Ata de Reunião

Toda ata TECSA segue esta estrutura padronizada:

### 1. Cabeçalho Institucional
- Logotipo TECSA no topo
- Título "ATA DE REUNIÃO" em destaque
- Número da ata (formato: ATA Nº XXX/AAAA)
- Tipo de reunião (Diretoria, Projeto/Obra, Técnica, Comercial, Geral)

### 2. Dados da Reunião
- Data e horário (início e término)
- Local (presencial ou remoto)
- Projeto/Obra relacionado (se aplicável)
- Convocada por (nome e cargo)

### 3. Participantes
Tabela com: Nome, Cargo/Função, Empresa (se externo), Presença (Presente/Ausente)

### 4. Pauta / Ordem do Dia
Lista numerada dos tópicos previstos para discussão.

### 5. Desenvolvimento / Deliberações
Para cada item da pauta:
- Resumo da discussão
- Posicionamentos relevantes
- Decisão ou deliberação tomada

### 6. Ações Definidas
Tabela com: Nº, Ação, Responsável, Prazo, Status

### 7. Próxima Reunião
- Data e horário previstos
- Local
- Pauta preliminar (se definida)

### 8. Encerramento e Assinaturas
- Texto de encerramento padrão
- Espaço para assinatura do redator e do presidente/coordenador da reunião

## Como Gerar uma Ata

### Passo 1: Receber o Áudio

O usuário fornece o arquivo de áudio da reunião gravado pelo Plaud (ou outro dispositivo). Formatos aceitos: `.mp3`, `.wav`, `.m4a`, `.webm`.

### Passo 2: Transcrever o Áudio

Use o utilitário de transcrição disponível no sandbox:

```bash
manus-speech-to-text <caminho-do-audio>
```

Isso gera a transcrição completa em texto. Salve o resultado em um arquivo `.txt`.

### Passo 3: Extrair Informações com LLM

Execute o script de extração que usa a API OpenAI para analisar a transcrição e estruturar os dados da ata:

```bash
python3 <skill-path>/scripts/extract_meeting_data.py \
  --transcript <caminho-transcricao.txt> \
  --output <caminho-dados.json>
```

O script envia a transcrição para o LLM com um prompt especializado que identifica participantes, pauta, deliberações, ações e demais campos da ata. O resultado é um JSON estruturado.

### Passo 4: Complementar Informações

Após a extração automática, pergunte ao usuário se deseja complementar ou corrigir:
- Número da ata (se não informado, sugerir sequencial)
- Lista de participantes com cargos formais
- Tipo de reunião
- Qualquer informação que o áudio não tenha captado claramente

Atualize o JSON com as correções do usuário.

### Passo 5: Gerar o PDF

Execute o script de geração:

```bash
python3 <skill-path>/scripts/generate_minutes_pdf.py \
  --data <caminho-dados.json> \
  --output <caminho-saida.pdf> \
  --logo <skill-path>/assets/logo_tecsa_color.png
```

### Passo 6: Revisar e Entregar

Apresente o PDF ao usuário para revisão. Se necessário, ajuste o JSON e regere o PDF.

## Observações Importantes

- Todas as atas devem ser geradas em português brasileiro
- Formato A4 (210mm x 297mm)
- Margens: superior 25mm, inferior 25mm, esquerda 20mm, direita 20mm
- Rodapé padrão: "TECSA — Confidencial" à esquerda, "Página X de Y" à direita
- Cabeçalho: logotipo TECSA com linha separadora cinza
- O áudio pode conter ruídos ou trechos inaudíveis — marcar como "[trecho inaudível]" na transcrição
- Se o áudio for muito longo (> 2 horas), informar ao usuário que a transcrição pode levar mais tempo
