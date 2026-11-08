python3 resumo_pdf.py "Direito Administrativo Aula 1.pdf" --disciplina "Direito Administrativo" --aula 1from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                PageBreak, Table, TableStyle, KeepTogether, HRFlowable)

GREY = colors.Color(0.92, 0.92, 0.92)
DARK = colors.black
H = "Helvetica"; HB = "Helvetica-Bold"; HI = "Helvetica-Oblique"

st = {
 'cover_d': ParagraphStyle('cd', fontName=HB, fontSize=14, alignment=TA_CENTER, leading=18),
 'cover_a': ParagraphStyle('ca', fontName=HB, fontSize=26, alignment=TA_CENTER, leading=32),
 'cover_n': ParagraphStyle('cn', fontName=HB, fontSize=18, alignment=TA_CENTER, leading=24),
 'cover_s': ParagraphStyle('cs', fontName=H, fontSize=11, alignment=TA_CENTER, leading=15),
 'slide': ParagraphStyle('sl', fontName=HB, fontSize=12.5, leading=16, spaceBefore=12, spaceAfter=4),
 'body': ParagraphStyle('b', fontName=H, fontSize=10.5, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=4),
 'box': ParagraphStyle('bx', fontName=H, fontSize=10, leading=13.5, alignment=TA_JUSTIFY),
 'h1': ParagraphStyle('h1', fontName=HB, fontSize=16, leading=20, spaceAfter=8),
 'bul': ParagraphStyle('bu', fontName=H, fontSize=10.5, leading=14.5, leftIndent=14, bulletIndent=2, spaceAfter=3, alignment=TA_JUSTIFY),
 'note': ParagraphStyle('nt', fontName=HI, fontSize=9.5, leading=13, alignment=TA_JUSTIFY),
}

def box(label, items):
    rows = []
    for it in items:
        rows.append([Paragraph(f"<b>{label}:</b> {it}", st['box'])])
    t = Table(rows, colWidths=[16.6*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),GREY),
        ('LINEBEFORE',(0,0),(0,-1),2.5,DARK),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    return [t, Spacer(1,3)]

def build(fname, num, nome, subtitulo, slides, revisao, obs=None):
    def footer(c, d):
        c.saveState(); c.setFont(H, 8.5)
        c.drawString(2*cm, 1.2*cm, f"Direito Civil - Contratos | Aula {num} - {nome}")
        c.drawRightString(A4[0]-2*cm, 1.2*cm, f"Página {d.page}")
        c.restoreState()
    doc = BaseDocTemplate(fname, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                          topMargin=2*cm, bottomMargin=2*cm,
                          title=f"Resumo - Aula {num} - {nome}", author="Resumo de aula")
    fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')
    doc.addPageTemplates([PageTemplate(id='p', frames=[fr], onPage=footer)])
    s = []
    # capa
    s += [Spacer(1, 6*cm), Paragraph("DISCIPLINA: DIREITO CIVIL - CONTRATOS", st['cover_d']),
          Spacer(1, 1*cm), HRFlowable(width="60%", thickness=1.2, color=DARK, hAlign='CENTER'),
          Spacer(1, 1*cm), Paragraph(f"AULA {num}", st['cover_a']), Spacer(1, 0.5*cm),
          Paragraph(nome, st['cover_n']), Spacer(1, 1*cm),
          HRFlowable(width="60%", thickness=1.2, color=DARK, hAlign='CENTER'), Spacer(1, 1*cm),
          Paragraph(subtitulo, st['cover_s']), Paragraph(f"Professor: Roberto Pinto", st['cover_s']),
          PageBreak()]
    s.append(Paragraph("Resumo slide a slide", st['h1']))
    s.append(Paragraph("Cada slide da aula foi resumido separadamente, na ordem em que aparece. Os quadros cinza destacam conceitos, exemplos e artigos de lei.", st['body']))
    if obs:
        s.append(Paragraph(obs, st['note']))
    for sl in slides:
        blk = [Paragraph(f"Slide {sl['n']} - {sl['t']}", st['slide'])]
        for p in sl.get('body', []):
            blk.append(Paragraph(p, st['body']))
        parts = []
        if sl.get('key'): parts += box("Conceito", sl['key'])
        if sl.get('ex'): parts += box("Exemplo", sl['ex'])
        if sl.get('lei'): parts += box("Base legal", sl['lei'])
        if sl.get('nota'): parts += box("Atenção", sl['nota'])
        s += [KeepTogether(blk[:2])] + blk[2:] + parts
    s.append(PageBreak())
    s.append(Paragraph("Revisão final - pontos mais importantes", st['h1']))
    for r in revisao:
        s.append(Paragraph(r, st['bul'], bulletText='•'))
    doc.build(s)
