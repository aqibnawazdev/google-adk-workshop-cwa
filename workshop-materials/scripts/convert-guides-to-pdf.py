#!/usr/bin/env python3
"""
Convert destination guide Markdown files to PDF for RAG corpus indexing.

This script converts all .md files in the destination-guides/ directory to PDF format,
preserving tables, lists, and formatting for optimal RAG chunking with Document AI parser.

Usage: python convert-guides-to-pdf.py

Requirements:
    pip install markdown2 weasyprint

Author: ADK Workshop Team
"""

import os
import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if required libraries are installed."""
    missing_deps = []

    try:
        import markdown2
    except ImportError:
        missing_deps.append('markdown2')

    try:
        import weasyprint
    except ImportError:
        missing_deps.append('weasyprint')

    if missing_deps:
        logger.error("Missing required dependencies!")
        logger.error(f"Please install: pip install {' '.join(missing_deps)}")
        sys.exit(1)


def convert_markdown_to_pdf(md_path: Path, output_dir: Path) -> Path:
    """
    Convert single Markdown file to PDF.

    Args:
        md_path: Path to source Markdown file
        output_dir: Directory to save PDF output

    Returns:
        Path to created PDF file
    """
    import markdown2
    from weasyprint import HTML, CSS

    logger.info(f"Converting: {md_path.name}")

    # Read Markdown content
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert Markdown to HTML with table support
    html_content = markdown2.markdown(
        md_content,
        extras=[
            'tables',           # Enable table parsing
            'fenced-code-blocks',
            'header-ids',
            'metadata',
        ]
    )

    # Create styled HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{md_path.stem.replace('-', ' ').title()}</title>
        <style>
            @page {{
                margin: 2cm;
                size: A4;
            }}
            body {{
                font-family: 'Helvetica', 'Arial', sans-serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
                margin-top: 0;
                font-size: 24pt;
            }}
            h2 {{
                color: #34495e;
                border-bottom: 2px solid #95a5a6;
                padding-bottom: 5px;
                margin-top: 20px;
                font-size: 18pt;
            }}
            h3 {{
                color: #34495e;
                margin-top: 15px;
                font-size: 14pt;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
                font-size: 10pt;
                page-break-inside: avoid;
            }}
            table th {{
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 8px;
                text-align: left;
                border: 1px solid #2980b9;
            }}
            table td {{
                padding: 6px 8px;
                border: 1px solid #bdc3c7;
            }}
            table tr:nth-child(even) {{
                background-color: #ecf0f1;
            }}
            ul, ol {{
                margin: 10px 0;
                padding-left: 25px;
            }}
            li {{
                margin: 5px 0;
            }}
            strong {{
                color: #2c3e50;
            }}
            code {{
                background-color: #ecf0f1;
                padding: 2px 5px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
            blockquote {{
                border-left: 4px solid #3498db;
                margin: 15px 0;
                padding: 10px 20px;
                background-color: #ecf0f1;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Generate PDF
    pdf_filename = md_path.stem + '.pdf'
    pdf_path = output_dir / pdf_filename

    HTML(string=full_html).write_pdf(
        pdf_path,
        presentational_hints=True
    )

    logger.info(f"  → Created: {pdf_filename}")
    return pdf_path


def main():
    """Main conversion logic."""
    # Check dependencies first
    check_dependencies()

    # Determine paths
    script_dir = Path(__file__).parent
    guides_dir = script_dir.parent / "destination-guides"
    output_dir = guides_dir / "pdf"

    logger.info("=" * 60)
    logger.info("Destination Guide PDF Conversion")
    logger.info("=" * 60)
    logger.info(f"Source directory: {guides_dir}")
    logger.info(f"Output directory: {output_dir}")
    logger.info("")

    # Verify source directory exists
    if not guides_dir.exists():
        logger.error(f"Destination guides directory not found: {guides_dir}")
        sys.exit(1)

    # Create output directory
    output_dir.mkdir(exist_ok=True)
    logger.info(f"Created output directory: {output_dir}")

    # Find all Markdown files (excluding README)
    md_files = [
        f for f in guides_dir.glob("*.md")
        if f.name.lower() != "readme.md"
    ]

    if not md_files:
        logger.warning(f"No Markdown files found in {guides_dir}")
        sys.exit(0)

    logger.info(f"Found {len(md_files)} guide(s) to convert")
    logger.info("")

    # Convert each file
    converted_count = 0
    failed_files = []

    for md_file in sorted(md_files):
        try:
            convert_markdown_to_pdf(md_file, output_dir)
            converted_count += 1
        except Exception as e:
            logger.error(f"Failed to convert {md_file.name}: {e}")
            failed_files.append(md_file.name)

    # Summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("Conversion Summary")
    logger.info("=" * 60)
    logger.info(f"✓ Successfully converted: {converted_count}/{len(md_files)} files")

    if failed_files:
        logger.warning(f"✗ Failed conversions: {len(failed_files)}")
        for filename in failed_files:
            logger.warning(f"  - {filename}")

    # List generated PDFs
    pdf_files = list(output_dir.glob("*.pdf"))
    logger.info(f"\nTotal PDFs in output directory: {len(pdf_files)}")
    logger.info(f"Output location: {output_dir.absolute()}")

    if converted_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
