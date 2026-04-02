#!/usr/bin/env python3
"""
TECSA Meeting Minutes PDF Generator
Gera atas de reunião em PDF seguindo o manual de identidade visual da TECSA.

Uso:
    python3 generate_minutes_pdf.py --data dados_ata.json --output ata.pdf --logo logo_tecsa_color.png

Dependências:
    pip3 install weasyprint
"""

import argparse
import json
import os
import sys
import base64


def load_logo_base64(logo_path: str) -> str:
    """Carrega o logotipo e converte para base64."""
    with open(logo_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")


def generate_html(data: dict, logo_base64: str) -> str:
    """Gera o HTML completo da ata de reunião."""

    meeting_number = data.get("meeting_number", "001/2026")
    meeting_type = data.get("meeting_type", "Reunião Geral")
    date = data.get("date", "")
    start_time = data.get("start_time", "")
    end_time = data.get("end_time", "")
    location = data.get("location", "Não informado")
    project = data.get("project", "")
    called_by = data.get("called_by", None)
    participants = data.get("participants", [])
    agenda = data.get("agenda", [])
    discussions = data.get("discussions", [])
    actions = data.get("actions", [])
    next_meeting = data.get("next_meeting", None)
    redactor = data.get("redactor", None)
    coordinator = data.get("coordinator", None)

    # Build time string
    time_str = start_time
    if end_time:
        time_str += f" às {end_time}"

    # Build participants table
    participants_html = build_participants_table(participants)

    # Build agenda list
    agenda_html = build_agenda_list(agenda)

    # Build discussions
    discussions_html = build_discussions(discussions)

    # Build actions table
    actions_html = build_actions_table(actions)

    # Build next meeting section
    next_meeting_html = build_next_meeting(next_meeting)

    # Build signatures
    signatures_html = build_signatures(redactor, coordinator)

    # Build meeting info fields
    called_by_html = ""
    if called_by:
        called_by_html = f"""
        <div class="info-row">
            <span class="info-label">Convocada por:</span>
            <span class="info-value">{called_by.get('name', '')} — {called_by.get('role', '')}</span>
        </div>"""

    project_html = ""
    if project:
        project_html = f"""
        <div class="info-row">
            <span class="info-label">Projeto/Obra:</span>
            <span class="info-value">{project}</span>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Ata de Reunião - TECSA</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

        :root {{
            --tecsa-blue: #003C82;
            --tecsa-blue-light: #E6EDF5;
            --tecsa-blue-medium: #1A5A9E;
            --tecsa-gray: #8A8C8E;
            --tecsa-gray-light: #F5F5F5;
            --tecsa-gray-medium: #D0D0D0;
            --tecsa-black: #231F20;
            --tecsa-white: #FFFFFF;
            --font-family: 'Montserrat', 'Helvetica Neue', Arial, sans-serif;
        }}

        @page {{
            size: A4;
            margin: 25mm 20mm 25mm 20mm;

            @top-left {{
                content: element(header-content);
            }}

            @bottom-left {{
                content: "TECSA — Confidencial";
                font-family: var(--font-family);
                font-size: 8pt;
                color: var(--tecsa-gray);
                border-top: 0.5pt solid var(--tecsa-gray-medium);
                padding-top: 5mm;
            }}

            @bottom-right {{
                content: "Página " counter(page) " de " counter(pages);
                font-family: var(--font-family);
                font-size: 8pt;
                color: var(--tecsa-gray);
                border-top: 0.5pt solid var(--tecsa-gray-medium);
                padding-top: 5mm;
            }}
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: var(--font-family);
            font-size: 11pt;
            line-height: 1.5;
            color: var(--tecsa-black);
            text-align: justify;
        }}

        /* Running Header */
        .header-content {{
            position: running(header-content);
            display: flex;
            align-items: center;
            border-bottom: 0.5pt solid var(--tecsa-gray-medium);
            padding-bottom: 3mm;
            width: 100%;
        }}

        .header-logo {{
            height: 10mm;
            width: auto;
        }}

        /* Title Block */
        .title-block {{
            text-align: center;
            margin-bottom: 8mm;
            padding-bottom: 5mm;
            border-bottom: 2pt solid var(--tecsa-blue);
        }}

        .title-main {{
            font-size: 22pt;
            font-weight: 700;
            color: var(--tecsa-blue);
            letter-spacing: 2pt;
            margin-bottom: 3mm;
        }}

        .title-number {{
            font-size: 14pt;
            font-weight: 600;
            color: var(--tecsa-blue);
            margin-bottom: 2mm;
        }}

        .title-type {{
            font-size: 12pt;
            font-weight: 600;
            color: var(--tecsa-gray);
            text-transform: uppercase;
            letter-spacing: 1pt;
        }}

        /* Meeting Info */
        .meeting-info {{
            background: var(--tecsa-gray-light);
            border-left: 3pt solid var(--tecsa-blue);
            padding: 5mm 6mm;
            margin-bottom: 8mm;
        }}

        .info-row {{
            display: flex;
            margin-bottom: 2mm;
            font-size: 10pt;
        }}

        .info-label {{
            font-weight: 600;
            color: var(--tecsa-blue);
            min-width: 35mm;
            flex-shrink: 0;
        }}

        .info-value {{
            color: var(--tecsa-black);
        }}

        /* Section Titles */
        .section-title {{
            font-size: 14pt;
            font-weight: 700;
            color: var(--tecsa-blue);
            margin-top: 8mm;
            margin-bottom: 4mm;
            padding-bottom: 2mm;
            border-bottom: 1pt solid var(--tecsa-blue);
            text-transform: uppercase;
            letter-spacing: 0.5pt;
            page-break-after: avoid;
        }}

        .section-number {{
            color: var(--tecsa-blue);
            margin-right: 3mm;
        }}

        /* Tables */
        .table-container {{
            margin: 4mm 0 6mm 0;
            page-break-inside: avoid;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 10pt;
        }}

        thead th {{
            background-color: var(--tecsa-blue);
            color: var(--tecsa-white);
            font-weight: 600;
            padding: 3mm 4mm;
            text-align: left;
            border: none;
        }}

        tbody td {{
            padding: 2.5mm 4mm;
            border-bottom: 0.3pt solid var(--tecsa-gray-medium);
            color: var(--tecsa-black);
            vertical-align: top;
        }}

        tbody tr:nth-child(even) {{
            background-color: var(--tecsa-blue-light);
        }}

        /* Presence indicator */
        .present {{
            color: #2E7D32;
            font-weight: 600;
        }}

        .absent {{
            color: #C62828;
            font-weight: 600;
        }}

        /* Agenda */
        .agenda-list {{
            margin: 3mm 0 3mm 0;
            padding: 0;
            list-style: none;
            counter-reset: agenda-counter;
        }}

        .agenda-item {{
            counter-increment: agenda-counter;
            padding: 2.5mm 4mm 2.5mm 0;
            border-bottom: 0.3pt dotted var(--tecsa-gray-medium);
            font-size: 11pt;
            display: flex;
            align-items: baseline;
        }}

        .agenda-item::before {{
            content: counter(agenda-counter) ".";
            font-weight: 700;
            color: var(--tecsa-blue);
            min-width: 8mm;
            flex-shrink: 0;
        }}

        /* Discussions */
        .discussion-block {{
            margin-bottom: 6mm;
            page-break-inside: avoid;
        }}

        .discussion-title {{
            font-size: 12pt;
            font-weight: 600;
            color: var(--tecsa-blue);
            margin-bottom: 2mm;
        }}

        .discussion-item-number {{
            font-weight: 700;
            color: var(--tecsa-blue);
            margin-right: 2mm;
        }}

        .discussion-subsection {{
            margin-bottom: 3mm;
        }}

        .discussion-label {{
            font-size: 10pt;
            font-weight: 600;
            color: var(--tecsa-gray);
            text-transform: uppercase;
            letter-spacing: 0.3pt;
            margin-bottom: 1mm;
        }}

        .decision-box {{
            background: var(--tecsa-blue-light);
            border-left: 2.5pt solid var(--tecsa-blue);
            padding: 3mm 5mm;
            margin: 2mm 0 3mm 0;
            font-size: 10.5pt;
        }}

        .decision-box .discussion-label {{
            color: var(--tecsa-blue);
            font-weight: 700;
        }}

        /* Next Meeting */
        .next-meeting-box {{
            background: var(--tecsa-gray-light);
            border: 0.5pt solid var(--tecsa-gray-medium);
            padding: 4mm 5mm;
            margin: 4mm 0;
        }}

        /* Signatures */
        .signatures {{
            margin-top: 15mm;
            page-break-inside: avoid;
        }}

        .closing-text {{
            text-align: center;
            font-size: 11pt;
            color: var(--tecsa-black);
            margin-bottom: 15mm;
            font-style: italic;
        }}

        .signature-row {{
            display: flex;
            justify-content: space-around;
            gap: 20mm;
        }}

        .signature-block {{
            text-align: center;
            flex: 1;
        }}

        .signature-line {{
            border-top: 0.5pt solid var(--tecsa-black);
            margin-top: 20mm;
            padding-top: 2mm;
        }}

        .signature-name {{
            font-weight: 600;
            font-size: 10pt;
            color: var(--tecsa-black);
        }}

        .signature-role {{
            font-size: 9pt;
            color: var(--tecsa-gray);
        }}

        /* Paragraphs */
        p {{
            margin-bottom: 3mm;
            text-align: justify;
            orphans: 3;
            widows: 3;
        }}

        /* Status badges */
        .status-pendente {{
            background: #FFF3E0;
            color: #E65100;
            padding: 1mm 3mm;
            font-size: 8pt;
            font-weight: 600;
            border-radius: 2pt;
        }}

        .status-concluido {{
            background: #E8F5E9;
            color: #2E7D32;
            padding: 1mm 3mm;
            font-size: 8pt;
            font-weight: 600;
            border-radius: 2pt;
        }}

        .status-andamento {{
            background: #E3F2FD;
            color: #1565C0;
            padding: 1mm 3mm;
            font-size: 8pt;
            font-weight: 600;
            border-radius: 2pt;
        }}
    </style>
</head>
<body>

    <!-- Running Header -->
    <div class="header-content">
        <img src="data:image/png;base64,{logo_base64}" class="header-logo" alt="TECSA">
    </div>

    <!-- TITLE BLOCK -->
    <div class="title-block">
        <div class="title-main">ATA DE REUNIÃO</div>
        <div class="title-number">ATA Nº {meeting_number}</div>
        <div class="title-type">{meeting_type}</div>
    </div>

    <!-- MEETING INFO -->
    <div class="meeting-info">
        <div class="info-row">
            <span class="info-label">Data:</span>
            <span class="info-value">{date}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Horário:</span>
            <span class="info-value">{time_str}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Local:</span>
            <span class="info-value">{location}</span>
        </div>
        {project_html}
        {called_by_html}
    </div>

    <!-- PARTICIPANTS -->
    <div class="section-title"><span class="section-number">1.</span> Participantes</div>
    {participants_html}

    <!-- AGENDA -->
    <div class="section-title"><span class="section-number">2.</span> Pauta / Ordem do Dia</div>
    {agenda_html}

    <!-- DISCUSSIONS -->
    <div class="section-title"><span class="section-number">3.</span> Desenvolvimento e Deliberações</div>
    {discussions_html}

    <!-- ACTIONS -->
    <div class="section-title"><span class="section-number">4.</span> Ações Definidas</div>
    {actions_html}

    <!-- NEXT MEETING -->
    {next_meeting_html}

    <!-- SIGNATURES -->
    {signatures_html}

</body>
</html>"""

    return html


def build_participants_table(participants: list) -> str:
    """Constrói a tabela de participantes."""
    if not participants:
        return "<p>Nenhum participante registrado.</p>"

    html = """<div class="table-container">
<table>
  <thead><tr>
    <th>Nome</th>
    <th>Cargo / Função</th>
    <th>Empresa</th>
    <th>Presença</th>
  </tr></thead>
  <tbody>
"""
    for p in participants:
        name = p.get("name", "")
        role = p.get("role", "")
        company = p.get("company", "TECSA")
        present = p.get("present", True)
        presence_class = "present" if present else "absent"
        presence_text = "Presente" if present else "Ausente"

        html += f"""    <tr>
      <td>{name}</td>
      <td>{role}</td>
      <td>{company}</td>
      <td><span class="{presence_class}">{presence_text}</span></td>
    </tr>
"""
    html += "  </tbody>\n</table>\n</div>\n"
    return html


def build_agenda_list(agenda: list) -> str:
    """Constrói a lista de pauta."""
    if not agenda:
        return "<p>Pauta não definida.</p>"

    html = '<ol class="agenda-list">\n'
    for item in agenda:
        html += f'  <li class="agenda-item"><span>{item}</span></li>\n'
    html += "</ol>\n"
    return html


def build_discussions(discussions: list) -> str:
    """Constrói as seções de deliberações."""
    if not discussions:
        return "<p>Nenhuma deliberação registrada.</p>"

    html = ""
    for disc in discussions:
        item_num = disc.get("agenda_item", "")
        title = disc.get("title", "")
        summary = disc.get("summary", "")
        positions = disc.get("positions", "")
        decision = disc.get("decision", "")

        html += f"""<div class="discussion-block">
    <div class="discussion-title">
        <span class="discussion-item-number">Item {item_num}.</span> {title}
    </div>
"""
        if summary:
            html += '    <div class="discussion-subsection">\n'
            html += '        <div class="discussion-label">Resumo da Discussão</div>\n'
            paragraphs = summary.split("\n\n") if "\n\n" in summary else [summary]
            for p in paragraphs:
                p = p.strip()
                if p:
                    html += f"        <p>{p}</p>\n"
            html += "    </div>\n"

        if positions:
            html += '    <div class="discussion-subsection">\n'
            html += '        <div class="discussion-label">Posicionamentos</div>\n'
            paragraphs = positions.split("\n\n") if "\n\n" in positions else [positions]
            for p in paragraphs:
                p = p.strip()
                if p:
                    html += f"        <p>{p}</p>\n"
            html += "    </div>\n"

        if decision:
            html += '    <div class="decision-box">\n'
            html += '        <div class="discussion-label">Deliberação</div>\n'
            html += f"        <p>{decision}</p>\n"
            html += "    </div>\n"

        html += "</div>\n"

    return html


def build_actions_table(actions: list) -> str:
    """Constrói a tabela de ações."""
    if not actions:
        return "<p>Nenhuma ação definida nesta reunião.</p>"

    html = """<div class="table-container">
<table>
  <thead><tr>
    <th>Nº</th>
    <th>Ação</th>
    <th>Responsável</th>
    <th>Prazo</th>
    <th>Status</th>
  </tr></thead>
  <tbody>
"""
    for action in actions:
        num = action.get("number", "")
        desc = action.get("description", "")
        responsible = action.get("responsible", "")
        deadline = action.get("deadline", "A definir")
        status = action.get("status", "Pendente")

        status_lower = status.lower().replace("í", "i")
        if "pendente" in status_lower:
            status_class = "status-pendente"
        elif "conclu" in status_lower:
            status_class = "status-concluido"
        else:
            status_class = "status-andamento"

        html += f"""    <tr>
      <td>{num}</td>
      <td>{desc}</td>
      <td>{responsible}</td>
      <td>{deadline}</td>
      <td><span class="{status_class}">{status}</span></td>
    </tr>
"""
    html += "  </tbody>\n</table>\n</div>\n"
    return html


def build_next_meeting(next_meeting: dict) -> str:
    """Constrói a seção de próxima reunião."""
    if not next_meeting:
        return ""

    html = '<div class="section-title"><span class="section-number">5.</span> Próxima Reunião</div>\n'
    html += '<div class="next-meeting-box">\n'

    if next_meeting.get("date"):
        html += f'    <div class="info-row"><span class="info-label">Data:</span><span class="info-value">{next_meeting["date"]}</span></div>\n'
    if next_meeting.get("time"):
        html += f'    <div class="info-row"><span class="info-label">Horário:</span><span class="info-value">{next_meeting["time"]}</span></div>\n'
    if next_meeting.get("location"):
        html += f'    <div class="info-row"><span class="info-label">Local:</span><span class="info-value">{next_meeting["location"]}</span></div>\n'
    if next_meeting.get("preliminary_agenda"):
        html += f'    <div class="info-row"><span class="info-label">Pauta preliminar:</span><span class="info-value">{next_meeting["preliminary_agenda"]}</span></div>\n'

    html += "</div>\n"
    return html


def build_signatures(redactor: dict, coordinator: dict) -> str:
    """Constrói a seção de assinaturas."""
    html = '<div class="signatures">\n'
    html += '    <div class="closing-text">Nada mais havendo a tratar, a reunião foi encerrada, sendo lavrada a presente ata que, após lida e aprovada, será assinada pelos presentes.</div>\n'
    html += '    <div class="signature-row">\n'

    if redactor:
        html += '        <div class="signature-block">\n'
        html += '            <div class="signature-line"></div>\n'
        html += f'            <div class="signature-name">{redactor.get("name", "")}</div>\n'
        html += f'            <div class="signature-role">{redactor.get("role", "")} — Redator(a)</div>\n'
        html += "        </div>\n"
    else:
        html += '        <div class="signature-block">\n'
        html += '            <div class="signature-line"></div>\n'
        html += '            <div class="signature-name">_________________________</div>\n'
        html += '            <div class="signature-role">Redator(a)</div>\n'
        html += "        </div>\n"

    if coordinator:
        html += '        <div class="signature-block">\n'
        html += '            <div class="signature-line"></div>\n'
        html += f'            <div class="signature-name">{coordinator.get("name", "")}</div>\n'
        html += f'            <div class="signature-role">{coordinator.get("role", "")} — Coordenador(a)</div>\n'
        html += "        </div>\n"
    else:
        html += '        <div class="signature-block">\n'
        html += '            <div class="signature-line"></div>\n'
        html += '            <div class="signature-name">_________________________</div>\n'
        html += '            <div class="signature-role">Coordenador(a)</div>\n'
        html += "        </div>\n"

    html += "    </div>\n"
    html += "</div>\n"
    return html


def generate_pdf(html_content: str, output_path: str):
    """Gera o PDF a partir do HTML usando WeasyPrint."""
    from weasyprint import HTML

    HTML(string=html_content).write_pdf(output_path)
    print(f"Ata gerada com sucesso: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Gerador de Atas de Reunião TECSA"
    )
    parser.add_argument(
        "--data", required=True, help="Caminho para o arquivo JSON com os dados da ata"
    )
    parser.add_argument(
        "--output", required=True, help="Caminho para o arquivo PDF de saída"
    )
    parser.add_argument(
        "--logo", required=True, help="Caminho para o arquivo PNG do logotipo TECSA"
    )
    parser.add_argument(
        "--html-only", action="store_true", help="Gerar apenas o HTML (sem converter para PDF)"
    )

    args = parser.parse_args()

    if not os.path.exists(args.data):
        print(f"Erro: Arquivo de dados não encontrado: {args.data}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.logo):
        print(f"Erro: Logotipo não encontrado: {args.logo}", file=sys.stderr)
        sys.exit(1)

    with open(args.data, "r", encoding="utf-8") as f:
        data = json.load(f)

    logo_base64 = load_logo_base64(args.logo)
    html_content = generate_html(data, logo_base64)

    if args.html_only:
        html_output = args.output.replace(".pdf", ".html")
        with open(html_output, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"HTML gerado: {html_output}")
    else:
        generate_pdf(html_content, args.output)


if __name__ == "__main__":
    main()
