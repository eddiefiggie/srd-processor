"""
D&D 5e SRD PDF to Markdown Converter & RAG Chunker

This tool provides a complete pipeline for converting D&D 5e System Reference Document (SRD) 
PDFs into clean, well-formatted Markdown and further chunking them into RAG-optimized pieces.

Main Features:
1. PDF text extraction with intelligent column detection
2. Basic text cleanup with regex-based formatting
3. AI-powered cleanup using OpenAI's GPT models
4. RAG-optimized chunking (200-500 words per chunk)
5. Table of Contents-driven section organization
6. Comprehensive health reporting on chunk quality

Author: eddiefiggie
Last Updated: July 2025
License: Mine!
"""

import pdfplumber
import re
from pathlib import Path
import os
import logging
from typing import Optional, Dict, List, Tuple
from openai import OpenAI

# Configuration handling - gracefully fallback if config.py doesn't exist
try:
    import config
except ImportError:
    print("❌ Config file not found. Please copy config.example.py to config.py and set your API key.")
    print("   Or set the OPENAI_API_KEY environment variable.")
    config = None

# ============================================================================
# CONFIGURATION & GLOBALS
# ============================================================================

# File configuration - use config file if available, otherwise use defaults
INPUT_FILE = config.INPUT_PDF_FILE if config else "SRD_CC_v5.2.1.pdf"
RAW_TEXT_FILE = config.RAW_TEXT_OUTPUT if config else "srd_raw_text.txt"
MARKDOWN_FILE = config.BASIC_MARKDOWN_OUTPUT if config else "srd_cleaned_output.md"
AI_CLEANED_FILE = config.AI_ENHANCED_OUTPUT if config else "srd_ai_cleaned.md"


# ============================================================================
# OPENAI CLIENT SETUP
# ============================================================================

def get_openai_client() -> OpenAI:
    """
    Initialize OpenAI client with API key from config or environment variable.
    
    Returns:
        OpenAI: Configured OpenAI client instance
        
    Raises:
        ValueError: If no API key is found or client initialization fails
    """
    try:
        if config:
            api_key = config.get_openai_api_key()
        else:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
        
        # Validate API key format
        if not api_key.startswith('sk-'):
            raise ValueError("Invalid OpenAI API key format (should start with 'sk-')")
        
        return OpenAI(api_key=api_key)
    except ImportError as e:
        raise ValueError(f"OpenAI library not installed: {e}") from e
    except (AttributeError, TypeError) as e:
        raise ValueError(f"Configuration error: {e}") from e
    except Exception as e:
        raise ValueError(f"Failed to initialize OpenAI client: {e}") from e


# ============================================================================
# PDF TEXT EXTRACTION
# ============================================================================

def extract_text_by_layout() -> bool:
    """
    Extract text from the SRD PDF using intelligent layout detection.
    
    This function handles different page layouts in the SRD:
    - Page 1: Single-column title page
    - Pages 2-4: Three-column table of contents (uses layout detection)
    - Remaining pages: Two-column main content (split down the middle)
    
    Output is saved to RAW_TEXT_FILE with page markers for later processing.
    
    Returns:
        bool: True if extraction succeeded, False otherwise
    """
    try:
        if not Path(INPUT_FILE).exists():
            print(f"❌ PDF file not found: {INPUT_FILE}")
            return False
        
        with pdfplumber.open(INPUT_FILE) as pdf:
            total_pages = len(pdf.pages)
            print(f"📖 Processing {total_pages} pages...")
            
            with open(RAW_TEXT_FILE, "w", encoding="utf-8") as out:
                for i, page in enumerate(pdf.pages):
                    # Progress indicator
                    if i % 10 == 0 or i == total_pages - 1:
                        print(f"   Page {i+1}/{total_pages}")
                    
                    page_marker = f"<!-- Page {i+1} -->\n"
                    out.write(page_marker)

                    if i == 0:
                        # Single-column title page
                        text = page.extract_text()
                    elif 1 <= i <= 3:
                        # Table of contents – 3-column: use layout detection
                        text = page.extract_text(layout=True)
                    else:
                        # Two-column layout: split page down the middle
                        left = page.crop((0, 0, page.width / 2, page.height)).extract_text()
                        right = page.crop((page.width / 2, 0, page.width, page.height)).extract_text()
                        text = (left or "") + "\n" + (right or "")

                    out.write((text or "") + "\n\n")
        
        print(f"✅ Text extraction complete: {RAW_TEXT_FILE}")
        return True
        
    except FileNotFoundError:
        print(f"❌ PDF file not found: {INPUT_FILE}")
        return False
    except PermissionError:
        print(f"❌ Permission denied accessing file: {INPUT_FILE}")
        return False
    except Exception as e:
        print(f"❌ Error during PDF extraction: {e}")
        return False

# ============================================================================
# PDF STRUCTURE ANALYSIS (for AI cleanup)
# ============================================================================

