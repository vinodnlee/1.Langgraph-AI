# 🏗️ Project Structure - Industry Standard

This document explains the professional folder structure of this LangGraph project.

## 📁 Directory Structure

```
langgraph-AI/
├── src/                          # Source code package
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration management
│   ├── models/                  # Data models and type definitions
│   │   └── __init__.py         # GraphState definition
│   ├── nodes/                   # Node implementations
│   │   └── __init__.py         # All workflow nodes
│   └── workflows/               # Workflow definitions
│       ├── __init__.py         # Workflow exports
│       ├── basic_workflow.py   # 3-node sequential workflow
│       └── advanced_workflow.py # Conditional routing workflow
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_nodes.py           # Node unit tests
│   ├── test_workflows.py       # Workflow integration tests
│   └── test_config.py          # Configuration tests
│
├── notebooks/                   # Jupyter notebooks
│   └── test_workflow.ipynb     # Interactive testing notebook
│
├── docs/                        # Documentation
│   ├── DIAGRAMS.md             # Mermaid diagrams
│   ├── API.md                  # API documentation
│   └── DEPLOYMENT.md           # Deployment guide
│
├── scripts/                     # Utility scripts
│   ├── setup.sh                # Environment setup
│   └── lint.sh                 # Code linting
│
├── .github/                     # GitHub configuration
│   ├── copilot-instructions.md # Copilot workspace instructions
│   └── workflows/              # CI/CD workflows
│
├── .vscode/                     # VS Code configuration
│   ├── launch.json             # Debug configurations
│   ├── settings.json           # Project settings
│   └── tasks.json              # Build tasks
│
├── run_basic.py                 # Entry point for basic workflow
├── run_advanced.py              # Entry point for advanced workflow
├── langgraph.json               # LangGraph Studio configuration
├── requirements.txt             # Python dependencies
├── requirements-dev.txt         # Development dependencies
├── setup.py                     # Package setup
├── pyproject.toml              # Modern Python project config
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

## 🎯 Design Principles

### 1. **Separation of Concerns**
- **models/**: Pure data structures and type definitions
- **nodes/**: Business logic for individual processing steps
- **workflows/**: Orchestration and graph composition
- **config.py**: Centralized configuration management

### 2. **Modularity**
- Each component is independently testable
- Clear interfaces between modules
- Easy to extend with new nodes or workflows

### 3. **Scalability**
- Organized structure supports growth
- Easy to add new workflows without affecting existing ones
- Clear import paths and dependencies

### 4. **Maintainability**
- Consistent naming conventions
- Comprehensive documentation
- Type hints throughout
- Proper error handling

## 📦 Package Structure

### `src/` - Main Source Package

#### `config.py`
- Environment variable loading
- LLM initialization
- Configuration constants
- Singleton pattern for shared resources

#### `models/`
- `GraphState`: TypedDict defining workflow state structure
- Shared type definitions
- Data validation schemas

#### `nodes/`
- `input_processor_node`: Text preprocessing
- `data_transformer_node`: LLM-based transformation
- `output_generator_node`: Final formatting
- Each node is a pure function: `(GraphState) -> GraphState`

#### `workflows/`
- `basic_workflow.py`: Linear 3-node pipeline
- `advanced_workflow.py`: Conditional branching logic
- `create_*_workflow()`: Factory functions for graph creation
- `run_workflow()`: Helper for execution

## 🔄 Data Flow

```
User Input
    ↓
Config (Load Environment)
    ↓
Workflow Factory (Create Graph)
    ↓
Node 1 (Process State)
    ↓
Node 2 (Transform State)
    ↓
Node 3 (Generate Output)
    ↓
Final Result
```

## 🧪 Testing Strategy

### Unit Tests (`tests/test_nodes.py`)
- Test each node in isolation
- Mock external dependencies (LLM)
- Verify state transformations

### Integration Tests (`tests/test_workflows.py`)
- Test complete workflow execution
- Verify end-to-end data flow
- Test conditional routing

### Configuration Tests (`tests/test_config.py`)
- Verify environment loading
- Test configuration validation
- Mock API key scenarios

## 🚀 Entry Points

### `run_basic.py`
- Demonstrates basic 3-node workflow
- Simple CLI interface
- Example usage

### `run_advanced.py`
- Shows conditional routing
- Multiple test cases
- Advanced patterns

## 📝 Import Patterns

### Absolute Imports (Recommended)
```python
from src.models import GraphState
from src.nodes import input_processor_node
from src.workflows.basic_workflow import run_workflow
```

### Package Imports
```python
from src import create_langgraph_workflow, run_workflow
```

## 🔧 Configuration Management

### Environment Variables
- Stored in `.env` (git-ignored)
- Template in `.env.example`
- Loaded via `python-dotenv`
- Centralized in `src/config.py`

### Configuration Class
```python
from src.config import Config, llm

# Access configuration
api_key = Config.OPENAI_API_KEY
temperature = Config.LLM_TEMPERATURE

# Use shared LLM instance
response = llm.invoke(messages)
```

## 📊 Dependency Management

### Production Dependencies (`requirements.txt`)
- Core libraries needed to run the application
- LangGraph, LangChain, OpenAI

### Development Dependencies (`requirements-dev.txt`)
- Testing frameworks (pytest)
- Linting tools (ruff, mypy)
- Documentation generators (mkdocs)

## 🎨 Code Style

### Conventions
- **PEP 8** compliance
- **Type hints** for all functions
- **Docstrings** (Google style)
- **Max line length**: 88 characters (Black standard)

### Linting Tools
- **ruff**: Fast Python linter
- **mypy**: Static type checking
- **black**: Code formatting

## 🔄 Migration from Old Structure

Old structure:
```
├── main.py                    # Monolithic file
└── advanced_example.py       # Separate example
```

New structure:
```
├── src/
│   ├── config.py             # Extracted configuration
│   ├── models/               # Extracted types
│   ├── nodes/                # Extracted node logic
│   └── workflows/            # Organized workflows
├── run_basic.py              # Clean entry point
└── run_advanced.py           # Clean entry point
```

## 🌟 Benefits

1. **Better Organization**: Clear structure, easy to navigate
2. **Improved Testability**: Isolated components
3. **Enhanced Maintainability**: Easier to update and extend
4. **Professional Standards**: Follows Python best practices
5. **Team Collaboration**: Clear ownership and responsibilities
6. **CI/CD Ready**: Structured for automated testing and deployment

## 📚 Further Reading

- [Python Application Layouts](https://realpython.com/python-application-layouts/)
- [Structuring Your Project](https://docs.python-guide.org/writing/structure/)
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/)
