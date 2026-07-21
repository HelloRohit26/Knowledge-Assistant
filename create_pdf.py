import os
import sys
import xml.sax.saxutils as saxutils
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress headers/footers on cover page

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Running Header
        self.drawString(54, 755, "KNOWLEDGE ASSISTANT — PROJECT CODEBASE & STRUCTURE DOCUMENTATION")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 747, 558, 747)

        # Running Footer
        self.line(54, 45, 558, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Confidential — Knowledge Assistant Project Report")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.restoreState()

def build_tree_lines(startpath, ignore_dirs):
    tree_lines = []
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        dirs.sort()
        files.sort()
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level)
        basename = os.path.basename(root)
        if level == 0:
            tree_lines.append(f"[DIR]  {basename}/")
        else:
            tree_lines.append(f"{indent}├── [DIR]  {basename}/")
        
        subindent = '│   ' * (level + 1)
        for f in files:
            if not f.endswith(('.pyc', '.db', '.sqlite3', '.png', '.jpg', '.ico', '.pdf', '.zip', '.tar')):
                tree_lines.append(f"{subindent}├── [FILE] {f}")
    return tree_lines

def escape_text(text):
    return saxutils.escape(text)

def get_code_paragraphs(content, style_code, max_lines_per_block=40):
    lines = content.splitlines()
    if not lines:
        lines = ["# (Empty file)"]
        
    formatted_lines = []
    for idx, line in enumerate(lines, 1):
        clean_line = line.replace('\t', '    ')
        escaped = escape_text(clean_line)
        escaped_spaces = escaped.replace(' ', '&nbsp;')
        line_str = f'<font color="#94A3B8">{idx:4d} │ </font>{escaped_spaces}'
        formatted_lines.append(line_str)
    
    paragraphs = []
    for i in range(0, len(formatted_lines), max_lines_per_block):
        chunk = formatted_lines[i:i + max_lines_per_block]
        block_text = "<br/>".join(chunk)
        p = Paragraph(block_text, style_code)
        paragraphs.append(p)
        
    return paragraphs