def analyze_page_structure_with_pdf(pdf, page_num: int) -> Optional[Dict]:
    """
    Analyze the visual structure of a PDF page to understand formatting.
    
    This function extracts font size information and identifies potential headers
    by analyzing text positioning and font characteristics. The results help the
    AI cleanup function understand document structure.
    
    Args:
        pdf: Open pdfplumber PDF object
        page_num: Page number to analyze (0-based index)
        
    Returns:
        dict: Structure information containing:
            - body_font_size: Most common font size (likely body text)
            - header_candidates: List of potential headers with position info
            - page_width/height: Page dimensions
        None: If analysis fails
    """
    try:
        page = pdf.pages[page_num]
        
        # Extract text with bounding boxes to understand structure
        words = page.extract_words()
        
        if not words:
            return None
        
        # Group words by similar font size (likely headers)
        font_sizes = {}
        for word in words:
            size = word.get('size', 12)
            if size not in font_sizes:
                font_sizes[size] = []
            font_sizes[size].append(word)
        
        if not font_sizes:
            return None
        
        # Find the most common font size (body text)
        body_size = max(font_sizes.keys(), key=lambda x: len(font_sizes[x]))
        
        # Identify potential headers (larger than body text)
        header_candidates = []
        for size, words_list in font_sizes.items():
            if size > body_size:
                for word in words_list:
                    header_candidates.append({
                        'text': word['text'],
                        'size': size,
                        'y': word['top'],
                        'bold': word.get('fontname', '').lower().find('bold') != -1
                    })
        
        # Sort headers by position (top to bottom)
        header_candidates.sort(key=lambda x: -x['y'])  # Negative for top-to-bottom
        
        return {
            'body_font_size': body_size,
            'header_candidates': header_candidates,
            'page_width': page.width,
            'page_height': page.height
        }
    except (IndexError, KeyError, AttributeError) as e:
        print(f"Warning: Could not analyze page {page_num + 1} structure: {e}")
        return None
    except Exception as e:
        print(f"Warning: Unexpected error analyzing page {page_num + 1}: {e}")
        return None


# ============================================================================
# AI-POWERED CLEANUP
# ============================================================================

def clean_page_with_ai(client: OpenAI, page_text: str, page_num: int, pdf_structure: Optional[Dict] = None) -> str:
    """
    Use OpenAI to clean and format a single page of text.
    
    This function sends raw OCR text to OpenAI's GPT model for intelligent cleanup,
    including OCR error correction, proper Markdown formatting, and D&D-specific
    content structuring.
    
    Args:
        client: OpenAI client instance
        page_text: Raw OCR text from the page
        page_num: Page number (0-based) for context
        pdf_structure: Optional structure analysis from analyze_page_structure_with_pdf
        
    Returns:
        str: Clean, formatted Markdown text
    """
    # Input validation
    if not page_text or not page_text.strip():
        return ""
    
    # Truncate extremely long pages to avoid API limits
    max_chars = 12000  # Conservative limit for API calls
    if len(page_text) > max_chars:
        page_text = page_text[:max_chars] + "\n[...truncated...]"
        print(f"   ⚠️  Page {page_num + 1} truncated to {max_chars} characters")
    
    # Create context about the document structure
    structure_context = ""
    if pdf_structure and pdf_structure.get('header_candidates'):
        headers = [h['text'] for h in pdf_structure['header_candidates'][:3]]
        structure_context = f"\n\nDetected headers on this page: {', '.join(headers)}"
    
    prompt = f"""You are helping to convert a D&D 5e SRD document from OCR text to clean Markdown. 

Page {page_num + 1} content:
{page_text}{structure_context}

Please clean this text and apply proper Markdown formatting:

1. Fix OCR errors and typos
2. Apply proper header hierarchy (# ## ### etc.) based on content importance
3. Format spell/ability blocks with proper structure
4. Bold important keywords like "Casting Time:", "Range:", "Duration:", etc.
5. Create proper lists and tables where appropriate
6. Preserve D&D terminology exactly
7. Remove excessive whitespace but maintain paragraph structure
8. Ensure proper sentence flow and grammar

Return ONLY the cleaned Markdown text, no explanations."""

    try:
        model = config.OPENAI_MODEL if config else "gpt-4o-mini"
        max_tokens = config.OPENAI_MAX_TOKENS if config else 4000
        temperature = config.OPENAI_TEMPERATURE if config else 0.1
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert at cleaning OCR text and formatting D&D content in Markdown."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        result = response.choices[0].message.content
        return result.strip() if result else page_text
    
    except ImportError as e:
        print(f"Warning: OpenAI library issue for page {page_num + 1}: {e}")
        return page_text
    except Exception as e:
        print(f"Warning: AI cleanup failed for page {page_num + 1}: {e}")
        return page_text  # Return original text if AI fails


# ============================================================================
# BASIC TEXT CLEANUP (Non-AI)
# ============================================================================

