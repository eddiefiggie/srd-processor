# 🆕 SRD Processor v2.0 - New Features Guide

## Overview

This document provides detailed information about the new features introduced in SRD Processor v2.0, including setup instructions, usage examples, and best practices.

---

## 🌐 Web Interface

### Features
- **Drag-and-Drop Upload**: Simply drag your PDF into the browser
- **Real-Time Progress**: Live updates during processing with progress bars
- **Background Processing**: Non-blocking operations with job queue
- **Results Dashboard**: View and download processed files
- **Quality Reports**: Visual display of processing quality metrics

### Setup and Usage

1. **Install Dependencies**:
   ```bash
   pip install -r requirements-enhanced.txt
   ```

2. **Start the Web Server**:
   ```bash
   python web_interface.py
   ```

3. **Access the Interface**:
   - Open your browser to `http://localhost:8000`
   - Upload your SRD PDF file
   - Monitor progress in real-time
   - Download results when complete

### API Endpoints

- `GET /`: Main web interface
- `POST /api/process`: Upload and start processing
- `GET /api/status/{job_id}`: Check processing status
- `GET /api/download/{job_id}`: Download results

### Example API Usage

```python
import requests
import time

# Upload file
with open("SRD_CC_v5.2.1.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/process",
        files={"file": f},
        data={"enable_ai_cleanup": True, "chunk_min_words": 200}
    )

job_id = response.json()["job_id"]

# Poll for completion
while True:
    status = requests.get(f"http://localhost:8000/api/status/{job_id}").json()
    if status['status'] == 'completed':
        break
    time.sleep(2)
```

---

## ⚙️ Configuration Profiles

### Available Profiles

#### **Fast Profile** (Development/Testing)
- Model: `gpt-3.5-turbo`
- Chunk size: 150-350 words
- Features: Basic validation, parallel processing
- Cost: ~$0.50-1 per document
- Use case: Quick testing, development

#### **Quality Profile** (Production)
- Model: `gpt-4`
- Chunk size: 300-700 words  
- Features: Comprehensive validation, retry logic
- Cost: ~$15-25 per document
- Use case: Final production output

### Using Profiles

```python
from config_manager import ConfigManager, ProcessingConfig

# Initialize manager
manager = ConfigManager()

# Load existing profile
config = manager.load_profile("fast")
print(f"Using model: {config.openai_model}")

# Create custom profile
custom = ProcessingConfig(
    openai_model="gpt-4o-mini",
    chunk_min_words=250,
    chunk_max_words=550,
    enable_parallel_processing=True,
    max_workers=6,
    cache_ai_responses=True
)

# Save for later use
manager.save_profile("custom_production", custom)

# List all profiles
profiles = manager.list_profiles()
print(f"Available: {profiles}")
```

### Creating Custom Profiles

```python
# Development profile with caching
dev_config = ProcessingConfig(
    openai_model="gpt-3.5-turbo",
    chunk_min_words=100,
    chunk_max_words=300,
    cache_ai_responses=True,
    retry_attempts=1,
    enable_parallel_processing=False  # Easier debugging
)

# High-quality profile with validation
premium_config = ProcessingConfig(
    openai_model="gpt-4",
    chunk_min_words=400,
    chunk_max_words=800,
    ocr_quality_threshold=0.9,
    retry_attempts=5,
    enable_parallel_processing=True,
    max_workers=2  # Fewer workers for gpt-4
)
```

---

## 🔍 Quality Validation

### Features
- **OCR Confidence**: Assess text extraction quality
- **D&D Term Preservation**: Track gaming-specific terminology
- **Formatting Analysis**: Score markdown structure quality
- **Completeness Detection**: Find truncated or incomplete content
- **Health Reporting**: Comprehensive analytics with recommendations

### Basic Usage

```python
from quality_validator import QualityValidator, generate_quality_report

# Validate individual chunk
validator = QualityValidator()
with open("export/001_Legal_Information_SRD_5_2.md") as f:
    content = f.read()
    
metrics = validator.validate_chunk(content)
print(f"OCR Confidence: {metrics.ocr_confidence:.2f}")
print(f"Formatting Score: {metrics.formatting_score:.2f}")
print(f"D&D Terms Found: {metrics.d20_terms_preserved}")
print(f"Potential Errors: {metrics.spell_errors}")
```