def main():
    root_dir = r"d:\Learning\Knowledge_Assistant"
    pdf_path = os.path.join(root_dir, "Knowledge_Assistant_Complete_Codebase.pdf")

    ignore_dirs = {'.venv', 'venv', 'node_modules', '__pycache__', '.git', 'dist', '.kombai', 'chroma_db', '.idea', '.vscode'}
    
    # Gather target source files
    target_files = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        dirs.sort()
        files.sort()
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, root_dir)
            
            # Skip build/generator scripts or lock files
            if rel_path in ["create_pdf.py", "build_project_pdf.py"]:
                continue
            if rel_path.startswith("data"):
                continue  # Skip raw dataset files, documented in Tree & Overview
            if f.endswith(('.png', '.jpg', '.ico', '.svg', '.db', '.sqlite3', '.lock', 'package-lock.json')):
                continue
            if f in ['.gitignore']:
                continue
                
            target_files.append((rel_path, full_path))

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#0F172A")    # Dark Slate
    SECONDARY = colors.HexColor("#1E293B")  # Slate 800
    ACCENT = colors.HexColor("#2563EB")     # Royal Blue
    TEXT_DARK = colors.HexColor("#334155")  # Slate 700
    BG_LIGHT = colors.HexColor("#F8FAFC")   # Light Slate
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=PRIMARY,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=17,
        textColor=ACCENT,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=ACCENT,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_DARK,
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=0,
        spaceAfter=0
    )

    tree_style = ParagraphStyle(
        'TreeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 30))
    story.append(Paragraph("KNOWLEDGE ASSISTANT", title_style))
    story.append(Paragraph("Project Architecture, Folder Structure & Exhaustive Codebase Documentation", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=3, color=ACCENT, spaceAfter=18, spaceBefore=0))
    
    cover_desc = """
    This document presents the full technical report and source code documentation for the 
    <b>Knowledge Assistant</b> system. It covers the system architecture, file manifest, complete folder hierarchy, 
    and line-by-line source code for both the <b>FastAPI Backend</b> and <b>React Frontend</b> applications.
    """
    story.append(Paragraph(cover_desc, body_style))
    story.append(Spacer(1, 15))

    # Calculate Lines & Stats
    total_files = len(target_files)
    total_loc = 0
    file_stats = []
    
    for rel_path, full_path in target_files:
        try:
            with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
                loc = len(lines)
                total_loc += loc
                file_stats.append((rel_path, loc, f"{os.path.getsize(full_path)/1024:.1f} KB"))
        except Exception:
            file_stats.append((rel_path, 0, "0 KB"))

    # Metadata Table on Cover Page
    meta_data = [
        [Paragraph("<b>Attribute</b>", body_style), Paragraph("<b>Specification / Detail</b>", body_style)],
        [Paragraph("<b>Project Title</b>", body_style), Paragraph("Knowledge Assistant (AI Knowledge & Document RAG)", body_style)],
        [Paragraph("<b>Backend Stack</b>", body_style), Paragraph("FastAPI, Python, ChromaDB Vector Store, SQLite, YAML", body_style)],
        [Paragraph("<b>Frontend Stack</b>", body_style), Paragraph("React.js, Vite, HTML5, Vanilla CSS / Tailwind", body_style)],
        [Paragraph("<b>Total Source Files</b>", body_style), Paragraph(str(total_files), body_style)],
        [Paragraph("<b>Total Lines of Code</b>", body_style), Paragraph(f"{total_loc:,} lines", body_style)],
        [Paragraph("<b>Document Created</b>", body_style), Paragraph("2026-07-21", body_style)],
        [Paragraph("<b>Author</b>", body_style), Paragraph("Antigravity AI Assistant", body_style)],
    ]
    t_meta = Table(meta_data, colWidths=[140, 364])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # ==================== ARCHITECTURE OVERVIEW ====================
    story.append(Paragraph("1. System Architecture & Component Design", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=12, spaceBefore=0))

    arch_text = """
    The <b>Knowledge Assistant</b> is an enterprise RAG (Retrieval-Augmented Generation) document management platform designed to index, structure, and query corporate documents across multiple domains (HR, Policy, Technical, Sales, Research).
    <br/><br/>
    <b>Core Subsystems & Modules:</b>
    <br/><br/>
    • <b>FastAPI REST Server (<code>backend/app/main.py</code>):</b> Defines asynchronous API routes for document scanning, indexing, search, metadata extraction, topic management, and database state.
    <br/><br/>
    • <b>Incremental Indexer & File Watcher (<code>backend/app/services/</code>):</b> Continuously checks target folders for file additions or modifications, extracts document metadata via rules defined in <code>document_rules.yaml</code>, chunks documents into optimal token windows, and builds vector embeddings.
    <br/><br/>
    • <b>Vector Database & Tracking DB (<code>backend/app/database/</code>):</b> Combines <b>ChromaDB</b> for high-density vector similarity search with a local <b>SQLite</b> database (<code>tracking.db</code>) to track file hashes, indexing status, and metadata registries.
    <br/><br/>
    • <b>Metadata Extractor & Rule Engine:</b> Utilizes <code>metadata_extractor.py</code> and <code>document_rules.py</code> to dynamically classify documents, assign topic tags, and extract domain attributes.
    <br/><br/>
    • <b>Frontend Dashboard (<code>frontend/src/</code>):</b> A modern React application providing semantic search UI, live document status dashboards, topic visualization, and system monitoring.
    """
    story.append(Paragraph(arch_text, body_style))
    story.append(Spacer(1, 15))

    # ==================== FOLDER STRUCTURE ====================
    story.append(Paragraph("2. Complete Folder Hierarchy & Directory Tree", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=12, spaceBefore=0))
    
    tree_lines = build_tree_lines(root_dir, ignore_dirs)
    
    # Chunk tree lines into blocks of 45 lines to avoid page overflow
    chunk_size = 45
    for i in range(0, len(tree_lines), chunk_size):
        chunk = tree_lines[i:i + chunk_size]
        escaped_chunk = escape_text("\n".join(chunk)).replace('\n', '<br/>').replace(' ', '&nbsp;')
        p_tree = Paragraph(escaped_chunk, tree_style)
        
        t_tree = Table([[p_tree]], colWidths=[504])
        t_tree.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
            ('BOX', (0,0), (-1,-1), 0.75, BORDER_COLOR),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t_tree)
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # ==================== FILE MANIFEST ====================
    story.append(Paragraph("3. Source File Manifest & Code Statistics", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=12, spaceBefore=0))

    table_data = [[
        Paragraph("<b>#</b>", body_style),
        Paragraph("<b>Relative File Path</b>", body_style),
        Paragraph("<b>Lines</b>", body_style),
        Paragraph("<b>Size</b>", body_style)
    ]]

    for idx, (rpath, loc, size_str) in enumerate(file_stats, 1):
        table_data.append([
            Paragraph(str(idx), body_style),
            Paragraph(f"<code>{rpath}</code>", body_style),
            Paragraph(str(loc), body_style),
            Paragraph(size_str, body_style)
        ])

    t_files = Table(table_data, colWidths=[30, 324, 70, 80])
    t_files.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_files)
    story.append(PageBreak())

    # ==================== FULL SOURCE CODE ====================
    story.append(Paragraph("4. Complete Source Code Listing", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceAfter=15, spaceBefore=0))

    for idx, (rel_path, full_path) in enumerate(target_files, 1):
        story.append(Paragraph(f"4.{idx} File: <code>{rel_path}</code>", h2_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=ACCENT, spaceAfter=8, spaceBefore=0))
        
        try:
            with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            content = f"# Error reading file {rel_path}: {e}"

        code_paragraphs = get_code_paragraphs(content, code_style, max_lines_per_block=40)
        
        for p_chunk in code_paragraphs:
            t_code = Table([[p_chunk]], colWidths=[504])
            t_code.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                ('PADDING', (0,0), (-1,-1), 6),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ]))
            story.append(t_code)
            story.append(Spacer(1, 4))
            
        story.append(Spacer(1, 12))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: Generated complete PDF at: {pdf_path}")

if __name__ == "__main__":
    main()