def clean_text_to_markdown(raw_text):
    """
    Apply basic regex-based text cleanup to convert raw OCR text to Markdown.
    
    This function performs simple but effective cleanup operations that work
    without AI, including:
    - Fixing line breaks and spacing issues
    - Converting ALL CAPS sections to headers
    - Adding basic Markdown formatting for D&D keywords
    
    Args:
        raw_text: Raw OCR text with layout artifacts
        
    Returns:
        str: Basic cleaned Markdown text
    """
    # Remove long blank gaps
    text = re.sub(r"\n{3,}", "\n\n", raw_text)

    # Remove broken words from hyphenated line endings
    text = re.sub(r"-\n", "", text)

    # Normalize line breaks in the middle of sentences
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Normalize multiple spaces
    text = re.sub(r" {2,}", " ", text)

    # Convert SCREAMING TITLES into headers (crude heuristic)
    text = re.sub(r"\n([A-Z][A-Z\s]{4,})\n", r"\n# \1\n", text)

    # Bold common mechanical keywords for clarity
    keywords = ["Casting Time", "Range", "Components", "Duration", "Level \\d+", "Saving Throw", "Hit Points"]
    for kw in keywords:
        text = re.sub(rf"(?<=\n)({kw}):", r"**\1**:", text)

    return text.strip()

def ai_cleanup_by_pages(raw_text_file, output_file):
    """
    Process each page individually with AI cleanup.
    
    This function coordinates the AI-powered cleanup process by:
    1. Reading the raw text file with page markers
    2. Splitting into individual pages
    3. Analyzing PDF structure for each page
    4. Sending each page to OpenAI for cleanup
    5. Combining results into a final cleaned file
    
    Args:
        raw_text_file: Path to raw text file with page markers
        output_file: Path where AI-cleaned output will be saved
        
    Returns:
        bool: True if successful, False if failed
    """
    print("🤖 Starting AI-powered cleanup...")
    
    # Initialize OpenAI client
    try:
        client = get_openai_client()
    except ValueError as e:
        print(f"❌ {e}")
        print("Please set your OPENAI_API_KEY environment variable")
        return False
    
    # Read the raw text
    raw_text = Path(raw_text_file).read_text(encoding="utf-8")
    
    # Split by page markers
    page_pattern = r'<!-- Page (\d+) -->'
    pages = re.split(page_pattern, raw_text)
    
    # Open PDF for structure analysis
    try:
        with pdfplumber.open(INPUT_FILE) as pdf:
            cleaned_pages = []
            
            # Process pages (skip first empty element from split)
            for i in range(1, len(pages), 2):
                page_num = int(pages[i]) - 1  # Convert to 0-based index
                page_text = pages[i + 1].strip()
                
                if not page_text:
                    continue
                
                print(f"🔄 Processing page {page_num + 1}...")
                
                # Analyze PDF structure for this page
                pdf_structure = analyze_page_structure_with_pdf(pdf, page_num)
                
                # Clean with AI
                cleaned_text = clean_page_with_ai(client, page_text, page_num, pdf_structure)
                
                # Add page marker and cleaned content
                cleaned_pages.append(f"<!-- Page {page_num + 1} -->\n\n{cleaned_text}")
            
            # Combine all cleaned pages
            final_text = "\n\n---\n\n".join(cleaned_pages)
            
            # Write to output file
            Path(output_file).write_text(final_text, encoding="utf-8")
            print(f"✅ AI cleanup complete! Saved to {output_file}")
            return True
            
    except Exception as e:
        print(f"❌ Error during AI cleanup: {e}")
        return False


# ============================================================================
# RAG CHUNKING SYSTEM
# ============================================================================

def count_words(text):
    """
    Count words in a text string, excluding Markdown formatting.
    
    This function provides accurate word counts for chunking by:
    - Removing Markdown syntax characters
    - Normalizing whitespace
    - Filtering out very short "words" (likely artifacts)
    
    Args:
        text: Text string to count words in
        
    Returns:
        int: Number of meaningful words in the text
    """
    # Remove markdown artifacts and count actual words
    clean_text = re.sub(r'[#\*\_\[\]\(\)]+', ' ', text)  # Remove markdown chars
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()  # Normalize whitespace
    words = [word for word in clean_text.split() if word and len(word) > 1]
    return len(words)

def split_large_content(content, target_min=200, target_max=500):
    """
    Split large content into smaller chunks targeting 200-500 words each.
    
    This function intelligently splits content by:
    1. Using headers as natural break points when possible
    2. Falling back to paragraph boundaries for oversized chunks
    3. Preserving content structure and readability
    
    The algorithm prioritizes keeping related content together while
    staying within the target word count range for optimal RAG performance.
    
    Args:
        content: Text content to split
        target_min: Minimum target words per chunk (default: 200)
        target_max: Maximum target words per chunk (default: 500)
        
    Returns:
        list: List of content chunks as strings
    """
    chunks = []
    lines = content.split('\n')
    current_chunk = []
    current_word_count = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        line_words = count_words(line)
        
        # Check if this is a header (# ## ### etc)
        is_header = line.strip().startswith('#') and len(line.strip()) > 1
        
        # If we're at a header and have content, consider splitting
        if is_header and current_chunk and current_word_count >= target_min:
            # Save current chunk
            chunk_content = '\n'.join(current_chunk).strip()
            if chunk_content:
                chunks.append(chunk_content)
            current_chunk = []
            current_word_count = 0
        
        # Add line to current chunk
        current_chunk.append(line)
        current_word_count += line_words
        
        # If chunk is getting too large, try to split at paragraph boundaries
        if current_word_count >= target_max:
            # Look for a good break point (empty line or next header)
            break_point = None
            for j in range(i + 1, min(i + 10, len(lines))):  # Look ahead a bit
                if not lines[j].strip():  # Empty line (paragraph break)
                    break_point = j
                    break
                elif lines[j].strip().startswith('#'):  # Header
                    break_point = j
                    break
            
            if break_point:
                # Split at the break point
                chunk_content = '\n'.join(current_chunk).strip()
                if chunk_content:
                    chunks.append(chunk_content)
                current_chunk = []
                current_word_count = 0
                i = break_point - 1  # Will be incremented at end of loop
        
        i += 1
    
    # Add remaining content
    if current_chunk:
        chunk_content = '\n'.join(current_chunk).strip()
        if chunk_content:
            chunks.append(chunk_content)
    
    return chunks