### Comprehensive Quality Report

```python
# Generate full report for all chunks
report = generate_quality_report("export")

# Summary statistics
summary = report['summary']
print(f"Total Chunks: {summary['total_chunks']}")
print(f"Average OCR Confidence: {summary['average_ocr_confidence']:.2f}")
print(f"Average Formatting Score: {summary['average_formatting_score']:.2f}")
print(f"Total Errors Found: {summary['total_spell_errors']}")

# Quality assessment
if summary['average_ocr_confidence'] > 0.8:
    print("🟢 Excellent OCR quality")
elif summary['average_ocr_confidence'] > 0.6:
    print("🟡 Good OCR quality")
else:
    print("🔴 Poor OCR quality - consider using higher quality source")

# Recommendations
for rec in report['recommendations']:
    print(f"💡 {rec}")
```

### Advanced Validation

```python
# Custom validation with thresholds
class CustomValidator(QualityValidator):
    def __init__(self):
        super().__init__()
        # Add custom D&D terms
        self.d20_terms['custom_spells'] = [
            'eldritch blast', 'healing word', 'magic missile'
        ]
    
    def validate_chunk(self, content: str) -> QualityMetrics:
        metrics = super().validate_chunk(content)
        
        # Custom validation logic
        if 'spell' in content.lower() and metrics.d20_terms_preserved < 3:
            metrics.completeness_score *= 0.8  # Penalize incomplete spells
            
        return metrics

# Use custom validator
custom_validator = CustomValidator()
```

---

## 🧪 Testing Suite

### Running Tests

```python
# Run all tests
from test_srd_processor import run_all_tests

success = run_all_tests()
if success:
    print("✅ All tests passed!")
```

### Test Categories

#### **Unit Tests**
- Text cleaning functions
- Word counting accuracy
- Chunk splitting logic
- Configuration validation

#### **Integration Tests**
- Full pipeline processing
- File input/output operations
- API integration tests
- Error handling scenarios

#### **Performance Tests**
- Large document processing
- Memory usage validation
- Processing time benchmarks
- Concurrent operation tests

### Creating Test Data

```python
from test_srd_processor import create_test_data

# Generate sample test files
create_test_data()

# This creates:
# - test_data/sample_content.md
# - test_data/raw_ocr_sample.txt
# - test_data/corrupted_sample.pdf (for error testing)
```

### Custom Test Cases

```python
import unittest
from test_srd_processor import TestBasicTextCleaning

class TestCustomFunctionality(unittest.TestCase):
    def test_quality_validation(self):
        """Test that quality validation works correctly."""
        from quality_validator import QualityValidator
        
        validator = QualityValidator()
        
        # Test high-quality content
        good_content = "# Combat\n\nCombat in D&D follows structured turns..."
        metrics = validator.validate_chunk(good_content)
        self.assertGreater(metrics.ocr_confidence, 0.8)
        
        # Test low-quality content
        bad_content = "C0mb@t 1n D&D f0ll0ws str|_|ctur3d t|_|rns..."
        metrics = validator.validate_chunk(bad_content)
        self.assertLess(metrics.ocr_confidence, 0.5)

# Run specific test
if __name__ == "__main__":
    unittest.main()
```

---

## 🚀 Performance Enhancements

### Parallel Processing

```python
from config_manager import ProcessingConfig

# Enable parallel processing for AI cleanup
config = ProcessingConfig(
    enable_parallel_processing=True,
    max_workers=4  # Adjust based on your system
)

# Process multiple pages concurrently
# Typically 3-4x faster than sequential processing
```

### Caching System

```python
# Enable response caching to avoid re-processing
config = ProcessingConfig(
    cache_ai_responses=True,
    # Cached responses stored in .cache/ directory
)

# Subsequent runs with identical content will use cache
# Saves 30-50% on API costs for similar documents
```

### Memory Optimization

```python
# For large documents, enable memory optimization
config = ProcessingConfig(
    # Process in smaller chunks to reduce memory usage
    chunk_max_words=400,  # Smaller chunks = less memory
    
    # Enable streaming for very large files
    stream_processing=True
)
```

---

## 📊 Monitoring and Analytics

### Processing Metrics

