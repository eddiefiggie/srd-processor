# Smart Workflow Resume Examples

## NEW in v2.0: Multiple Interface Options

### Web Interface Example
```bash
# Start the web server
python web_interface.py

# Browser output:
🌐 Starting FastAPI server on http://localhost:8000
📱 Upload PDFs via web interface
📊 Real-time progress tracking
📥 Download results when complete
```

### Configuration Profile Example
```python
# Use different profiles for different needs
from config_manager import ConfigManager

manager = ConfigManager()

# Development: Fast and cheap
config = manager.load_profile("fast")
# Uses: gpt-3.5-turbo, smaller chunks, basic validation

# Production: High quality
config = manager.load_profile("quality") 
# Uses: gpt-4, larger chunks, comprehensive validation
```

### Quality Validation Example
```python
# Check processing quality
from quality_validator import generate_quality_report

report = generate_quality_report("export")
print(f"Quality Score: {report['summary']['average_ocr_confidence']:.2f}")
print(f"Recommendations: {report['recommendations']}")
```

## Command Line Interface Examples

## Example 1: First Run (No Files)
```
🔍 Checking existing files...
📋 Current Workflow Status:
   ❌ Raw text extraction (srd_raw_text.txt)
   ❌ Basic cleanup (srd_cleaned_output.md)
   ❌ AI cleanup (srd_ai_cleaned.md)
   ❌ RAG chunking (export/ directory)

📋 No existing files found - will start from PDF extraction.
```

## Example 2: Partial Progress (Raw Text Exists)
```
🔍 Checking existing files...
📋 Current Workflow Status:
   ✅ Raw text extraction (srd_raw_text.txt)
   ❌ Basic cleanup (srd_cleaned_output.md)
   ❌ AI cleanup (srd_ai_cleaned.md)
   ❌ RAG chunking (export/ directory)

📑 Raw text exists but no cleaned files found.
Would you like to:
  1. Start fresh (re-extract PDF)
  2. Resume from basic cleanup step
  3. Exit
Choice (1/2/3):
```

## Example 3: Most Work Done (Ready for Chunking)
```
🔍 Checking existing files...
📋 Current Workflow Status:
   ✅ Raw text extraction (srd_raw_text.txt)
   ✅ Basic cleanup (srd_cleaned_output.md)
   ✅ AI cleanup (srd_ai_cleaned.md)
   ❌ RAG chunking (export/ directory)

📄 AI-cleaned file exists but no chunks found.
Would you like to:
  1. Start fresh (re-extract and re-process everything)
  2. Just create RAG chunks from existing AI-cleaned file
  3. Exit
Choice (1/2/3):
```

## Example 4: Everything Complete
```
🔍 Checking existing files...
📋 Current Workflow Status:
   ✅ Raw text extraction (srd_raw_text.txt)
   ✅ Basic cleanup (srd_cleaned_output.md)
   ✅ AI cleanup (srd_ai_cleaned.md)
   ✅ RAG chunking (export/ directory)

🎉 All workflow steps appear to be complete!
Would you like to:
  1. Start fresh (overwrite existing files)
  2. Re-run chunking only
  3. Exit
Choice (1/2/3):
```

## Benefits of Smart Resume

1. **Time Saving**: Never re-extract PDF or re-process files unnecessarily
2. **Cost Saving**: Avoid re-running expensive AI cleanup if already done
3. **Flexibility**: Jump to any step you want (e.g., just chunking)
4. **Safe**: Always asks before overwriting existing work
5. **Clear Status**: Shows exactly what's been done and what's missing