def chunk_file_for_rag(input_file, output_dir="export", target_min=200, target_max=500):
    """
    Split the AI-cleaned markdown file into small, focused chunks suitable for RAG.
    
    This is the main RAG optimization function that:
    1. Uses the D&D 5e SRD Table of Contents as the authoritative structure guide
    2. Keeps each ToC section as a single chunk when possible (preserves logical grouping)
    3. Only splits sections that are much larger than target_max (>2x target_max)
    4. Uses intelligent splitting at headers and paragraph boundaries
    5. Adds YAML metadata to each chunk for RAG systems
    6. Generates comprehensive quality reports
    
    Chunking Strategy:
    - Priority 1: Keep ToC sections intact (even if slightly over target_max)
    - Priority 2: Split only very large sections using natural boundaries
    - Priority 3: Maintain content coherence and context
    
    Output Format:
    - File naming: {seq}_{section_name}_SRD_5_2.md
    - YAML frontmatter with metadata (title, source_section, word_count, chunk_id)
    - Sequential numbering for easy organization
    
    Args:
        input_file: Path to AI-cleaned markdown file to chunk
        output_dir: Directory where chunk files will be written (default: "export")
        target_min: Minimum target words per chunk (default: 200)
        target_max: Maximum target words per chunk (default: 500)
        
    Returns:
        bool: True if chunking succeeded, False if failed
    """
    print(f"📁 Creating RAG-optimized chunks from {input_file}...")
    print(f"🎯 Target: {target_min}-{target_max} words per chunk")
    
    # Create export directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    print(f"📂 Export directory: {output_path.absolute()}")
    
    # Read the input file
    if not Path(input_file).exists():
        print(f"❌ Input file {input_file} not found")
        return False
    
    content = Path(input_file).read_text(encoding="utf-8")
    
    # Comprehensive Table of Contents sections based on the actual SRD structure
    # Each entry represents a top-level category that should get its own chunk
    toc_sections = [
        ("Legal Information", "# Legal Information"),
        ("Playing the Game", "# Playing the Game"),
        ("The Six Abilities", "# The Six Abilities"),
        ("D20 Tests", "# D20 Tests"),
        ("Proficiency", "# Proficiency"),
        ("Actions", "# Actions"),
        ("Social Interaction", "# Social Interaction"),
        ("Exploration", "# Exploration"),
        ("Combat", "# Combat"),
        ("Damage and Healing", "# Damage and Healing"),
        ("Character Creation", "# Character Creation"),
        ("Classes", "# Classes"),
        ("Character Backgrounds", "# Character Backgrounds"),
        ("Character Species", "# Character Species"),
        ("Feats", "# Feats"),
        ("Spells", "# Spells"),
        ("Fighter", "# Fighter"),
        ("Monk", "# Monk"),
        ("Paladin", "# Paladin"),
        ("Ranger", "# Ranger"),
        ("Rogue", "# Rogue"),
        ("Sorcerer", "# Sorcerer"),
        ("Warlock", "# Warlock"),
        ("Wizard", "# Wizard"),
        ("Character Origins", "# Character Origins"),
        ("Magic Items", "# Magic Items"),
        ("Magic Item Categories", "# Magic Item Categories"),
        ("Monsters", "# Monsters"),
        ("Monsters A–Z", "# Monsters A–Z"),
        ("Index of Stat Blocks", "# Index of Stat Blocks"),
        ("Magic Items A–Z", "# Magic Items A–Z"),
    ]
    
    all_chunks = []
    chunk_counter = 1
    
    # Clear existing export directory
    print(f"🧹 Clearing existing chunks in {output_dir}/")
    for existing_file in output_path.glob("*.md"):
        existing_file.unlink()
    
    # Process each major section
    for i, (section_name, section_header) in enumerate(toc_sections):
        print(f"\n🔍 Processing section: {section_name}")
        
        # Find section start
        section_start = content.find(section_header)
        if section_start == -1:
            print(f"⚠️  Section '{section_name}' not found, skipping")
            continue
        
        # Find section end (next major section or end of document)
        section_end = len(content)
        for j in range(i + 1, len(toc_sections)):
            next_header = toc_sections[j][1]
            next_pos = content.find(next_header, section_start + 1)
            if next_pos != -1:
                section_end = next_pos
                break
        
        # Extract section content
        section_content = content[section_start:section_end].strip()
        section_word_count = count_words(section_content)
        
        print(f"   📊 Section size: {section_word_count} words")
        
        if section_word_count == 0:
            print("   ⚠️  Empty section, skipping")
            continue
        
        # Strategy: Always try to keep ToC sections as single chunks if possible
        # Only split if absolutely necessary (much larger than target_max)
        if section_word_count <= target_max * 2:  # Allow up to 2x target_max for single chunks
            # Keep as single chunk - this preserves ToC structure
            chunk_info = {
                'number': chunk_counter,
                'title': section_name,
                'content': section_content,
                'word_count': section_word_count,
                'source_section': section_name
            }
            all_chunks.append(chunk_info)
            status = "✅ Single chunk" if section_word_count <= target_max else "📏 Large single chunk"
            print(f"   {status}: {section_word_count} words")
            chunk_counter += 1
        else:
            # Only split very large sections that are more than 2x target_max
            print(f"   📝 Section too large ({section_word_count} words), splitting intelligently...")
            
            # Try to split at natural boundaries (subsections first, then paragraphs)
            sub_chunks = split_large_content(section_content, target_min, target_max)
            print(f"   📝 Split into {len(sub_chunks)} sub-chunks")
            
            for j, sub_chunk in enumerate(sub_chunks, 1):
                sub_word_count = count_words(sub_chunk)
                # Create title for sub-chunk
                sub_title = f"{section_name} Part {j}" if len(sub_chunks) > 1 else section_name
                
                chunk_info = {
                    'number': chunk_counter,
                    'title': sub_title,
                    'content': sub_chunk,
                    'word_count': sub_word_count,
                    'source_section': section_name
                }
                all_chunks.append(chunk_info)
                print(f"      - Part {j}: {sub_word_count} words")
                chunk_counter += 1
    
    # Write chunks to files and collect statistics
    chunk_stats = {
        'total_chunks': len(all_chunks),
        'word_counts': [],
        'ideal_range_count': 0,
        'too_small_count': 0,
        'too_large_count': 0,
        'sections_covered': set()
    }
    
    print(f"\n📝 Writing {len(all_chunks)} chunks to files...")
    
    for chunk_info in all_chunks:
        # Clean title for filename
        clean_title = re.sub(r'[^\w\s-]', '', chunk_info['title'])
        clean_title = re.sub(r'\s+', '_', clean_title)
        clean_title = clean_title.strip('_')
        
        # Truncate if too long
        if len(clean_title) > 40:
            clean_title = clean_title[:40]
        
        # Create filename
        filename = f"{chunk_info['number']:03d}_{clean_title}_SRD_5_2.md"
        filepath = output_path / filename
        
        # Add metadata header to chunk
        chunk_with_metadata = f"""---
title: "{chunk_info['title']}"
source_section: "{chunk_info['source_section']}"
word_count: {chunk_info['word_count']}
chunk_id: {chunk_info['number']:03d}
---

{chunk_info['content']}"""
        
        # Write to file
        try:
            filepath.write_text(chunk_with_metadata, encoding="utf-8")
            
            # Update statistics
            word_count = chunk_info['word_count']
            chunk_stats['word_counts'].append(word_count)
            chunk_stats['sections_covered'].add(chunk_info['source_section'])
            
            if target_min <= word_count <= target_max:
                chunk_stats['ideal_range_count'] += 1
                status = "✅"
            elif word_count < target_min:
                chunk_stats['too_small_count'] += 1
                status = "🔸"
            else:
                chunk_stats['too_large_count'] += 1
                status = "🔹"
            
            print(f"   {status} {filename} ({word_count} words)")
            
        except OSError as e:
            print(f"❌ Failed to create {filename}: {e}")
    
    # Generate health report
    generate_health_report(chunk_stats, target_min, target_max, len(toc_sections))
    
    print(f"\n🎉 Successfully created {len(all_chunks)} RAG-optimized chunks in {output_dir}/")
    return True

