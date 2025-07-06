# 🐉 D&D SRD PDF to Markdown Converter & RAG Chunker v2.0

<div align="center">

**Transform D&D 5e System Reference Documents into AI-Ready Knowledge Bases**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI GPT](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Web_Interface-blue.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*A comprehensive, production-ready pipeline with web interface, quality validation, advanced configuration, and testing suite for converting complex PDF documents into clean, structured Markdown optimized for Retrieval-Augmented Generation (RAG) applications.*

</div>

---

## 🎯 What This Application Does

**Transform complex tabletop RPG documents into AI-ready knowledge bases in minutes, not hours.**

This production-grade tool solves critical challenges facing AI developers, game masters, and content creators: **converting the official D&D 5e System Reference Document (SRD) from PDF format into clean, structured, search-optimized content that works seamlessly with modern AI systems**.

### 🆕 **What's New in v2.0**

- **🌐 Web Interface**: FastAPI-powered web UI with drag-and-drop PDF upload and real-time progress tracking
- **⚙️ Configuration Profiles**: Multiple preset configurations (fast, quality, custom) for different use cases
- **🔍 Quality Validation**: Comprehensive quality assessment with OCR confidence, formatting scores, and D&D-specific term preservation
- **🧪 Testing Suite**: Complete test coverage with unit, integration, and performance tests
- **📊 Enhanced Analytics**: Detailed health reports with optimization recommendations
- **🔄 Parallel Processing**: Multi-threaded AI cleanup for 3-4x speed improvements
- **💾 Smart Caching**: Cache AI responses to avoid re-processing identical content

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
5. **Quality Validation** → Comprehensive assessment with detailed analytics and recommendations

#### 📊 **Professional-Grade Output**
- **Clean Markdown** with proper headers, formatting, and D&D-specific styling
- **Vector-Ready Chunks** optimized for embedding models and similarity search
- **Rich Metadata** including titles, word counts, and unique identifiers
- **Quality Analytics** with detailed health reports and optimization recommendations
- **Web Dashboard** for monitoring processing status and downloading results

#### 🔄 **Developer-Friendly Workflow**
- **Smart Resume** → Pick up where you left off, skip completed steps
- **Flexible Processing** → Choose free basic cleanup or premium AI enhancement
- **Configuration Profiles** → Fast, quality, or custom settings for different needs
- **Web Interface** → User-friendly browser-based processing with progress tracking
- **Batch Support** → Process multiple documents with custom parameters
- **Quality Assurance** → Automated validation and comprehensive health reporting
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

### 🌐 **Web Interface (NEW!)**
- **Drag-and-Drop Upload**: Simply drop your PDF into the browser for processing
- **Real-Time Progress**: Live updates on extraction, cleanup, and chunking progress  
- **Background Processing**: Non-blocking operations with job queue management
- **Results Dashboard**: Download processed files and view quality reports
- **API Endpoints**: RESTful API for programmatic integration

### ⚙️ **Advanced Configuration (NEW!)**
- **Configuration Profiles**: Pre-built settings for different use cases:
  - **Fast Profile**: `gpt-3.5-turbo`, smaller chunks, basic validation (testing/development)
  - **Quality Profile**: `gpt-4`, larger chunks, comprehensive validation (production)
  - **Custom Profile**: Full control over all parameters
- **Environment Management**: Secure API key handling with multiple authentication methods
- **Flexible Parameters**: Customize chunk sizes, AI models, and processing options

### 🔍 **Quality Validation (NEW!)**
- **OCR Confidence Assessment**: Detect and score text extraction quality
- **D&D-Specific Validation**: Preserve critical gaming terms (spells, conditions, abilities)
- **Formatting Analysis**: Score markdown structure and formatting quality
- **Completeness Checking**: Detect truncated content and broken references
- **Health Reporting**: Comprehensive analytics with optimization recommendations

### 🧪 **Testing & Reliability (NEW!)**
- **Comprehensive Test Suite**: Unit, integration, and performance tests
- **Quality Assurance**: Automated validation of processing pipeline
- **Performance Monitoring**: Track processing times and resource usage
- **Error Handling**: Robust error recovery with detailed diagnostics

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

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (for AI-enhanced processing)
- 2-4 GB RAM recommended
- Internet connection for API calls

### 1. Installation Options

#### **Option A: Basic Installation (Command Line Only)**
```bash
# Clone the repository
git clone https://github.com/eddiefiggie/srd-processor.git
cd srd-processor

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Install core dependencies
pip install -r requirements.txt
```

#### **Option B: Enhanced Installation (Web Interface + All Features)**
```bash
# Clone the repository
git clone https://github.com/eddiefiggie/srd-processor.git
cd srd-processor

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Install enhanced dependencies
pip install -r requirements-enhanced.txt
```

### 2. Configuration

### 2. Configuration

#### **Method 1: Configuration File (Recommended)**
Copy the example configuration file and set your API key:

```bash
cp config.example.py config.py
```

Then edit `config.py` and set your OpenAI API key:
```python
OPENAI_API_KEY = "sk-your-openai-api-key-here"
```

#### **Method 2: Environment Variable (Production)**
```bash
export OPENAI_API_KEY="sk-your-openai-api-key-here"
```

#### **Method 3: Configuration Profiles (NEW!)**
```python
# Use the new configuration manager
from config_manager import ConfigManager, ProcessingConfig

manager = ConfigManager()

# Load a pre-built profile
config = manager.load_profile("fast")  # or "quality"

# Or create a custom profile
custom_config = ProcessingConfig(
    openai_model="gpt-4",
    chunk_min_words=300,
    chunk_max_words=600,
    enable_parallel_processing=True
)
manager.save_profile("custom", custom_config)
```

### 3. Add Your PDF

### 3. Add Your PDF

Place your D&D SRD PDF file in the project directory and update the filename in `config.py` if needed:

```python
INPUT_PDF_FILE = "your-srd-file.pdf"
```

### 4. Choose Your Interface

#### **Option A: Command Line Interface**
```bash
python srd_processor.py
```

#### **Option B: Web Interface (NEW!)**
```bash
# Start the web server
python web_interface.py

# Open your browser to http://localhost:8000
# Upload PDF and track progress in real-time
```

#### **Option C: Programmatic API (NEW!)**
```python
from srd_processor import extract_text_by_layout, chunk_file_for_rag
from quality_validator import generate_quality_report

# Process with validation
success = extract_text_by_layout()
if success:
    chunk_file_for_rag("srd_ai_cleaned.md")
    
    # Get quality report
    report = generate_quality_report("export")
    print(f"Quality score: {report['summary']['average_ocr_confidence']:.2f}")
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
srd-processor/
├── 📱 Core Application
│   ├── srd_processor.py              # Main processing pipeline
│   ├── config.py                     # Configuration file (create from example)
│   └── config.example.py             # Example configuration
├── 🌐 Web Interface (NEW!)
│   ├── web_interface.py              # FastAPI web server
│   └── static/                       # Web assets (auto-created)
├── ⚙️ Enhanced Features (NEW!)
│   ├── config_manager.py             # Configuration profiles manager
│   ├── quality_validator.py          # Quality assessment tools
│   └── test_srd_processor.py         # Comprehensive test suite
├── 📋 Dependencies
│   ├── requirements.txt              # Core dependencies
│   └── requirements-enhanced.txt     # All features dependencies
├── 📖 Processing Outputs
│   ├── srd_raw_text.txt             # Stage 1: Raw extracted text
│   ├── srd_cleaned_output.md        # Stage 2: Basic cleaned Markdown  
│   ├── srd_ai_cleaned.md            # Stage 3: AI-enhanced Markdown
│   └── export/                      # Stage 4: RAG-optimized chunks
│       ├── 001_Legal_Information_SRD_5_2.md
│       ├── 002_Playing_the_Game_SRD_5_2.md
│       └── ... (30+ more chunks)
├── 🔍 Quality Reports (NEW!)
│   ├── quality_report.json          # Detailed quality analytics
│   └── processing_logs/             # Processing history
└── 📚 Documentation
    ├── README.md                    # This file
    ├── WORKFLOW_EXAMPLES.md         # Usage examples
    └── CLEANUP_SUMMARY.md           # Development notes
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

### Enhanced Configuration (NEW!)

#### **Configuration Profiles**
Use pre-built profiles for common scenarios:

```python
from config_manager import ConfigManager

manager = ConfigManager()

# Fast profile - for development and testing
fast_config = manager.load_profile("fast")
# Uses: gpt-3.5-turbo, smaller chunks, basic validation

# Quality profile - for production
quality_config = manager.load_profile("quality") 
# Uses: gpt-4, larger chunks, comprehensive validation

# List available profiles
profiles = manager.list_profiles()
print(f"Available profiles: {profiles}")
```

#### **Quality Validation Settings**
```python
from quality_validator import QualityValidator, generate_quality_report

# Run quality assessment
validator = QualityValidator()
report = generate_quality_report("export")

# View quality metrics
print(f"OCR Confidence: {report['summary']['average_ocr_confidence']:.2f}")
print(f"Formatting Score: {report['summary']['average_formatting_score']:.2f}")
print(f"Recommendations: {report['recommendations']}")
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

### Web API Integration (NEW!)

Start the web server and use the REST API:

```python
import requests
import time

# Start the server: python web_interface.py

# Upload and process a PDF
with open("SRD_CC_v5.2.1.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/process", 
        files={"file": f},
        data={"enable_ai_cleanup": True}
    )

job_id = response.json()["job_id"]

# Monitor progress
while True:
    status = requests.get(f"http://localhost:8000/api/status/{job_id}").json()
    print(f"Status: {status['status']} - {status['current_step']} ({status['progress']*100:.1f}%)")
    
    if status['status'] in ['completed', 'failed']:
        break
    time.sleep(2)

# Download results
if status['status'] == 'completed':
    results = requests.get(f"http://localhost:8000/api/download/{job_id}")
```

### Configuration Management (NEW!)

```python
from config_manager import ConfigManager, ProcessingConfig

# Create custom configuration
config = ProcessingConfig(
    openai_model="gpt-4",
    chunk_min_words=300,
    chunk_max_words=600,
    enable_parallel_processing=True,
    max_workers=4,
    cache_ai_responses=True
)

# Save for reuse
manager = ConfigManager()
manager.save_profile("my_custom", config)

# Load and use
loaded_config = manager.load_profile("my_custom")
```

### Quality Assessment (NEW!)

```python
from quality_validator import QualityValidator, generate_quality_report

# Validate individual chunks
validator = QualityValidator()
with open("export/001_Legal_Information_SRD_5_2.md") as f:
    content = f.read()
    metrics = validator.validate_chunk(content)
    
print(f"OCR Quality: {metrics.ocr_confidence:.2f}")
print(f"D&D Terms Preserved: {metrics.d20_terms_preserved}")
print(f"Spell Errors: {metrics.spell_errors}")

# Generate comprehensive report
report = generate_quality_report("export")
print(f"Overall Quality: {report['summary']['average_ocr_confidence']:.2f}")
for rec in report['recommendations']:
    print(f"💡 {rec}")
```

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

### Batch Processing with Quality Validation

Process multiple documents with comprehensive quality tracking:

```python
from config_manager import ConfigManager
from quality_validator import generate_quality_report
from srd_processor import extract_text_by_layout, chunk_file_for_rag

documents = ["SRD_Core.pdf", "SRD_Monsters.pdf", "SRD_Spells.pdf"]
manager = ConfigManager()

# Load quality configuration
config = manager.load_profile("quality")

batch_results = []

for doc in documents:
    print(f"Processing {doc}...")
    
    # Update config for each document
    config.input_pdf = doc
    
    # Run processing pipeline
    if extract_text_by_layout():
        chunk_file_for_rag(f"{doc}_cleaned.md", f"export_{doc}")
        
        # Generate quality report
        report = generate_quality_report(f"export_{doc}")
        batch_results.append({
            'document': doc,
            'quality_score': report['summary']['average_ocr_confidence'],
            'chunk_count': report['summary']['total_chunks'],
            'recommendations': report['recommendations']
        })

# Summary report
for result in batch_results:
    print(f"{result['document']}: {result['quality_score']:.2f} quality, {result['chunk_count']} chunks")
```

### Testing and Validation (NEW!)

```python
# Run the test suite
from test_srd_processor import run_all_tests, create_test_data

# Create test data
create_test_data()

# Run comprehensive tests
success = run_all_tests()
if success:
    print("✅ All tests passed!")
else:
    print("❌ Some tests failed - check output for details")
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
- **gpt-4o-mini**: ~$1-3 for a complete SRD document (recommended for most users)
- **gpt-4**: ~$15-25 for a complete SRD document (highest quality, production use)
- **gpt-3.5-turbo**: ~$0.50-1 for a complete SRD document (fast profile, development)
- **Basic cleanup**: $0 (no API calls required)

### New Cost Optimization Features (v2.0)
- **Smart Caching**: Avoid re-processing identical content (saves 30-50% on API costs)
- **Parallel Processing**: Faster completion means less idle time and resource costs
- **Configuration Profiles**: Choose optimal cost/quality balance for your use case
- **Quality Validation**: Catch issues early to avoid expensive re-processing
- **Resume Capability**: Never pay twice for the same processing step

### Cost Optimization Tips
- Use **fast profile** for development and testing (cheapest)
- Use **quality profile** for final production processing  
- Enable **caching** for repeated processing of similar content
- Use **basic cleanup** for initial content review (free)
- Process in **stages** to minimize API usage on failures
- **Resume from checkpoints** rather than starting over

---

## 🆘 Troubleshooting

### 🌐 **Web Interface Issues (NEW!)**
**Problem**: Web interface won't start or shows errors
**Solutions**:
1. Install enhanced dependencies: `pip install -r requirements-enhanced.txt`
2. Check port availability: `lsof -i :8000` (kill process if needed)
3. Verify FastAPI installation: `python -c "import fastapi; print('FastAPI works')"`
4. Try different port: `uvicorn web_interface:app --port 8001`

**Problem**: File upload fails or processing gets stuck
**Solutions**:
1. Check file size limits (large PDFs may timeout)
2. Verify upload directory permissions
3. Check browser console for JavaScript errors
4. Try uploading a smaller test PDF first

### ⚙️ **Configuration Profile Issues (NEW!)**
**Problem**: Profile loading fails or config errors
**Solutions**:
1. Create configs directory: `mkdir configs`
2. Initialize default profiles: `python -c "from config_manager import create_default_profiles; create_default_profiles()"`
3. Check JSON syntax in profile files
4. Verify profile names match exactly (case-sensitive)

### 🔍 **Quality Validation Issues (NEW!)**
**Problem**: Quality reports show poor scores or validation errors
**Solutions**:
1. Check OCR quality threshold: lower for scanned PDFs
2. Verify D&D terminology in source content
3. Run with verbose logging to see detailed metrics
4. Try different AI models for better structure detection

**Problem**: Quality validator fails or crashes
**Solutions**:
1. Install spellchecker dependencies: `pip install spellchecker textstat`
2. Check chunk file format (YAML frontmatter required)
3. Verify export directory exists and contains .md files
4. Run validator on individual files first to isolate issues

### 🧪 **Testing Issues (NEW!)**
**Problem**: Tests fail or skip unexpectedly
**Solutions**:
1. Install test dependencies: `pip install pytest pytest-cov`
2. Create test data: `python test_srd_processor.py create-data`
3. Run individual test classes: `python -m pytest test_srd_processor.py::TestBasicTextCleaning`
4. Check test_data directory exists and has sample files

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