```python
from quality_validator import generate_quality_report
import json

# Generate detailed analytics
report = generate_quality_report("export")

# Save metrics for tracking
with open("quality_metrics.json", "w") as f:
    json.dump(report, f, indent=2, default=str)

# Track metrics over time
metrics_history = {
    "timestamp": datetime.now(),
    "document": "SRD_CC_v5.2.1.pdf",
    "quality_score": report['summary']['average_ocr_confidence'],
    "chunk_count": report['summary']['total_chunks'],
    "processing_time": processing_time,
    "api_cost": estimated_cost
}
```

### Health Monitoring

```python
# Monitor processing health
def check_processing_health():
    health_checks = {
        "api_connectivity": test_openai_connection(),
        "file_permissions": test_file_write_permissions(),
        "memory_usage": get_memory_usage(),
        "disk_space": get_available_disk_space()
    }
    
    return all(health_checks.values()), health_checks

is_healthy, checks = check_processing_health()
if not is_healthy:
    print("⚠️ Health check failed:")
    for check, status in checks.items():
        if not status:
            print(f"  ❌ {check}")
```

---

## 🔧 Integration Examples

### Django Integration

```python
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from config_manager import ConfigManager
from srd_processor import extract_text_by_layout, chunk_file_for_rag

@csrf_exempt
def process_srd(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['pdf']
        
        # Save file temporarily
        with open(f"temp_{uploaded_file.name}", "wb") as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        
        # Process with SRD processor
        config = ConfigManager().load_profile("fast")
        success = extract_text_by_layout()
        
        if success:
            chunk_file_for_rag("srd_ai_cleaned.md")
            return JsonResponse({"status": "success"})
        
        return JsonResponse({"status": "error"})
```

### Flask Integration

```python
# app.py
from flask import Flask, request, jsonify
from quality_validator import generate_quality_report

app = Flask(__name__)

@app.route('/api/quality-report/<path:export_dir>')
def quality_report(export_dir):
    try:
        report = generate_quality_report(export_dir)
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 🛡️ Security Considerations

### API Key Management

```python
# Use environment variables in production
import os
from config_manager import ProcessingConfig

config = ProcessingConfig(
    # Never hardcode API keys
    openai_api_key=os.getenv('OPENAI_API_KEY'),
    
    # Use secure storage for production
    config_dir="/secure/path/configs"
)
```

### Input Validation

```python
# Validate PDF files before processing
def validate_pdf_input(file_path):
    """Validate PDF file before processing."""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            if header != b'%PDF':
                raise ValueError("Invalid PDF file")
        
        # Check file size (max 100MB)
        file_size = os.path.getsize(file_path)
        if file_size > 100 * 1024 * 1024:
            raise ValueError("File too large")
            
        return True
    except Exception as e:
        print(f"PDF validation failed: {e}")
        return False
```

### Output Sanitization

```python
# Sanitize output for web display
import html
import re

def sanitize_chunk_content(content):
    """Sanitize chunk content for safe web display."""
    # Remove potential script tags
    content = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
    
    # Escape HTML entities
    content = html.escape(content)
    
    # Allow safe markdown
    safe_tags = ['#', '*', '_', '`', '[', ']', '(', ')']
    
    return content
```

---

## 📈 Best Practices

### Development Workflow

1. **Start with Fast Profile**: Use `fast` profile for initial development
2. **Enable Caching**: Set `cache_ai_responses=True` to save costs
3. **Validate Early**: Run quality validation on small samples first
4. **Test Incrementally**: Use the test suite to validate changes
5. **Monitor Costs**: Track API usage and costs during development

### Production Deployment

1. **Use Quality Profile**: Switch to `quality` profile for production
2. **Environment Variables**: Store API keys securely
3. **Health Monitoring**: Implement health checks and monitoring
4. **Error Handling**: Set up proper error logging and alerting
5. **Backup Strategy**: Backup processed files and configurations

### Performance Optimization

1. **Right-size Workers**: 2-4 workers for gpt-4, 4-8 for gpt-3.5-turbo
2. **Enable Caching**: Significant cost savings for repeated processing
3. **Tune Chunk Sizes**: Larger chunks = fewer API calls but slower processing
4. **Monitor Memory**: Watch memory usage with large documents
5. **Use Profiles**: Match profile to use case (fast vs quality)

---

*This completes the comprehensive guide to SRD Processor v2.0 features. For additional support, see the main README.md or submit an issue on GitHub.*