def generate_health_report(stats, target_min, target_max, total_sections):
    """Generate a comprehensive health report on the chunking results."""
    print("\n" + "="*60)
    print("📊 CHUNKING HEALTH REPORT")
    print("="*60)
    
    # Basic statistics
    print(f"📦 Total chunks created: {stats['total_chunks']}")
    print(f"📚 Sections covered: {len(stats['sections_covered'])}/{total_sections}")
    
    if stats['word_counts']:
        word_counts = stats['word_counts']
        avg_words = sum(word_counts) / len(word_counts)
        min_words = min(word_counts)
        max_words = max(word_counts)
        
        print("📝 Word count statistics:")
        print(f"   • Average: {avg_words:.0f} words")
        print(f"   • Range: {min_words} - {max_words} words")
        print(f"   • Target range: {target_min}-{target_max} words")
    
    # Size distribution
    print("\n📏 Size distribution:")
    ideal_pct = (stats['ideal_range_count'] / stats['total_chunks']) * 100
    small_pct = (stats['too_small_count'] / stats['total_chunks']) * 100
    large_pct = (stats['too_large_count'] / stats['total_chunks']) * 100
    
    print(f"   ✅ Ideal size ({target_min}-{target_max} words): {stats['ideal_range_count']} chunks ({ideal_pct:.1f}%)")
    print(f"   🔸 Too small (<{target_min} words): {stats['too_small_count']} chunks ({small_pct:.1f}%)")
    print(f"   🔹 Too large (>{target_max} words): {stats['too_large_count']} chunks ({large_pct:.1f}%)")
    
    # Quality assessment
    print("\n🎯 Quality assessment:")
    if ideal_pct >= 80:
        print("   🟢 EXCELLENT: >80% of chunks in ideal range")
    elif ideal_pct >= 60:
        print("   🟡 GOOD: 60-80% of chunks in ideal range")
    elif ideal_pct >= 40:
        print("   🟠 FAIR: 40-60% of chunks in ideal range")
    else:
        print("   🔴 NEEDS IMPROVEMENT: <40% of chunks in ideal range")
    
    # Recommendations
    print("\n💡 Recommendations:")
    if stats['too_large_count'] > stats['total_chunks'] * 0.2:
        print("   • Consider splitting large chunks further at paragraph boundaries")
    if stats['too_small_count'] > stats['total_chunks'] * 0.2:
        print("   • Consider merging very small chunks with related content")
    if len(stats['sections_covered']) < total_sections * 0.9:
        print("   • Some sections may be missing - verify section detection logic")
    
    print("="*60)


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(verbose: bool = True) -> logging.Logger:
    """
    Set up logging with appropriate levels and formatting.
    
    Args:
        verbose: If True, show INFO level logs. If False, only show WARNING and above.
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger('srd_processor')
    
    # Don't add handlers if already configured
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO if verbose else logging.WARNING)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    return logger

# Initialize logger
_logger = setup_logging(verbose=config.VERBOSE_LOGGING if config else True)


# ============================================================================
# CONFIGURATION VALIDATION
# ============================================================================

def validate_environment() -> Tuple[bool, List[str]]:
    """
    Validate that the environment is properly set up for running the processor.
    
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    # Check if PDF file exists
    if not Path(INPUT_FILE).exists():
        issues.append(f"PDF file not found: {INPUT_FILE}")
    
    # Check write permissions
    try:
        test_file = Path("test_write_permission.tmp")
        test_file.write_text("test", encoding="utf-8")
        test_file.unlink()
    except OSError:
        issues.append("No write permission in current directory")
    
    # Check if config file exists when expected
    if config is None:
        issues.append("Config file not found - using defaults and environment variables")
    
    # Check if required directories can be created
    try:
        Path("export").mkdir(exist_ok=True)
    except Exception as e:
        issues.append(f"Cannot create export directory: {e}")
    
    return len(issues) == 0, issues


