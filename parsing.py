import json
import re
import os
from typing import Dict, List, Any
import pdfplumber
import spacy
from spacy.matcher import PhraseMatcher
class ResumeParserNLP:
    def __init__(self, skill_database: List[str] = None):
        """
        Initializes the NLP resume parser with spaCy and a phrase matcher for skills.
        """
        # Load small English model; fallback if not pre-downloaded
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            import subprocess
            import sys
            subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)
            self.nlp = spacy.load("en_core_web_sm")

        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        # Default fallback skill bank if none provided
        if not skill_database:
            skill_database = [
                "Python", "Java", "C++", "JavaScript", "TypeScript", "SQL", "NoSQL",
                "Machine Learning", "Deep Learning", "Statistics", "Data Handling",
                "Flask", "Django", "React", "Angular", "HTML", "CSS", "Git", "Docker",
                "NetworkX", "NLP", "Natural Language Processing", "Data Science"
            ]
        patterns = [self.nlp.make_doc(skill) for skill in skill_database]
        self.matcher.add("SKILL_BANK", patterns)
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Safely extracts raw text from a given PDF file path.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"The file path {pdf_path} does not exist.")
        extracted_text = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)         
        return "\n".join(extracted_text)
    def _extract_skills(self, doc: spacy.tokens.Doc) -> List[str]:
        """
        Extracts skills using spaCy's PhraseMatcher.
        """
        matches = self.matcher(doc)
        skills = set()
        for match_id, start, end in matches:
            span = doc[start:end]
            skills.add(span.text)
        return sorted(list(skills))
    def _extract_companies(self, doc: spacy.tokens.Doc) -> List[str]:
        """
        Extracts potential company names using spaCy Named Entity Recognition (NER).
        """
        companies = set()
        for ent in doc.ents:
            if ent.label_ == "ORG":
                # Filter out obvious non-company hits if necessary
                clean_org = ent.text.strip().replace("\n", " ")
                if len(clean_org) > 2:
                    companies.add(clean_org)
        return sorted(list(companies))
    def _extract_experience_years(self, text: str) -> float:
        """
        Uses standard regex patterns to estimate stated years of experience.
        """
        patterns = [
            r'(\d+(?:\.\d+)?)\s* \+?\s*years?\s*(?:of\s*)?experience',
            r'experience\s*:\s*(\d+(?:\.\d+)?)\s*years?',
            r'(\d+(?:\.\d+)?)\s*yrs?\b'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    continue
        return 0.0
    def _extract_durations_and_projects(self, text: str) -> Dict[str, List[str]]:
        """
        Extracts text patterns resembling job durations (e.g., 2021 - 2024) and project headers.
        """
        duration_pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\s*\d{4}\s*[-––]\s*(?:Present|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\s*\d{4})\b'
        durations = re.findall(duration_pattern, text, re.IGNORECASE)
        project_lines = []
        lines = text.split('\n')
        is_project_section = False
        for line in lines:
            if re.search(r'\b(projects|key projects|academic projects)\b', line, re.IGNORECASE):
                is_project_section = True
                continue
            if is_project_section and re.search(r'\b(experience|education|skills|certifications)\b', line, re.IGNORECASE):
                is_project_section = False
                break
            if is_project_section and line.strip():
                # Clean bullet symbols or numbers
                clean_line = re.sub(r'^[\s•\-\*–\d\.\)]+', '', line).strip()
                if clean_line:
                    project_lines.append(clean_line)
        return {
            "job_durations": sorted(list(set(durations))),
            "projects": project_lines[:5]  # Limit to top 5 detected points for downstream structural sanitization
        }
    def process_resume(self, pdf_path: str) -> str:
        """
        Main pipeline execution function. Parses raw text, extracts structural 
        features, and builds a verified JSON output structure.
        """
        # 1. Text Extraction
        raw_text = self.extract_text_from_pdf(pdf_path)
        
        # 2. NLP Pipeline Processing
        doc = self.nlp(raw_text)
        # 3. Component Extraction
        skills = self._extract_skills(doc)
        companies = self._extract_companies(doc)
        exp_years = self._extract_experience_years(raw_text)
        duration_and_projects = self._extract_durations_and_projects(raw_text)
        # 4. JSON Generation Mapping
        structured_data = {
            "skills": skills,
            "experience_years": exp_years,
            "company_names": companies,
            "job_durations": duration_and_projects["job_durations"],
            "projects": duration_and_projects["projects"]
        }
        return json.dumps(structured_data, indent=4, ensure_ascii=False)
# Execution pipeline verification guard
if __name__ == "__main__":
    # Example Initialization
    custom_skills = ["Python", "Machine Learning", "Statistics", "Flask", "NetworkX", "Data Handling"]
    parser = ResumeParserNLP(skill_database=custom_skills)
    print("ResumeParserNLP initialized successfully. Ready to push to repository.")
    print("Integration Check: Call `parser.process_resume('path_to_resume.pdf')` inside backend routers.")