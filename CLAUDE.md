# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Essential Commands

### Development Setup

- `uv sync` - Set up Python environment and install dependencies
- `just` - List all available recipes/commands

### Code Quality and Testing

- `just lint` - Run all linters (ruff, mypy, vulture) at once
- `just format` - Run all auto-formatting tools
- `just test` - Run unit tests with pytest
- `just ruff-check` - Check Python code style
- `just mypy` - Type checking (excludes src/excel2xml)
- `just vulture` - Dead code analysis
- `just clean` - Remove artifact files

### Data Generation

- `uv run src/xmllib/main.py` - Generate the main XML file (data_daschland.xml) using new xmllib
- `uv run src/excel2xml/main_excel2xml.py` - Generate XML using legacy excel2xml module

### DSP-API Upload

Local upload:

```bash
dsp-tools create daschland.json
dsp-tools xmlupload -u cheshire.cat@dasch.swiss -p 'alice9548' data_daschland.xml
```

Test server (rdu-08):

```bash
dsp-tools create -s https://api.rdu-08.dasch.swiss -u root@example.com -p 'xxxx' daschland.json
dsp-tools xmlupload -s https://api.rdu-08.dasch.swiss -u cheshire.cat@dasch.swiss -p 'alice9548' data_daschland.xml
```

## DSP-TOOLS Overview

DSP-TOOLS is the command-line interface for the DaSCH Service Platform.
This project heavily relies on DSP-TOOLS for data model creation and upload workflows.

### Key DSP-TOOLS Commands Used

- `dsp-tools create` - Creates project data model on DSP server from JSON definition (`daschland.json`)
- `dsp-tools xmlupload` - Uploads resources and metadata from XML file (`data_daschland.xml`)
- `dsp-tools excel2json` - Converts Excel ontology files to JSON project definition (used for `daschland.json`)
- `dsp-tools validate-data` - Validates XML data against server ontology before upload

### DSP-TOOLS Workflow

1. **Project Setup**: `excel2json` converts ontology Excel files to `daschland.json`
2. **Model Creation**: `create` establishes the data model on the DSP server
3. **Data Upload**: `xmlupload` populates the project with resources and metadata
4. **Validation**: `validate-data` can verify XML structure before upload

### Important DSP-TOOLS Notes

- Creates `id2iri_mapping_[timestamp].json` files during upload for resource tracking
- Supports both local DSP instances and remote servers (like rdu-08)
- Authentication required for project creation and data upload
- XML files must conform to DSP ontology structure

## Development Workflow

### Pull Request Reviews

PRs in this repository are typically reviewed by:
- [@Notheturtle](https://github.com/Notheturtle)
- [@jnussbaum](https://github.com/jnussbaum)
- [@Nora-Olivia-Ammann](https://github.com/Nora-Olivia-Ammann)

## Architecture Overview

This is a DaSCH Service Platform (DSP) example project called "Alice in DaSCHland"
that demonstrates data modeling and upload workflows.
The project converts multimedia and metadata about Lewis Carroll's Alice books
into formats suitable for the DSPplatform.

### Core Data Flow

1. **Spreadsheets** (`data/spreadsheets/`) contain structured data for different resource types
2. **Two parallel conversion paths**:
   - **Modern**: `src/xmllib/` uses new dsp-tools xmllib for XML generation
   - **Legacy**: `src/excel2xml/` uses old dsp-tools excel2xml module
3. **Output**: Both generate XML files for upload to DSP-API servers
4. **Mirror**: NodeGoat CSV files are automatically updated for parallel project

### Key Components

- **Resource Types**: Archive, Audio, AudioSegment, Book, BookChapter, BookCover, BookEdition, Character,
  Documentation, Event, Image, Location, Material, Region, Video, VideoSegment
- **Data Sources**: Excel spreadsheets in `data/spreadsheets/`
- **Multimedia Files**: Organized in `data/multimedia/` by type (audio, image, video, etc.)
- **Ontology**: Defined in `daschland_ontology/` Excel files, compiled to `daschland.json`

### Important Notes

- Requires Git LFS for large multimedia files
- Uses uv for Python environment management
- ExifTool required for metadata extraction
- MyPy excludes `src/excel2xml` due to legacy code issues
- NodeGoat files are automatically updated when running main XML generation