def print_environment_status():
    """Print environment validation results."""
    is_valid, issues = validate_environment()
    
    if is_valid:
        print("✅ Environment validation passed")
    else:
        print("⚠️  Environment issues detected:")
        for issue in issues:
            print(f"   • {issue}")
        print()


# ============================================================================
# MAIN ORCHESTRATION
# ============================================================================

def detect_workflow_state():
    """
    Detect what files already exist to determine where to resume the workflow.
    
    Returns:
        dict: Workflow state information containing:
            - has_raw_text: bool - Raw text file exists
            - has_basic_markdown: bool - Basic cleaned markdown exists  
            - has_ai_cleaned: bool - AI-enhanced markdown exists
            - has_chunks: bool - RAG chunks directory exists with files
            - suggested_start: str - Recommended starting point
    """
    state = {
        'has_raw_text': Path(RAW_TEXT_FILE).exists(),
        'has_basic_markdown': Path(MARKDOWN_FILE).exists(),
        'has_ai_cleaned': Path(AI_CLEANED_FILE).exists(),
        'has_chunks': False,
        'suggested_start': 'pdf_extraction'
    }
    
    # Check for existing chunks
    export_dir = Path("export")
    if export_dir.exists():
        chunk_files = list(export_dir.glob("*.md"))
        state['has_chunks'] = len(chunk_files) > 0
    
    # Determine suggested starting point
    if state['has_chunks']:
        state['suggested_start'] = 'complete'
    elif state['has_ai_cleaned']:
        state['suggested_start'] = 'chunking'
    elif state['has_basic_markdown']:
        state['suggested_start'] = 'ai_cleanup'
    elif state['has_raw_text']:
        state['suggested_start'] = 'basic_cleanup'
    else:
        state['suggested_start'] = 'pdf_extraction'
    
    return state


