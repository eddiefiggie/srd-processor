"""
Quality assurance and validation tools for SRD processing.
"""
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class QualityMetrics:
    """Quality metrics for processed content."""
    ocr_confidence: float
    formatting_score: float
    completeness_score: float
    d20_terms_preserved: int
    spell_errors: int
    broken_references: int

class QualityValidator:
    """Validate and score processed SRD content."""
    
    def __init__(self):
        # D&D 5e specific terms that should be preserved
        self.d20_terms = {
            'ability_scores': ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma'],
            'damage_types': ['acid', 'cold', 'fire', 'force', 'lightning', 'necrotic', 'poison', 'psychic', 'radiant', 'thunder'],
            'conditions': ['blinded', 'charmed', 'deafened', 'frightened', 'grappled', 'incapacitated', 'invisible', 'paralyzed', 'petrified', 'poisoned', 'prone', 'restrained', 'stunned', 'unconscious'],
            'spell_schools': ['abjuration', 'conjuration', 'divination', 'enchantment', 'evocation', 'illusion', 'necromancy', 'transmutation']
        }
    
    def validate_chunk(self, content: str) -> QualityMetrics:
        """Validate a single chunk and return quality metrics."""
        ocr_confidence = self._assess_ocr_quality(content)
        formatting_score = self._assess_formatting(content)
        completeness_score = self._assess_completeness(content)
        d20_terms = self._count_preserved_terms(content)
        spell_errors = self._detect_spelling_errors(content)
        broken_refs = self._detect_broken_references(content)
        
        return QualityMetrics(
            ocr_confidence=ocr_confidence,
            formatting_score=formatting_score,
            completeness_score=completeness_score,
            d20_terms_preserved=d20_terms,
            spell_errors=spell_errors,
            broken_references=broken_refs
        )
    
    def _assess_ocr_quality(self, content: str) -> float:
        """Assess OCR quality based on character patterns."""
        total_chars = len(content)
        if total_chars == 0:
            return 0.0
        
        # Count suspicious OCR artifacts
        artifacts = 0
        artifacts += len(re.findall(r'[Il1]{2,}', content))  # Multiple I/l/1
        artifacts += len(re.findall(r'[O0]{2,}', content))   # Multiple O/0
        artifacts += len(re.findall(r'\b[a-z]{1,2}\b', content))  # Single letters
        artifacts += len(re.findall(r'[^\w\s\-.,;:!?\'\"()[\]{}]', content))  # Strange characters
        
        return max(0.0, 1.0 - (artifacts / total_chars * 10))
    
    def _assess_formatting(self, content: str) -> float:
        """Assess markdown formatting quality."""
        score = 1.0
        
        # Check for proper headers
        if not re.search(r'^#{1,6}\s', content, re.MULTILINE):
            score -= 0.2
        
        # Check for proper lists
        if re.search(r'^\d+\.|\*|\-', content, re.MULTILINE):
            score += 0.1
        
        # Check for proper emphasis
        if re.search(r'\*\*.*?\*\*|\*.*?\*', content):
            score += 0.1
        
        # Penalize excessive whitespace
        if re.search(r'\n{4,}', content):
            score -= 0.2
        
        return max(0.0, min(1.0, score))
    
    def _assess_completeness(self, content: str) -> float:
        """Assess if content appears complete (no truncation)."""
        # Check for truncation indicators
        if '[...truncated...]' in content:
            return 0.5
        
        # Check for incomplete sentences
        sentences = re.split(r'[.!?]', content)
        incomplete = sum(1 for s in sentences if len(s.strip()) > 0 and not s.strip()[-1] in '.!?')
        
        return max(0.0, 1.0 - (incomplete / max(1, len(sentences))))
    
    def _count_preserved_terms(self, content: str) -> int:
        """Count how many D&D terms are properly preserved."""
        content_lower = content.lower()
        count = 0
        
        for category, terms in self.d20_terms.items():
            for term in terms:
                if term.lower() in content_lower:
                    count += 1
        
        return count
    
    def _detect_spelling_errors(self, content: str) -> int:
        """Detect potential spelling errors (simple heuristic)."""
        # This is a simplified version - you could integrate with pyspell or similar
        words = re.findall(r'\b[a-zA-Z]+\b', content)
        
        # Look for common OCR errors
        errors = 0
        for word in words:
            # Multiple consecutive identical letters (likely OCR error)
            if re.search(r'(.)\1{2,}', word):
                errors += 1
            # Very short "words" that are likely artifacts
            if len(word) == 1 and word.lower() not in ['a', 'i']:
                errors += 1
        
        return errors
    
    def _detect_broken_references(self, content: str) -> int:
        """Detect broken cross-references."""
        # Look for incomplete references
        broken = 0
        broken += len(re.findall(r'see\s+$|page\s+$', content, re.IGNORECASE))
        broken += len(re.findall(r'\bpp?\.\s*$', content))
        broken += len(re.findall(r'chapter\s+$', content, re.IGNORECASE))
        
        return broken

def generate_quality_report(chunks_dir: str) -> Dict:
    """Generate comprehensive quality report for all chunks."""
    validator = QualityValidator()
    chunks_path = Path(chunks_dir)
    
    if not chunks_path.exists():
        return {"error": f"Chunks directory {chunks_dir} not found"}
    
    chunk_files = list(chunks_path.glob("*.md"))
    if not chunk_files:
        return {"error": f"No markdown files found in {chunks_dir}"}
    
    metrics = []
    for chunk_file in chunk_files:
        content = chunk_file.read_text(encoding='utf-8')
        # Skip YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2].strip()
        
        chunk_metrics = validator.validate_chunk(content)
        metrics.append({
            'file': chunk_file.name,
            'metrics': chunk_metrics
        })
    
    # Aggregate statistics
    total_chunks = len(metrics)
    avg_ocr = sum(m['metrics'].ocr_confidence for m in metrics) / total_chunks
    avg_formatting = sum(m['metrics'].formatting_score for m in metrics) / total_chunks
    avg_completeness = sum(m['metrics'].completeness_score for m in metrics) / total_chunks
    total_errors = sum(m['metrics'].spell_errors for m in metrics)
    total_broken_refs = sum(m['metrics'].broken_references for m in metrics)
    
    return {
        'summary': {
            'total_chunks': total_chunks,
            'average_ocr_confidence': avg_ocr,
            'average_formatting_score': avg_formatting,
            'average_completeness_score': avg_completeness,
            'total_spell_errors': total_errors,
            'total_broken_references': total_broken_refs
        },
        'chunks': metrics,
        'recommendations': _generate_recommendations(avg_ocr, avg_formatting, total_errors, total_broken_refs)
    }

def _generate_recommendations(ocr_score: float, formatting_score: float, errors: int, broken_refs: int) -> List[str]:
    """Generate improvement recommendations based on quality metrics."""
    recommendations = []
    
    if ocr_score < 0.8:
        recommendations.append("Consider using higher quality PDF or OCR preprocessing")
    
    if formatting_score < 0.7:
        recommendations.append("Improve markdown formatting in AI cleanup prompts")
    
    if errors > 20:
        recommendations.append("Add spell-checking step to the pipeline")
    
    if broken_refs > 5:
        recommendations.append("Implement cross-reference repair logic")
    
    if not recommendations:
        recommendations.append("Quality looks good! Consider fine-tuning chunk sizes for your specific RAG use case")
    
    return recommendations
