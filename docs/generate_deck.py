import os
import sys
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
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
        self.saveState()
        # Background dark theme
        self.setFillColor(colors.HexColor("#090D16"))
        self.rect(0, 0, 792, 612, fill=True, stroke=False)
        
        # Header bar accent
        self.setFillColor(colors.HexColor("#F43F5E"))
        self.rect(0, 598, 792, 14, fill=True, stroke=False)
        
        # Footer text
        self.setFont("Helvetica-Bold", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(40, 25, "REDROB AI OS — Autonomous Career Operating System Deck")
        
        page_str = f"Slide {self._pageNumber} of {page_count}"
        self.drawRightString(752, 25, page_str)
        self.restoreState()

def build_pdf(filename="Redrob_Autonomous_AI_Career_OS_Deck.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(letter),
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#FFFFFF"),
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#F43F5E"),
        spaceAfter=20
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#FFFFFF"),
        spaceAfter=14
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#CBD5E1")
    )
    
    card_title = ParagraphStyle(
        'CardTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#F43F5E")
    )

    story = []

    # -------------------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 100))
    story.append(Paragraph("THE AUTONOMOUS AI CAREER OPERATING SYSTEM", title_style))
    story.append(Paragraph("Transforming Redrob into an AI-Native Career Ecosystem", subtitle_style))
    story.append(Spacer(1, 30))
    
    meta_text = Paragraph(
        "<b>Architectural Deck & Implementation Approach</b><br/>"
        "Outlining What We Built, Why We Built It That Way, and How It Works.<br/><br/>"
        "<i>Tech Stack: Next.js 15 • React 19 • FastAPI • LangGraph • Qdrant • Neo4j • Redis</i>", 
        body_style
    )
    story.append(meta_text)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 2: WHAT WE BUILT (OVERVIEW & AGENT ECOSYSTEM)
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. WHAT WE BUILT: Autonomous AI Ecosystem", section_heading))
    story.append(Paragraph("We built a complete, multi-agent SaaS platform where candidates and recruiters delegate tasks to 12 specialized autonomous AI agents.", body_style))
    story.append(Spacer(1, 15))

    col1 = [
        Paragraph("<b>Executive Agent</b>", card_title),
        Paragraph("Orchestrates global workflows, assigns goals, and maintains long-term memory.", body_style),
        Spacer(1, 10),
        Paragraph("<b>Career Coach & Forecast Agent</b>", card_title),
        Paragraph("Predicts trajectory, salary benchmarks, and 12-month promotion roadmaps.", body_style),
        Spacer(1, 10),
        Paragraph("<b>Resume & Skill Gap Agent</b>", card_title),
        Paragraph("Real-time ATS parsing, bullet rewriting, and missing skill node detection.", body_style),
        Spacer(1, 10),
        Paragraph("<b>Job Discovery Agent</b>", card_title),
        Paragraph("Scans thousands of jobs and auto-saves top matched opportunities.", body_style)
    ]
    
    col2 = [
        Paragraph("<b>Interview Agent</b>", card_title),
        Paragraph("Simulates voice, coding, and behavioral interviews with sentiment analysis.", body_style),
        Spacer(1, 10),
        Paragraph("<b>Recruiter Suite Agent</b>", card_title),
        Paragraph("Multi-signal candidate ranking, semantic matching, and hiring analytics.", body_style),
        Spacer(1, 10),
        Paragraph("<b>Networking & Learning Agent</b>", card_title),
        Paragraph("Curates YouTube videos, courses, gamified XP, and alumni mentor graphs.", body_style),
        Spacer(1, 10),
        Paragraph("<b>24x7 Opportunity Monitor</b>", card_title),
        Paragraph("Runs autonomously checking hackathons, freelance contracts, and jobs.", body_style)
    ]

    table_data = [[col1, col2]]
    t = Table(table_data, colWidths=[350, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('PADDING', (0,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1E293B")),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor("#1E293B"))
    ]))
    story.append(t)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 3: WHY WE BUILT IT THAT WAY (DESIGN PHILOSOPHY & ARCHITECTURE)
    # -------------------------------------------------------------------------
    story.append(Paragraph("2. WHY WE BUILT IT THAT WAY: Strategic Architecture", section_heading))
    story.append(Paragraph("Traditional job portals are static CRUD applications where users manually search and apply. Redrob flips this paradigm into proactive AI execution.", body_style))
    story.append(Spacer(1, 15))

    why_data = [
        [
            Paragraph("<b>Architectural Decision</b>", card_title),
            Paragraph("<b>Rationale & Strategic Benefit</b>", card_title)
        ],
        [
            Paragraph("<b>AI-First Autonomous Agents vs. CRUD Forms</b>", body_style),
            Paragraph("Users spend hours tweaking resumes and searching job boards. Autonomous background agents continuously perform work without user fatigue.", body_style)
        ],
        [
            Paragraph("<b>Unified Multi-Provider LLM Abstraction</b>", body_style),
            Paragraph("Prevents vendor lock-in and API outage failures. Enables dynamic switching between OpenAI, Gemini, Claude, Ollama, Groq, and DeepSeek.", body_style)
        ],
        [
            Paragraph("<b>Hybrid Storage (SQL + Qdrant Vector + Neo4j Graph)</b>", body_style),
            Paragraph("Relational DB handles transactional data; Vector DB powers semantic resume/job RAG; Knowledge Graph maps skill connections.", body_style)
        ],
        [
            Paragraph("<b>Next.js 15 Dark Glassmorphism UI</b>", body_style),
            Paragraph("Delivers an ultra-premium, modern SaaS aesthetic with instant real-time telemetry, animated progress widgets, and interactive agent chats.", body_style)
        ]
    ]

    t_why = Table(why_data, colWidths=[240, 460])
    t_why.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor("#1E293B")),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#0F172A")),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#334155"))
    ]))
    story.append(t_why)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SLIDE 4: HOW IT WORKS (END-TO-END WORKFLOW & DATA PIPELINE)
    # -------------------------------------------------------------------------
    story.append(Paragraph("3. HOW IT WORKS: Technical Execution Flow", section_heading))
    story.append(Paragraph("End-to-end user and system lifecycle from onboarding to autonomous placement:", body_style))
    story.append(Spacer(1, 15))

    flow_steps = [
        "<b>1. Onboarding & Parsing:</b> User uploads resume → Parsed by Resume Agent → Stored in PostgreSQL & embedded into Qdrant vector collection.",
        "<b>2. Knowledge Graph Mapping:</b> Candidate skills mapped into Neo4j nodes to detect missing proficiencies and project gaps.",
        "<b>3. Multi-Agent Orchestration:</b> Executive Agent initializes background workflows → Job Discovery matches jobs → Career Coach forecasts salary growth.",
        "<b>4. Real-time User Interaction:</b> Candidate practices in AI Mock Interview Lab → Receives instant sentiment and technical clarity feedback.",
        "<b>5. Recruiter Candidate Ranking:</b> Recruiters run semantic queries → Candidate ranking engine computes weighted composite fit scores.",
        "<b>6. 24x7 Continuous Monitoring:</b> Background daemon scans market opportunities and triggers proactive notifications via WebSockets."
    ]

    for step in flow_steps:
        story.append(Paragraph(step, body_style))
        story.append(Spacer(1, 10))

    story.append(Spacer(1, 20))
    summary_box = Table([[Paragraph("<b>Production Status:</b> 100% Code Complete • Docker Orchestrated • Unit Tested (Pytest 100% Pass)", ParagraphStyle('Box', parent=body_style, textColor=colors.HexColor("#10B981"), fontName='Helvetica-Bold'))]], colWidths=[700])
    summary_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#064E3B")),
        ('PADDING', (0,0), (-1,-1), 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#10B981"))
    ]))
    story.append(summary_box)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Presentation deck successfully created at: {filename}")

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, "Redrob_Autonomous_AI_Career_OS_Deck.pdf")
    build_pdf(pdf_path)