def print_workflow_status(state):
    """
    Print a user-friendly summary of the current workflow state.
    
    Args:
        state: Dictionary from detect_workflow_state()
    """
    print("📋 Current Workflow Status:")
    print(f"   {'✅' if state['has_raw_text'] else '❌'} Raw text extraction (srd_raw_text.txt)")
    print(f"   {'✅' if state['has_basic_markdown'] else '❌'} Basic cleanup (srd_cleaned_output.md)")
    print(f"   {'✅' if state['has_ai_cleaned'] else '❌'} AI cleanup (srd_ai_cleaned.md)")
    print(f"   {'✅' if state['has_chunks'] else '❌'} RAG chunking (export/ directory)")
    print()


def ask_user_workflow_choice(state):
    """
    Ask the user what they want to do based on the current workflow state.
    
    Args:
        state: Dictionary from detect_workflow_state()
        
    Returns:
        str: User's choice ('start_fresh', 'resume', 'skip_to', 'chunks_only')
    """
    if state['suggested_start'] == 'complete':
        print("🎉 All workflow steps appear to be complete!")
        choice = input("Would you like to:\n"
                      "  1. Start fresh (overwrite existing files)\n"
                      "  2. Re-run chunking only\n"
                      "  3. Exit\n"
                      "Choice (1/2/3): ").strip()
        if choice == '1':
            return 'start_fresh'
        elif choice == '2':
            return 'chunks_only'
        else:
            return 'exit'
    
    elif state['suggested_start'] == 'chunking':
        print("📄 AI-cleaned file exists but no chunks found.")
        choice = input("Would you like to:\n"
                      "  1. Start fresh (re-extract and re-process everything)\n"
                      "  2. Just create RAG chunks from existing AI-cleaned file\n"
                      "  3. Exit\n"
                      "Choice (1/2/3): ").strip()
        if choice == '1':
            return 'start_fresh'
        elif choice == '2':
            return 'chunks_only'
        else:
            return 'exit'
    
    elif state['suggested_start'] == 'ai_cleanup':
        print("📝 Basic cleaned file exists but no AI cleanup found.")
        choice = input("Would you like to:\n"
                      "  1. Start fresh (re-extract and re-process everything)\n"
                      "  2. Resume from AI cleanup step\n"
                      "  3. Exit\n"
                      "Choice (1/2/3): ").strip()
        if choice == '1':
            return 'start_fresh'
        elif choice == '2':
            return 'resume'
        else:
            return 'exit'
    
    elif state['suggested_start'] == 'basic_cleanup':
        print("📑 Raw text exists but no cleaned files found.")
        choice = input("Would you like to:\n"
                      "  1. Start fresh (re-extract PDF)\n"
                      "  2. Resume from basic cleanup step\n"
                      "  3. Exit\n"
                      "Choice (1/2/3): ").strip()
        if choice == '1':
            return 'start_fresh'
        elif choice == '2':
            return 'resume'
        else:
            return 'exit'
    
    else:  # pdf_extraction
        print("📋 No existing files found - will start from PDF extraction.")
        return 'start_fresh'


def main():
    """
    Main orchestration function for the D&D SRD processing pipeline.
    
    This function coordinates the complete workflow with smart resume capability:
    1. Validate environment setup
    2. Detect existing files to determine where to resume
    3. Ask user what they want to do (start fresh, resume, or skip steps)
    4. Execute only the necessary steps based on user choice
    
    Smart Resume Features:
    - Detects existing raw text, cleaned markdown, AI-enhanced files, and chunks
    - Suggests optimal starting point based on existing files
    - Allows users to start fresh or resume from any step
    - Prevents unnecessary re-processing of existing work
    
    Processing Steps (conditionally executed):
    - PDF extraction: Creates raw text with page markers
    - Basic cleanup: Creates basic readable Markdown
    - AI cleanup: Creates AI-enhanced Markdown (requires API key)
    - RAG chunking: Creates 200-500 word chunks with metadata
    
    Output Files (depending on steps chosen):
    - {RAW_TEXT_FILE}: Raw OCR text with page markers
    - {MARKDOWN_FILE}: Basic cleaned Markdown
    - {AI_CLEANED_FILE}: AI-enhanced Markdown (if AI cleanup chosen)
    - export/*.md: Individual RAG chunks (if chunking chosen)
    """
    # Validate environment
    print_environment_status()
    
    print("🔍 Checking existing files...")
    state = detect_workflow_state()
    print_workflow_status(state)
    
    # Ask user what they want to do
    user_choice = ask_user_workflow_choice(state)
    
    if user_choice == 'exit':
        print("👋 Goodbye!")
        return
    
    # Execute workflow based on user choice
    if user_choice == 'start_fresh':
        print("\n🔄 Starting fresh workflow...\n")
        execute_full_workflow()
    
    elif user_choice == 'resume':
        if state['suggested_start'] == 'basic_cleanup':
            print("\n▶️  Resuming from basic cleanup...\n")
            execute_workflow_from_basic_cleanup()
        elif state['suggested_start'] == 'ai_cleanup':
            print("\n▶️  Resuming from AI cleanup...\n")
            execute_workflow_from_ai_cleanup()
    
    elif user_choice == 'chunks_only':
        print("\n▶️  Creating RAG chunks only...\n")
        execute_chunking_only()


