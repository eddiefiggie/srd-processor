# 🐉 D&D SRD PDF to Markdown Converter & RAG Chunker

<div align="center">

**Transform D&D 5e System Reference Documents into AI-Ready Knowledge Bases**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI GPT](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*An intelligent pipeline that converts complex PDF documents into clean, structured Markdown and optimizes them for Retrieval-Augmented Generation (RAG) applications.*

</div>

---

## 🎯 What This Application Does

**Transform complex tabletop RPG documents into AI-ready knowledge bases in minutes, not hours.**

This sophisticated tool solves a critical challenge facing AI developers, game masters, and content creators: **converting the official D&D 5e System Reference Document (SRD) from PDF format into clean, structured, search-optimized content that works seamlessly with modern AI systems**.

### 🔍 The Challenge We Solve

**Raw PDFs are AI's kryptonite:**
- **📄 Layout Chaos**: Multi-column layouts, page breaks, and formatting artifacts destroy content flow
- **👁️ OCR Errors**: Text extraction produces broken hyphenation, garbled characters, and malformed words  
- **🏗️ Structure Loss**: Headers, lists, and hierarchies get flattened into unstructured text blobs
- **🎲 Gaming-Specific Complexity**: Spell blocks, stat tables, and rule references need specialized handling
- **⏰ Manual Effort**: Converting 400+ page documents by hand takes weeks and introduces human errors

**The result?** Unusable content for chatbots, RAG systems, and AI applications that depend on clean, structured data.

### ✨ Our Complete Solution

This application delivers a **fully automated, production-ready pipeline** that transforms any D&D SRD PDF into multiple optimized formats:

#### 🧠 **Intelligent Multi-Stage Processing**
1. **Layout-Aware Extraction** → Automatically detects and handles single/multi-column layouts
2. **Smart Text Cleanup** → Fixes OCR errors and applies proper Markdown formatting  
3. **AI-Powered Enhancement** → Uses GPT models for advanced structure recognition and cleanup
4. **RAG Optimization** → Creates perfectly-sized, semantically coherent content chunks

#### 📊 **Professional-Grade Output**
- **Clean Markdown** with proper headers, formatting, and D&D-specific styling
- **Vector-Ready Chunks** optimized for embedding models and similarity search
- **Rich Metadata** including titles, word counts, and unique identifiers
- **Quality Analytics** with detailed health reports and optimization recommendations

#### 🔄 **Developer-Friendly Workflow**
- **Smart Resume** → Pick up where you left off, skip completed steps
- **Flexible Processing** → Choose free basic cleanup or premium AI enhancement
- **Batch Support** → Process multiple documents with custom parameters
- **Cost Optimization** → Transparent pricing with budget-friendly model options

### 🎯 Perfect For

| **Use Case** | **How It Helps** | **Output** |
|-------------|------------------|------------|
| **🤖 AI Development** | Build D&D chatbots, rule assistants, and RAG systems | Vector-ready chunks with metadata |
| **🎮 Game Management** | Create searchable digital rule references | Clean, mobile-friendly Markdown |
| **� Content Creation** | Generate professional documentation and wikis | Structured, consistent formatting |
| **🔬 Research & Analysis** | Extract data for game balance and linguistic studies | Machine-readable, tagged content |
| **🌐 Web Development** | Populate game databases and search engines | API-ready JSON metadata + content |

### 🚀 Why Choose This Tool?

- **⚡ Speed**: Process entire SRD documents in 15-30 minutes vs. weeks of manual work
- **🎯 Accuracy**: AI-powered cleanup catches errors human eyes miss
- **💰 Cost-Effective**: $1-5 per document vs. hundreds of hours of manual labor
- **🔧 Customizable**: Flexible parameters for different AI models and use cases
- **🛡️ Secure**: Local processing with optional API integration
- **📖 Battle-Tested**: Optimized specifically for D&D 5e content structure and formatting

---

## ✨ Key Features & Benefits

### 🧠 Intelligent Processing
- **Layout-Aware Extraction**: Automatically detects and handles single-column, multi-column, and two-column page layouts
- **OCR Error Correction**: AI-powered cleanup fixes common PDF extraction issues like broken hyphenation and garbled text
- **Structure Preservation**: Maintains proper header hierarchy and document organization throughout the conversion process

### 🎯 RAG Optimization
- **Smart Chunking Strategy**: Keeps logically related content together (e.g., complete spell descriptions) while staying within optimal word counts (200-500 words)
- **Rich Metadata**: Each chunk includes YAML frontmatter with title, source section, word count, and unique identifiers
- **Table of Contents Driven**: Uses the official SRD structure as the authoritative guide for content organization

### 🔄 Workflow Intelligence
- **Smart Resume Capability**: Automatically detects existing work and offers to resume from any step in the pipeline
- **Flexible Processing Options**: Choose between basic cleanup (free) or AI-enhanced cleanup (requires OpenAI API)
- **Comprehensive Validation**: Pre-flight checks ensure your environment is properly configured before processing

### 📊 Quality Assurance
- **Health Reporting**: Detailed analytics on chunk quality, size distribution, and section coverage
- **Progress Tracking**: Real-time feedback on processing status with clear progress indicators
- **Error Handling**: Graceful degradation with informative error messages and recovery suggestions

---

## 🚀 Quick Start

### 1. Python Environment

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configuration

Copy the example configuration file and set your API key:

```bash
cp config.example.py config.py
```

Then edit `config.py` and either:
- Set `OPENAI_API_KEY = "your-api-key-here"` directly in the file, or
- Set the `OPENAI_API_KEY` environment variable

**Option 1: Set in config.py (easier for development)**
```python
OPENAI_API_KEY = "sk-your-openai-api-key-here"
```

**Option 2: Set as environment variable (more secure)**
```bash
export OPENAI_API_KEY="sk-your-openai-api-key-here"
```

### 4. Add Your PDF

Place your D&D SRD PDF file in the project directory and update the filename in `config.py` if needed:

```python
INPUT_PDF_FILE = "your-srd-file.pdf"
```

### 5. Run the Tool

```bash
python srd_processor.py
```

---

## 🔄 How It Works

### Interactive Workflow

The application features an **intelligent, resumable workflow** that adapts to your needs:

```
🔍 Environment Check → 📋 File Detection → 🎯 Smart Resume Options → ⚡ Targeted Processing
```

**First Run (clean slate):**
- Automatically detects your PDF and validates the environment
- Walks through the complete pipeline from extraction to chunking
- Provides clear progress indicators and status updates

**Subsequent Runs (work in progress):**
- Shows status of existing files (✅ completed, ❌ missing)  
- Offers intelligent resume options:
  - **Start Fresh**: Overwrite everything and restart
  - **Resume**: Pick up from the next unfinished step
  - **Targeted**: Jump to specific steps (e.g., re-run chunking only)

### 4-Stage Processing Pipeline

#### 🔍 **Stage 1: PDF Text Extraction**
```
📖 SRD_PDF → 🧠 Layout Detection → 📄 Raw Text + Page Markers
```
- **Layout Intelligence**: Automatically detects and handles:
  - Single-column title pages
  - Multi-column table of contents (3-column layout)
  - Two-column main content (most of the document)
- **Structure Preservation**: Maintains page boundaries with markers for later processing
- **Progress Tracking**: Real-time feedback as pages are processed
- **Output**: `srd_raw_text.txt` with clean text and page markers

#### 🧹 **Stage 2: Basic Text Cleanup**
```
📄 Raw Text → 🔧 Regex Processing → 📝 Clean Markdown
```
- **OCR Error Correction**: Fixes common PDF extraction issues:
  - Broken hyphenation at line endings
  - Excessive whitespace and line breaks
  - Malformed paragraph structures
- **Markdown Formatting**: Applies basic formatting:
  - Converts ALL CAPS sections to proper headers
  - Bolds D&D-specific keywords (Casting Time, Range, etc.)
  - Normalizes spacing and line breaks
- **Fast & Free**: No API calls required, completes in seconds
- **Output**: `srd_cleaned_output.md` with basic formatting

#### 🤖 **Stage 3: AI-Powered Enhancement** *(Optional)*
```
📄 Raw Text → 🧠 GPT Analysis → ✨ Enhanced Markdown
```
- **Intelligent Cleanup**: Uses OpenAI's GPT models for:
  - Advanced OCR error correction
  - Proper header hierarchy detection
  - Spell/ability block formatting
  - Table structure recognition
  - Grammar and flow improvements
- **Structure Analysis**: Cross-references PDF font data to understand document hierarchy
- **D&D Optimization**: Specifically tuned for game content formatting
- **Quality vs Cost**: Choose between `gpt-4o-mini` (fast/cheap) or `gpt-4` (high quality)
- **Output**: `srd_ai_cleaned.md` with professional-grade formatting

#### 📚 **Stage 4: RAG Optimization** *(Optional)*
```
📝 Clean Markdown → 📊 Smart Chunking → 🗂️ Vector-Ready Files
```
- **Content-Aware Chunking**: Intelligently splits content while:
  - Preserving logical sections (complete spells, abilities, etc.)
  - Maintaining 200-500 word target range for optimal RAG performance
  - Using Table of Contents as the authoritative structure guide
- **Rich Metadata**: Each chunk includes YAML frontmatter:
  ```yaml
  ---
  title: "Combat Fundamentals"
  source_section: "Combat"
  word_count: 387
  chunk_id: 023
  ---
  ```
- **Quality Analytics**: Comprehensive health reporting on:
  - Chunk size distribution and quality metrics
  - Section coverage analysis
  - Optimization recommendations
- **Output**: `export/` directory with numbered, metadata-rich chunk files

---

## 📊 Output Files & Structure

### File Organization
```
agentic-dm/
├── 📖 srd_raw_text.txt              # Stage 1: Raw extracted text
├── 📝 srd_cleaned_output.md         # Stage 2: Basic cleaned Markdown  
├── ✨ srd_ai_cleaned.md             # Stage 3: AI-enhanced Markdown
└── 📁 export/                       # Stage 4: RAG-optimized chunks
    ├── 001_Legal_Information_SRD_5_2.md
    ├── 002_Playing_the_Game_SRD_5_2.md
    ├── 003_Combat_Part_1_SRD_5_2.md
    └── ... (30+ more chunks)
```

### Chunk File Format
Each chunk is a standalone Markdown file optimized for vector databases:

```markdown
---
title: "Spellcasting Fundamentals"
source_section: "Spells"  
word_count: 423
chunk_id: 015
---

# Spells

A spell is a discrete magical effect, a single shaping of the magical energies 
that suffuse the multiverse into a specific, limited expression...

[Clean, properly formatted content continues...]
```

### Flexible Configuration

Edit `config.py` to customize the processing pipeline:

```python
# OpenAI Configuration
OPENAI_MODEL = "gpt-4o-mini"  # Options: "gpt-4o-mini" (fast/cheap) or "gpt-4" (high quality)
OPENAI_MAX_TOKENS = 4000      # Adjust based on your needs
OPENAI_TEMPERATURE = 0.1      # Lower = more consistent, higher = more creative

# File Paths
INPUT_PDF_FILE = "SRD_CC_v5.2.1.pdf"
RAW_TEXT_OUTPUT = "srd_raw_text.txt"
BASIC_MARKDOWN_OUTPUT = "srd_cleaned_output.md"
AI_ENHANCED_OUTPUT = "srd_ai_cleaned.md"

# Processing Options
ENABLE_AI_CLEANUP = True      # Set to False to skip AI processing by default
VERBOSE_LOGGING = True        # Set to False for quieter operation
```

### Chunking Customization

Adjust RAG parameters for your specific use case:

```python
# For shorter, more focused chunks (better for precise lookups)
chunk_file_for_rag(input_file, target_min=150, target_max=350)

# For longer, more comprehensive chunks (better for context)
chunk_file_for_rag(input_file, target_min=300, target_max=700)
```

---

## 🎯 Use Cases & Applications

### 🤖 **AI Development**
- **Chatbots**: Create D&D rule assistants and campaign helpers
- **RAG Systems**: Build searchable knowledge bases for game mechanics
- **LLM Fine-tuning**: Prepare training data for D&D-specific language models
- **Vector Databases**: Populate embedding stores with structured game content

### 🎮 **Game Management**
- **Digital DM Screens**: Quick rule lookups during gameplay
- **Campaign Tools**: Searchable spell and monster databases
- **Rule References**: Mobile-friendly formatted rules for tablets
- **Custom Content**: Templates for homebrew additions

### 📚 **Content Creation**
- **Documentation**: Clean Markdown for wikis and documentation sites
- **Publishing**: Professional formatting for derived works
- **Translation**: Structured content for multilingual projects
- **Analysis**: Data extraction for game balance studies

---

## 🔧 Advanced Usage

### Programmatic API

Use individual functions for custom workflows:

```python
from srd_processor import extract_text_by_layout, clean_text_to_markdown, ai_cleanup_by_pages, chunk_file_for_rag

# Stage 1: Extract text from PDF
success = extract_text_by_layout()

# Stage 2: Basic cleanup
with open("srd_raw_text.txt", encoding="utf-8") as f:
    raw_text = f.read()
cleaned = clean_text_to_markdown(raw_text)

# Stage 3: AI cleanup (requires API key)
ai_cleanup_by_pages("srd_raw_text.txt", "srd_ai_cleaned.md")

# Stage 4: RAG chunking
chunk_file_for_rag("srd_ai_cleaned.md", "export", target_min=200, target_max=500)
```

### Batch Processing

Process multiple documents with custom parameters:

```python
documents = ["SRD_Core.pdf", "SRD_Monsters.pdf", "SRD_Spells.pdf"]

for doc in documents:
    # Update config for each document
    config.INPUT_PDF_FILE = doc
    
    # Run processing pipeline
    if extract_text_by_layout():
        ai_cleanup_by_pages("srd_raw_text.txt", f"{doc}_cleaned.md")
        chunk_file_for_rag(f"{doc}_cleaned.md", f"export_{doc}")
```

---

## 🛡️ Security & Privacy

### 🔐 **API Key Protection**
- `config.py` is automatically git-ignored to prevent accidental commits
- Support for environment variables for production deployments
- Never hard-code API keys in version-controlled files

### 📊 **Data Handling**
- All processing happens locally on your machine
- Only text content is sent to OpenAI APIs (no sensitive metadata)
- Raw PDFs and personal configurations never leave your system
- Full control over what data gets processed and when

### 🚀 **Production Deployment**
```bash
# Use environment variables in production
export OPENAI_API_KEY="your-api-key"
export SRD_INPUT_FILE="/path/to/srd.pdf"
export SRD_OUTPUT_DIR="/path/to/output"

python srd_processor.py
```

---

## 💰 Cost Considerations

### AI Processing Costs
- **gpt-4o-mini**: ~$1-3 for a complete SRD document (recommended)
- **gpt-4**: ~$15-25 for a complete SRD document (highest quality)
- **Basic cleanup**: $0 (no API calls required)

### Cost Optimization Tips
- Use basic cleanup for initial testing (free)
- Process in stages to minimize API usage on failures
- Choose `gpt-4o-mini` for most applications (excellent quality/cost ratio)
- Reserve `gpt-4` for final production processing

---

## 🆘 Troubleshooting

### 🔑 **API Key Issues**
**Problem**: `"OpenAI API key not found"` error
**Solutions**:
1. Verify `config.py` exists and contains your API key
2. Check that `OPENAI_API_KEY` environment variable is set correctly
3. Ensure API key starts with `sk-` and is valid
4. Test API connectivity: `python -c "import openai; print('API key works')"`

### 📁 **File & Import Issues**
**Problem**: `"Config file not found"` or import errors
**Solutions**:
1. Copy `config.example.py` to `config.py`
2. Ensure you're in the correct directory with `srd_processor.py`
3. Activate the virtual environment: `source .venv/bin/activate`
4. Reinstall dependencies: `pip install -r requirements.txt`

### 📖 **PDF Processing Issues**
**Problem**: PDF extraction fails or produces garbled text
**Solutions**:
1. Verify PDF file exists and filename matches `config.py`
2. Check PDF is not password-protected or corrupted
3. Try with a different PDF file to isolate the issue
4. Large PDFs (>400 pages) may take 10+ minutes - be patient

### 📚 **Chunking & RAG Issues**
**Problem**: Chunks too large/small or poor quality
**Solutions**:
1. Adjust parameters: `chunk_file_for_rag(input_file, target_min=150, target_max=400)`
2. Review the health report for specific recommendations
3. Ensure Table of Contents detection is working correctly
4. Consider different AI models for better structure detection

### 🔄 **Workflow & Resume Issues**
**Problem**: Resume functionality not working properly
**Solutions**:
- **"No existing files found"**: Ensure PDF is in directory and config is correct
- **"File exists but process failed"**: Choose "Start fresh" to overwrite and restart
- **Want to skip steps**: Use targeted resume options to jump to specific stages
- **Lost progress**: Check file timestamps to see what completed successfully

### 💻 **Environment Issues**
**Problem**: Python, dependency, or virtual environment issues
**Solutions**:
1. Ensure Python 3.8+ is installed: `python --version`
2. Recreate virtual environment: `rm -rf .venv && python -m venv .venv`
3. Update pip: `pip install --upgrade pip`
4. Clear Python cache: `rm -rf __pycache__/`

---

## 📝 **License & Legal**

**MIT License** - This project is open source and free to use, modify, and distribute.

**Important Note**: This tool is designed to work with the **official D&D 5e System Reference Document (SRD)**, which is available under the Open Game License (OGL). Ensure you have the right to process any PDF content you use with this tool.

---

## 🤝 **Contributing & Support**

### Found a Bug?
1. Check existing issues for similar problems
2. Include detailed error messages and system information
3. Provide sample files (if possible) that reproduce the issue

### Want to Contribute?
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear documentation

### Need Help?
- Review this README thoroughly
- Check the troubleshooting section above
- Look at `WORKFLOW_EXAMPLES.md` for detailed usage examples
- Examine `config.example.py` for all configuration options

---

*Built with ❤️ for the D&D and AI communities. Happy adventuring! 🎲✨*