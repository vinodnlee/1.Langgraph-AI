# LangGraph Workflow Diagrams

## 📊 Main Workflow Architecture

```mermaid
graph TD
    A[🚀 START] --> B[🔍 Input Processor]
    B --> |processed_text| C[🔄 Data Transformer]
    C --> |transformed_text| D[📤 Output Generator]
    D --> E[🏁 END]
    
    subgraph "State Variables"
        F[input_text]
        G[processed_text]
        H[transformed_text]
        I[output_text]
        J[step]
    end
    
    subgraph "Node Functions"
        B1[Clean & Format Input<br/>Add Processing Context]
        C1[LLM Enhancement<br/>Fallback Logic]
        D1[Final Formatting<br/>Result Generation]
    end
    
    B -.-> B1
    C -.-> C1
    D -.-> D1
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style E fill:#fce4ec
```

## 🔄 Data Flow Sequence

```mermaid
sequenceDiagram
    participant User
    participant Workflow
    participant IP as Input Processor
    participant DT as Data Transformer
    participant OG as Output Generator
    
    User->>Workflow: input_text
    Workflow->>IP: {"input_text": "Hello World"}
    IP->>IP: Process & format
    IP-->>Workflow: {"processed_text": "PROCESSING: HELLO WORLD"}
    
    Workflow->>DT: Pass state with processed_text
    DT->>DT: Transform with LLM or fallback
    DT-->>Workflow: {"transformed_text": "✨ ENHANCED: ..."}
    
    Workflow->>OG: Pass state with transformed_text
    OG->>OG: Generate final formatted output
    OG-->>Workflow: {"output_text": "📋 RESULT..."}
    
    Workflow-->>User: Complete result state
```

## 🏗️ Project Architecture

```mermaid
flowchart LR
    subgraph "LangGraph Project"
        subgraph "Core Files"
            M[main.py<br/>3-Node Workflow]
            A[advanced_example.py<br/>Conditional Routing]
            N[test_workflow.ipynb<br/>Interactive Testing]
        end
        
        subgraph "Configuration"
            L[langgraph.json<br/>Studio Config]
            R[requirements.txt<br/>Dependencies]
            E[.env<br/>Environment Variables]
        end
        
        subgraph "LangGraph Studio"
            S[Visual Debugger<br/>http://127.0.0.1:2024]
            API[API Docs<br/>/docs endpoint]
        end
    end
    
    M --> L
    A --> L
    L --> S
    R --> M
    E --> M
    N --> M
    
    style M fill:#e3f2fd
    style A fill:#f1f8e9
    style S fill:#fff8e1
    style L fill:#fce4ec
```

## 🎯 Advanced Workflow with Conditional Routing

```mermaid
graph TD
    START[🚀 START] --> ROUTER{🔀 Router<br/>Conditional Logic}
    
    ROUTER -->|"contains 'urgent'"| PRIORITY[🚨 Priority Processor]
    ROUTER -->|"contains 'simple'"| SIMPLE[📝 Simple Processor]
    ROUTER -->|"default"| STANDARD[⚙️ Standard Processor]
    
    PRIORITY --> END1[🏁 END]
    SIMPLE --> END2[🏁 END]
    STANDARD --> END3[🏁 END]
    
    style START fill:#e1f5fe
    style ROUTER fill:#fff9c4
    style PRIORITY fill:#ffebee
    style SIMPLE fill:#e8f5e9
    style STANDARD fill:#e3f2fd
```

## 📝 State Diagram

```mermaid
stateDiagram-v2
    [*] --> started: Initialize
    started --> input_processed: input_processor()
    input_processed --> data_transformed: data_transformer()
    data_transformed --> output_generated: output_generator()
    output_generated --> [*]: Complete
    
    note right of started
        Initial State:
        - input_text
        - empty processed_text
        - empty transformed_text
        - empty output_text
    end note
    
    note right of output_generated
        Final State:
        - input_text
        - processed_text
        - transformed_text
        - output_text (complete)
    end note
```

## 🔍 Node Details

### Input Processor Node
- **Input**: `input_text`
- **Process**: Clean, format, and add context
- **Output**: `processed_text`
- **Example**: "hello" → "PROCESSING: HELLO"

### Data Transformer Node
- **Input**: `processed_text`
- **Process**: LLM enhancement (with fallback)
- **Output**: `transformed_text`
- **Example**: "PROCESSING: HELLO" → "✨ TRANSFORMED: ENHANCED: HELLO ✨"

### Output Generator Node
- **Input**: `transformed_text`
- **Process**: Final formatting with metadata
- **Output**: `output_text`
- **Example**: Creates complete formatted result

## 🎨 Viewing These Diagrams

### In VS Code:
1. Install "Markdown Preview Mermaid Support" extension
2. Right-click this file → "Open Preview"
3. Diagrams will render beautifully

### In GitHub:
- GitHub natively renders Mermaid diagrams in Markdown files
- Just commit and push this file

### Online:
- Copy diagram code to https://mermaid.live
- Export as PNG/SVG for presentations

## 🚀 Quick Reference

**Workflow Path**: START → input_processor → data_transformer → output_generator → END

**State Flow**: input_text → processed_text → transformed_text → output_text

**Files**: main.py (basic) | advanced_example.py (routing) | test_workflow.ipynb (testing)