def execute_full_workflow():
    """Execute the complete workflow from PDF extraction to chunking."""
    print("📖 Extracting text from PDF...")
    
    if not extract_text_by_layout():
        print("❌ PDF extraction failed. Please check your PDF file and try again.")
        return
    
    print("🧹 Performing basic cleanup...")
    try:
        raw = Path(RAW_TEXT_FILE).read_text(encoding="utf-8")
        cleaned = clean_text_to_markdown(raw)
        Path(MARKDOWN_FILE).write_text(cleaned, encoding="utf-8")
        print(f"✅ Basic cleanup done: {MARKDOWN_FILE}")
    except Exception as e:
        print(f"❌ Basic cleanup failed: {e}")
        return
    
    # Continue with AI cleanup option
    execute_ai_cleanup_workflow()


def execute_workflow_from_basic_cleanup():
    """Execute workflow starting from basic cleanup (raw text already exists)."""
    if not Path(RAW_TEXT_FILE).exists():
        print(f"❌ Raw text file {RAW_TEXT_FILE} not found. Starting from PDF extraction...")
        execute_full_workflow()
        return
    
    print("🧹 Performing basic cleanup...")
    raw = Path(RAW_TEXT_FILE).read_text(encoding="utf-8")
    cleaned = clean_text_to_markdown(raw)
    Path(MARKDOWN_FILE).write_text(cleaned, encoding="utf-8")
    print(f"✅ Basic cleanup done: {MARKDOWN_FILE}")
    
    # Continue with AI cleanup option
    execute_ai_cleanup_workflow()


def execute_workflow_from_ai_cleanup():
    """Execute workflow starting from AI cleanup (basic markdown already exists)."""
    if not Path(MARKDOWN_FILE).exists():
        print(f"❌ Basic markdown file {MARKDOWN_FILE} not found. Starting from basic cleanup...")
        execute_workflow_from_basic_cleanup()
        return
    
    # Continue with AI cleanup option
    execute_ai_cleanup_workflow()


def execute_ai_cleanup_workflow():
    """Handle the AI cleanup portion of the workflow with user interaction."""
    # Ask user if they want AI cleanup
    try:
        use_ai = input("\n🤖 Would you like to perform AI-powered cleanup? (y/n): ").lower().strip()
        if use_ai in ['y', 'yes']:
            success = ai_cleanup_by_pages(RAW_TEXT_FILE, AI_CLEANED_FILE)
            if success:
                print("🎉 AI cleanup complete!")
                print(f"   - Basic: {MARKDOWN_FILE}")
                print(f"   - AI Enhanced: {AI_CLEANED_FILE}")
                
                # Ask about chunking
                ask_about_chunking(AI_CLEANED_FILE)
            else:
                print(f"⚠️  AI cleanup failed, but basic cleanup is available in {MARKDOWN_FILE}")
                ask_about_chunking(MARKDOWN_FILE)
        else:
            print(f"✅ Skipping AI cleanup. Using basic cleaned file: {MARKDOWN_FILE}")
            ask_about_chunking(MARKDOWN_FILE)
    except (KeyboardInterrupt, EOFError):
        print(f"\n✅ AI cleanup skipped. Basic file available: {MARKDOWN_FILE}")
        ask_about_chunking(MARKDOWN_FILE)


def execute_chunking_only():
    """Execute only the RAG chunking step using the best available file."""
    # Determine which file to use for chunking
    if Path(AI_CLEANED_FILE).exists():
        input_file = AI_CLEANED_FILE
        print(f"📂 Using AI-enhanced file for chunking: {input_file}")
    elif Path(MARKDOWN_FILE).exists():
        input_file = MARKDOWN_FILE
        print(f"📂 Using basic cleaned file for chunking: {input_file}")
    else:
        print("❌ No suitable input file found for chunking.")
        print("   Please run the full workflow first to create cleaned files.")
        return
    
    # Perform chunking
    chunk_file_for_rag(input_file)


def ask_about_chunking(input_file):
    """Ask user if they want to perform RAG chunking."""
    try:
        chunk = input("\n📂 Would you like to split the file into RAG-optimized chunks? (y/n): ").lower().strip()
        if chunk in ['y', 'yes']:
            chunk_file_for_rag(input_file)
        else:
            print("✅ Chunking skipped.")
    except (KeyboardInterrupt, EOFError):
        print("\n⚠️  Chunking skipped by user")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Script entry point.
    #
    # To use this script:
    # 1. Place your SRD PDF file in the same directory (or update INPUT_FILE in config)
    # 2. Set up your OpenAI API key (in config.py or environment variable)
    # 3. Run: python srd_processor.py
    # 4. Follow the interactive prompts to choose processing options
    #
    # For automated/non-interactive use, you can import and call functions directly:
    # - extract_text_by_layout() for PDF extraction
    # - clean_text_to_markdown() for basic cleanup
    # - ai_cleanup_by_pages() for AI enhancement
    # - chunk_file_for_rag() for RAG optimization
    
    main()
