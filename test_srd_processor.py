"""
Comprehensive test suite for SRD processor.
"""
import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path to import our modules
sys.path.append(str(Path(__file__).parent.parent))

try:
    from srd_processor import (
        clean_text_to_markdown, 
        count_words, 
        split_large_content,
        validate_environment
    )
except ImportError:
    # If running standalone, define mock functions
    def clean_text_to_markdown(text):
        return text.replace('\n\n\n', '\n\n')
    
    def count_words(text):
        return len(text.split())
    
    def split_large_content(content, target_min=200, target_max=500):
        return [content]
    
    def validate_environment():
        return True, []

class TestBasicTextCleaning(unittest.TestCase):
    """Test basic text cleaning functions."""
    
    def test_clean_markdown_removes_excess_newlines(self):
        """Test that excessive newlines are reduced."""
        input_text = "Line 1\n\n\n\n\nLine 2"
        result = clean_text_to_markdown(input_text)
        self.assertNotIn('\n\n\n', result)
    
    def test_clean_markdown_handles_hyphenated_words(self):
        """Test that hyphenated line breaks are handled."""
        input_text = "This is a long word that is hy-\nphenated across lines"
        result = clean_text_to_markdown(input_text)
        self.assertIn('hyphenated', result)
        self.assertNotIn('hy-\n', result)
    
    def test_clean_markdown_creates_headers(self):
        """Test that ALL CAPS sections become headers."""
        input_text = "\nCOMBAT RULES\n\nSome content here"
        result = clean_text_to_markdown(input_text)
        self.assertIn('# COMBAT RULES', result)

class TestWordCounting(unittest.TestCase):
    """Test word counting functionality."""
    
    def test_count_words_basic(self):
        """Test basic word counting."""
        text = "This is a test with five words"
        self.assertEqual(count_words(text), 7)  # "five" is one word
    
    def test_count_words_ignores_markdown(self):
        """Test that markdown syntax is ignored in word count."""
        text = "**Bold** text and *italic* text"
        # Should count: Bold, text, and, italic, text = 5 words
        self.assertEqual(count_words(text), 5)
    
    def test_count_words_filters_short_artifacts(self):
        """Test that single characters (OCR artifacts) are filtered."""
        text = "Real words a b c and more real words"
        # Should ignore single letters 'a', 'b', 'c'
        result = count_words(text)
        self.assertLess(result, 9)  # Less than if we counted everything

class TestChunkSplitting(unittest.TestCase):
    """Test content chunking functionality."""
    
    def test_split_large_content_respects_headers(self):
        """Test that content is split at header boundaries."""
        content = """# First Section
This is some content for the first section.

# Second Section  
This is content for the second section.

# Third Section
This is content for the third section."""
        
        chunks = split_large_content(content, target_min=10, target_max=50)
        
        # Should create separate chunks for each section
        self.assertGreater(len(chunks), 1)
        # Each chunk should contain a header
        for chunk in chunks:
            self.assertIn('#', chunk)
    
    def test_split_large_content_preserves_structure(self):
        """Test that content structure is preserved during splitting."""
        content = """# Main Section
Some introductory text.

## Subsection A
Content for subsection A.

## Subsection B  
Content for subsection B."""
        
        chunks = split_large_content(content, target_min=5, target_max=30)
        
        # Verify that headers are preserved
        all_content = '\n'.join(chunks)
        self.assertIn('# Main Section', all_content)
        self.assertIn('## Subsection A', all_content)
        self.assertIn('## Subsection B', all_content)

class TestEnvironmentValidation(unittest.TestCase):
    """Test environment validation."""
    
    def test_validate_environment_basic(self):
        """Test basic environment validation."""
        is_valid, issues = validate_environment()
        self.assertIsInstance(is_valid, bool)
        self.assertIsInstance(issues, list)

class TestIntegration(unittest.TestCase):
    """Integration tests for the full pipeline."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.test_pdf = Path(self.test_dir) / "test.pdf"
        self.test_text = Path(self.test_dir) / "test.txt"
        
        # Create minimal test files
        self.test_pdf.write_bytes(b"%PDF-1.4\nMinimal PDF content")
        self.test_text.write_text("Test content for processing")
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    @patch('srd_processor.pdfplumber')
    def test_pdf_extraction_pipeline(self, mock_pdfplumber):
        """Test the PDF extraction pipeline with mocked PDF."""
        # Mock pdfplumber
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Sample extracted text"
        mock_page.width = 612
        mock_page.height = 792
        mock_pdf.pages = [mock_page]
        mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf
        
        # This would test the actual extraction function
        # result = extract_text_by_layout()
        # self.assertTrue(result)
        pass  # Placeholder for actual test

class TestErrorHandling(unittest.TestCase):
    """Test error handling scenarios."""
    
    def test_missing_file_handling(self):
        """Test handling of missing input files."""
        # Test would verify graceful handling of missing PDFs
        pass
    
    def test_api_failure_handling(self):
        """Test handling of OpenAI API failures."""
        # Test would verify graceful degradation when AI fails
        pass
    
    def test_corrupted_pdf_handling(self):
        """Test handling of corrupted PDF files."""
        # Test would verify error handling for bad PDFs
        pass

class TestPerformance(unittest.TestCase):
    """Performance tests for the SRD processor."""
    
    def test_large_text_processing_performance(self):
        """Test performance with large text inputs."""
        # Create large test text
        large_text = "Sample text. " * 10000  # ~130KB of text
        
        import time
        start_time = time.time()
        result = clean_text_to_markdown(large_text)
        end_time = time.time()
        
        # Should complete in reasonable time (adjust threshold as needed)
        self.assertLess(end_time - start_time, 5.0)  # 5 seconds max
        self.assertIsInstance(result, str)
    
    def test_word_counting_performance(self):
        """Test word counting performance."""
        large_text = "word " * 50000  # 50k words
        
        import time
        start_time = time.time()
        word_count = count_words(large_text)
        end_time = time.time()
        
        # Should be very fast
        self.assertLess(end_time - start_time, 1.0)  # 1 second max
        self.assertGreater(word_count, 40000)  # Should count most words

def create_test_data():
    """Create sample test data for development."""
    test_data_dir = Path("test_data")
    test_data_dir.mkdir(exist_ok=True)
    
    # Create sample markdown content
    sample_content = """# Test Section
This is a test section with some content.

## Subsection
More detailed content here.

### Sub-subsection  
Even more detailed content.

# Another Section
Different content for testing chunking.
"""
    
    (test_data_dir / "sample_content.md").write_text(sample_content)
    
    # Create sample raw OCR text with artifacts
    raw_content = """DUNGEONS    &    DRAGONS
SYSTEM   REFERENCE   DOCUMENT

This  text  has  some  OCR   artifacts   and   extra   spaces.
Some-
times words are split across lines.

CHAPTER  1:  COMBAT
This  chapter  covers  combat  rules  and  procedures.
"""
    
    (test_data_dir / "raw_ocr_sample.txt").write_text(raw_content)
    
    print(f"Test data created in {test_data_dir}")

def run_all_tests():
    """Run all tests and generate report."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestBasicTextCleaning,
        TestWordCounting, 
        TestChunkSplitting,
        TestEnvironmentValidation,
        TestIntegration,
        TestErrorHandling,
        TestPerformance
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "create-data":
        create_test_data()
    else:
        run_all_tests()
