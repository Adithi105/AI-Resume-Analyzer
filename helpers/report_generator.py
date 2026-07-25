import io
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf_report(resume_data: Dict[str, Any], jd_match_data: Optional[Dict[str, Any]] = None) -> bytes:
    """
    Generates a professional PDF executive report summarizing candidate analysis,
    ATS score, skills, recommendations, projects, and education.
    
    Returns:
        bytes: PDF file binary content.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#334155')
    )

    bold_label = ParagraphStyle(
        'BoldLabel',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # Title Banner
    story.append(Paragraph("AI Resume Analysis Report", title_style))
    story.append(Paragraph("Executive Resume Audit & ATS Readiness Summary", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3B82F6'), spaceAfter=15))

    # Candidate Overview Table
    name = resume_data.get("Name", "Not Specified")
    email = resume_data.get("Email", "Not Specified")
    phone = resume_data.get("Phone", "Not Specified")
    ats_score = resume_data.get("ATS_Score", 0)

    summary_data = [
        [
            Paragraph(f"<b>Candidate Name:</b> {name}", body_style),
            Paragraph(f"<b>ATS Score:</b> <font color='#2563EB'><b>{ats_score} / 100</b></font>", body_style)
        ],
        [
            Paragraph(f"<b>Email:</b> {email}", body_style),
            Paragraph(f"<b>Phone:</b> {phone}", body_style)
        ]
    ]

    if jd_match_data and jd_match_data.get("Match_Score") is not None:
        match_score = jd_match_data.get("Match_Score", 0)
        summary_data.append([
            Paragraph(f"<b>Target JD Match Score:</b> <font color='#059669'><b>{match_score}%</b></font>", body_style),
            Paragraph("", body_style)
        ])

    summary_table = Table(summary_data, colWidths=[260, 270])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 15))

    # Strengths & AI Suggestions
    strengths = resume_data.get("Strengths", [])
    if strengths:
        story.append(Paragraph("Key Strengths", section_heading))
        for item in strengths:
            story.append(Paragraph(f"• {item}", body_style))
        story.append(Spacer(1, 10))

    suggestions = resume_data.get("Suggestions", [])
    if suggestions:
        story.append(Paragraph("AI Recommendations for Improvement", section_heading))
        for item in suggestions:
            story.append(Paragraph(f"💡 {item}", body_style))
        story.append(Spacer(1, 10))

    # Skills Breakdown
    skills = resume_data.get("Skills", [])
    missing_skills = resume_data.get("Missing_Skills", [])

    story.append(Paragraph("Skills & Gap Analysis", section_heading))
    skills_text = ", ".join(skills) if skills else "None identified"
    story.append(Paragraph(f"<b>Detected Skills:</b> {skills_text}", body_style))
    story.append(Spacer(1, 4))
    
    if missing_skills:
        missing_text = ", ".join(missing_skills)
        story.append(Paragraph(f"<b>Recommended Missing Skills:</b> <font color='#DC2626'>{missing_text}</font>", body_style))
        story.append(Spacer(1, 10))

    # Job Description Comparison Section (If applicable)
    if jd_match_data:
        story.append(Paragraph("Job Description Alignment", section_heading))
        jd_matched = ", ".join(jd_match_data.get("Matching_Skills", [])) or "None"
        jd_missing = ", ".join(jd_match_data.get("Missing_Skills", [])) or "None"
        story.append(Paragraph(f"<b>Matching JD Skills:</b> {jd_matched}", body_style))
        story.append(Paragraph(f"<b>Missing JD Skills:</b> <font color='#DC2626'>{jd_missing}</font>", body_style))
        story.append(Spacer(1, 10))

    # Experience
    experience = resume_data.get("Experience", [])
    if experience:
        story.append(Paragraph("Professional Experience", section_heading))
        for exp in experience:
            if isinstance(exp, dict):
                company = exp.get('Company', 'Company')
                role = exp.get('Role', 'Role')
                duration = exp.get('Duration', '')
                desc = exp.get('Description', '')
                header_line = f"<b>{role}</b> - {company}"
                if duration:
                    header_line += f" ({duration})"
                story.append(Paragraph(header_line, bold_label))
                if desc:
                    story.append(Paragraph(desc, body_style))
            else:
                story.append(Paragraph(f"• {exp}", body_style))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 10))

    # Projects
    projects = resume_data.get("Projects", [])
    if projects:
        story.append(Paragraph("Projects", section_heading))
        for proj in projects:
            if isinstance(proj, dict):
                title = proj.get('Title', 'Project')
                tech = proj.get('TechStack', '')
                desc = proj.get('Description', '')
                p_text = f"<b>{title}</b>"
                if tech:
                    p_text += f" [{tech}]"
                story.append(Paragraph(p_text, bold_label))
                if desc:
                    story.append(Paragraph(desc, body_style))
            else:
                story.append(Paragraph(f"• {proj}", body_style))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 10))

    # Education
    education = resume_data.get("Education", [])
    if education:
        story.append(Paragraph("Education", section_heading))
        for edu in education:
            if isinstance(edu, dict):
                deg = edu.get('Degree', 'Degree')
                inst = edu.get('Institution', '')
                session = edu.get('Session', '')
                score = edu.get('Score') or edu.get('CGP') or edu.get('Percentage') or ''
                line = f"<b>{deg}</b> - {inst}"
                if session:
                    line += f" ({session})"
                if score:
                    line += f" | Score: {score}"
                story.append(Paragraph(line, body_style))
            else:
                story.append(Paragraph(f"• {edu}", body_style))
            story.append(Spacer(1, 4))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
