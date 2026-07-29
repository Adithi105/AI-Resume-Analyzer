import io
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf_report(resume_data: Dict[str, Any], jd_match_data: Optional[Dict[str, Any]] = None) -> bytes:
    """
    Generates a professional PDF executive report summarizing candidate analysis,
    Recruiter Verdict, Weighted ATS Score breakdown, skills, risks, recommendations, projects, and education.
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
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#334155')
    )

    bold_label = ParagraphStyle(
        'BoldLabel',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # Title Banner
    story.append(Paragraph("Intelligent ATS Recruiter Audit Report", title_style))
    story.append(Paragraph("Executive Resume Audit, Weighted ATS Score Breakdown & Development Roadmap", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3B82F6'), spaceAfter=12))

    # Candidate Overview Table
    name = resume_data.get("Name", "Not Specified")
    email = resume_data.get("Email", "Not Specified")
    phone = resume_data.get("Phone", "Not Specified")
    ats_score = resume_data.get("ATS_Score", 0)
    verdict = resume_data.get("Recruiter_Verdict", "Under Review")
    hiring_prob = resume_data.get("Hiring_Probability", "0%")
    level = resume_data.get("Candidate_Level", "Not Specified")

    summary_data = [
        [
            Paragraph(f"<b>Candidate Name:</b> {name}", body_style),
            Paragraph(f"<b>Overall Weighted ATS Score:</b> <font color='#2563EB'><b>{ats_score} / 100</b></font>", body_style)
        ],
        [
            Paragraph(f"<b>Email:</b> {email}", body_style),
            Paragraph(f"<b>Phone:</b> {phone}", body_style)
        ],
        [
            Paragraph(f"<b>Recruiter Verdict:</b> <font color='#059669'><b>{verdict}</b></font>", body_style),
            Paragraph(f"<b>Hiring Probability:</b> <b>{hiring_prob}</b> | <b>Level:</b> {level}", body_style)
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
        ('PADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 10))

    # Weighted ATS Breakdown Table
    breakdown = resume_data.get("ATS_Breakdown", {})
    if isinstance(breakdown, dict) and breakdown:
        story.append(Paragraph("Weighted ATS Category Breakdown", section_heading))
        cats_data = [
            [
                Paragraph("<b>Category</b>", bold_label),
                Paragraph("<b>Weight</b>", bold_label),
                Paragraph("<b>Score</b>", bold_label),
                Paragraph("<b>Category</b>", bold_label),
                Paragraph("<b>Weight</b>", bold_label),
                Paragraph("<b>Score</b>", bold_label)
            ],
            [
                Paragraph("Skills", body_style), Paragraph("25%", body_style), Paragraph(f"<b>{breakdown.get('Skills_Score', 0)}%</b>", body_style),
                Paragraph("Experience", body_style), Paragraph("25%", body_style), Paragraph(f"<b>{breakdown.get('Experience_Score', 0)}%</b>", body_style)
            ],
            [
                Paragraph("Projects", body_style), Paragraph("15%", body_style), Paragraph(f"<b>{breakdown.get('Projects_Score', 0)}%</b>", body_style),
                Paragraph("Keyword Match", body_style), Paragraph("15%", body_style), Paragraph(f"<b>{breakdown.get('Keyword_Match_Score', 0)}%</b>", body_style)
            ],
            [
                Paragraph("Education", body_style), Paragraph("10%", body_style), Paragraph(f"<b>{breakdown.get('Education_Score', 0)}%</b>", body_style),
                Paragraph("Formatting", body_style), Paragraph("5%", body_style), Paragraph(f"<b>{breakdown.get('Formatting_Score', 0)}%</b>", body_style)
            ],
            [
                Paragraph("Certifications", body_style), Paragraph("3%", body_style), Paragraph(f"<b>{breakdown.get('Certifications_Score', 0)}%</b>", body_style),
                Paragraph("Readability", body_style), Paragraph("2%", body_style), Paragraph(f"<b>{breakdown.get('Readability_Score', 0)}%</b>", body_style)
            ]
        ]
        breakdown_table = Table(cats_data, colWidths=[120, 50, 95, 120, 50, 95])
        breakdown_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EFF6FF')),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(breakdown_table)
        story.append(Spacer(1, 10))

    # Executive Summary & Overview
    exec_summary = resume_data.get("Executive_Summary", "")
    if exec_summary and exec_summary != "Not Provided":
        story.append(Paragraph("Executive Recruiter Summary", section_heading))
        story.append(Paragraph(exec_summary, body_style))
        story.append(Spacer(1, 8))

    # Resume Risks & Red Flags
    risks = resume_data.get("Resume_Risks", [])
    if risks:
        story.append(Paragraph("Resume Risks & Red Flags", section_heading))
        for r in risks:
            story.append(Paragraph(f"🚩 <font color='#DC2626'>{r}</font>", body_style))
        story.append(Spacer(1, 8))

    # Strengths & AI Suggestions
    tech_strengths = resume_data.get("Technical_Strengths", []) or resume_data.get("Strengths", [])
    if tech_strengths:
        story.append(Paragraph("Technical Strengths", section_heading))
        for item in tech_strengths:
            story.append(Paragraph(f"• {item}", body_style))
        story.append(Spacer(1, 8))

    suggestions = resume_data.get("Suggestions", []) or resume_data.get("Career_Suggestions", [])
    if suggestions:
        story.append(Paragraph("AI Recommendations for Improvement", section_heading))
        for item in suggestions:
            story.append(Paragraph(f"💡 {item}", body_style))
        story.append(Spacer(1, 8))

    # Skills Breakdown
    skills = resume_data.get("Skills", [])
    missing_skills = resume_data.get("Missing_Skills", [])

    story.append(Paragraph("Skills & Gap Analysis", section_heading))
    skills_text = ", ".join(skills) if skills else "None identified"
    story.append(Paragraph(f"<b>Detected Skills:</b> {skills_text}", body_style))
    story.append(Spacer(1, 3))
    
    if missing_skills:
        missing_text = ", ".join(missing_skills)
        story.append(Paragraph(f"<b>Recommended Missing Skills:</b> <font color='#DC2626'>{missing_text}</font>", body_style))
        story.append(Spacer(1, 8))

    # Learning Roadmap
    roadmap = resume_data.get("Learning_Roadmap", [])
    if roadmap:
        story.append(Paragraph("Learning & Career Roadmap", section_heading))
        for idx, step in enumerate(roadmap, 1):
            story.append(Paragraph(f"<b>Step {idx}:</b> {step}", body_style))
        story.append(Spacer(1, 8))

    # Job Description Comparison Section (If applicable)
    if jd_match_data:
        story.append(Paragraph("Job Description Alignment", section_heading))
        jd_matched = ", ".join(jd_match_data.get("Matching_Skills", [])) or "None"
        jd_missing = ", ".join(jd_match_data.get("Missing_Skills", [])) or "None"
        story.append(Paragraph(f"<b>Matching JD Skills:</b> {jd_matched}", body_style))
        story.append(Paragraph(f"<b>Missing JD Skills:</b> <font color='#DC2626'>{jd_missing}</font>", body_style))
        story.append(Spacer(1, 8))

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
            story.append(Spacer(1, 3))
        story.append(Spacer(1, 8))

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
            story.append(Spacer(1, 3))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generate_improved_resume_pdf(improved_data: Dict[str, Any], candidate_name: str = "Candidate") -> bytes:
    """
    Generates a publication-grade ATS-optimized PDF resume for the rewritten candidate profile.
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

    title_style = ParagraphStyle(
        'ImpTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )

    section_style = ParagraphStyle(
        'ImpSection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=12,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'ImpBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#334155')
    )

    bold_label = ParagraphStyle(
        'ImpBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # Title Banner
    story.append(Paragraph(f"{candidate_name} - ATS Optimized Resume", title_style))
    story.append(Paragraph("AI-Rewritten Executive Resume & Professional Highlights", styles['Normal']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=14))

    # Professional Summary
    prof_sum = improved_data.get("Professional_Summary")
    if prof_sum:
        story.append(Paragraph("Professional Summary", section_style))
        story.append(Paragraph(prof_sum, body_style))
        story.append(Spacer(1, 10))

    # Skills
    skills = improved_data.get("Skills", [])
    if skills:
        story.append(Paragraph("Technical & Core Competencies", section_style))
        skills_text = " • ".join(skills) if isinstance(skills, list) else str(skills)
        story.append(Paragraph(skills_text, body_style))
        story.append(Spacer(1, 10))

    # Experience
    exp_list = improved_data.get("Experience", [])
    if exp_list:
        story.append(Paragraph("Professional Experience", section_style))
        for exp in exp_list:
            if isinstance(exp, dict):
                comp = exp.get("Company", "Company")
                role = exp.get("Role", "Role")
                dur = exp.get("Duration", "")
                header = f"<b>{role}</b> - {comp}"
                if dur:
                    header += f" ({dur})"
                story.append(Paragraph(header, bold_label))

                bullets = exp.get("Bullet_Points") or exp.get("Description") or []
                if isinstance(bullets, list):
                    for b in bullets:
                        story.append(Paragraph(f"• {b}", body_style))
                elif bullets:
                    story.append(Paragraph(f"• {bullets}", body_style))
            else:
                story.append(Paragraph(f"• {exp}", body_style))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 8))

    # Key Projects
    proj_list = improved_data.get("Projects", [])
    if proj_list:
        story.append(Paragraph("Key Technical Projects", section_style))
        for proj in proj_list:
            if isinstance(proj, dict):
                title = proj.get("Title", "Project")
                tech = proj.get("TechStack", "")
                header = f"<b>{title}</b>"
                if tech:
                    header += f" [{tech}]"
                story.append(Paragraph(header, bold_label))

                bullets = proj.get("Bullet_Points") or proj.get("Description") or []
                if isinstance(bullets, list):
                    for b in bullets:
                        story.append(Paragraph(f"• {b}", body_style))
                elif bullets:
                    story.append(Paragraph(f"• {bullets}", body_style))
            else:
                story.append(Paragraph(f"• {proj}", body_style))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 8))

    # Achievements
    achievements = improved_data.get("Achievements", [])
    if achievements:
        story.append(Paragraph("Quantified Key Achievements", section_style))
        for a in achievements:
            story.append(Paragraph(f"🏆 {a}", body_style))
        story.append(Spacer(1, 10))

    # Education
    edu_list = improved_data.get("Education", [])
    if edu_list:
        story.append(Paragraph("Education Credentials", section_style))
        for edu in edu_list:
            if isinstance(edu, dict):
                deg = edu.get("Degree", "Degree")
                inst = edu.get("Institution", "")
                session = edu.get("Session", "")
                high = edu.get("Highlights") or edu.get("Description") or ""
                header = f"<b>{deg}</b> - {inst}"
                if session:
                    header += f" ({session})"
                story.append(Paragraph(header, body_style))
                if high:
                    story.append(Paragraph(f"• {high}", body_style))
            else:
                story.append(Paragraph(f"• {edu}", body_style))
            story.append(Spacer(1, 4))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generate_builder_resume_pdf(builder_data: Dict[str, Any], template_style: str = "Classic Executive") -> bytes:
    """
    Generates a template-styled PDF document for the AI Resume Builder.
    Supports: Classic Executive, Modern Tech, Minimalist Clean, Creative Professional.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Template Color Themes
    if template_style == "Modern Tech":
        header_color = colors.HexColor('#059669')    # Emerald Green
        accent_color = colors.HexColor('#0F172A')    # Slate
    elif template_style == "Minimalist Clean":
        header_color = colors.HexColor('#334155')    # Slate Blue
        accent_color = colors.HexColor('#0F172A')
    elif template_style == "Creative Professional":
        header_color = colors.HexColor('#6366F1')    # Indigo
        accent_color = colors.HexColor('#1E293B')
    else:
        # Default: Classic Executive
        header_color = colors.HexColor('#1E3A8A')    # Classic Deep Blue
        accent_color = colors.HexColor('#111827')

    name_style = ParagraphStyle(
        'BldName',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=header_color,
        alignment=1, # Center
        spaceAfter=4
    )

    contact_style = ParagraphStyle(
        'BldContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#64748B'),
        alignment=1,
        spaceAfter=12
    )

    section_style = ParagraphStyle(
        'BldSection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=header_color,
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BldBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=accent_color
    )

    bold_style = ParagraphStyle(
        'BldBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # Name Header
    name = builder_data.get("Name", "Candidate Name")
    story.append(Paragraph(name, name_style))

    # Contact Details Subtitle
    email = builder_data.get("Email", "")
    phone = builder_data.get("Phone", "")
    location = builder_data.get("Location", "")
    linkedin = builder_data.get("LinkedIn", "")
    bits = [b for b in [email, phone, location, linkedin] if b]
    if bits:
        story.append(Paragraph(" | ".join(bits), contact_style))
    
    story.append(HRFlowable(width="100%", thickness=1, color=header_color, spaceAfter=10))

    # Summary
    summary = builder_data.get("Professional_Summary", "")
    if summary:
        story.append(Paragraph("Professional Summary", section_style))
        story.append(Paragraph(summary, body_style))
        story.append(Spacer(1, 8))

    # Skills
    skills = builder_data.get("Skills", [])
    if skills:
        story.append(Paragraph("Technical & Core Skills", section_style))
        skills_text = " • ".join(skills) if isinstance(skills, list) else str(skills)
        story.append(Paragraph(skills_text, body_style))
        story.append(Spacer(1, 8))

    # Experience
    exp_list = builder_data.get("Experience", [])
    if exp_list:
        story.append(Paragraph("Professional Experience", section_style))
        for exp in exp_list:
            if isinstance(exp, dict):
                comp = exp.get("Company", "Company")
                role = exp.get("Role", "Role")
                dur = exp.get("Duration", "")
                header = f"<b>{role}</b> - {comp}"
                if dur:
                    header += f" ({dur})"
                story.append(Paragraph(header, bold_style))

                bullets = exp.get("Bullet_Points") or exp.get("Description") or []
                if isinstance(bullets, list):
                    for b in bullets:
                        story.append(Paragraph(f"• {b}", body_style))
                elif bullets:
                    story.append(Paragraph(f"• {bullets}", body_style))
            else:
                story.append(Paragraph(f"• {exp}", body_style))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 6))

    # Projects
    proj_list = builder_data.get("Projects", [])
    if proj_list:
        story.append(Paragraph("Key Technical Projects", section_style))
        for proj in proj_list:
            if isinstance(proj, dict):
                title = proj.get("Title", "Project")
                tech = proj.get("TechStack", "")
                header = f"<b>{title}</b>"
                if tech:
                    header += f" [{tech}]"
                story.append(Paragraph(header, bold_style))

                bullets = proj.get("Bullet_Points") or proj.get("Description") or []
                if isinstance(bullets, list):
                    for b in bullets:
                        story.append(Paragraph(f"• {b}", body_style))
                elif bullets:
                    story.append(Paragraph(f"• {bullets}", body_style))
            else:
                story.append(Paragraph(f"• {proj}", body_style))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 6))

    # Certifications
    certs = builder_data.get("Certifications", [])
    if certs:
        story.append(Paragraph("Certifications & Credentials", section_style))
        for cert in certs:
            if isinstance(cert, dict):
                ct = cert.get("Certificate", "Certification")
                inst = cert.get("Institution", "")
                line = f"<b>{ct}</b> - {inst}" if inst else ct
            else:
                line = str(cert)
            story.append(Paragraph(f"🏅 {line}", body_style))
        story.append(Spacer(1, 6))

    # Education
    edu_list = builder_data.get("Education", [])
    if edu_list:
        story.append(Paragraph("Education Credentials", section_style))
        for edu in edu_list:
            if isinstance(edu, dict):
                deg = edu.get("Degree", "Degree")
                inst = edu.get("Institution", "")
                session = edu.get("Session", "")
                score = edu.get("Score", "")
                header = f"<b>{deg}</b> - {inst}"
                if session:
                    header += f" ({session})"
                if score:
                    header += f" | Score: {score}"
                story.append(Paragraph(header, bold_style))
                desc = edu.get("Description") or edu.get("Highlights")
                if desc:
                    story.append(Paragraph(f"• {desc}", body_style))
            else:
                story.append(Paragraph(f"• {edu}", body_style))
            story.append(Spacer(1, 3))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
