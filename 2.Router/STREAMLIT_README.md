# 🤖 LangGraph Streamlit Chat Application

A beautiful, interactive chat interface for the LangGraph Router with LLM agent and tool integration.

## ✨ Features

- 💬 **Interactive Chat Interface**: User-friendly conversation UI
- 🤖 **LLM Agent**: Powered by GPT-4o-mini for intelligent responses
- 🔧 **Tool Integration**: Automatic multiply tool calling when needed
- 🎯 **Smart Routing**: Agent decides when to use tools vs direct response
- 📊 **Real-time Stats**: Track messages and tool calls
- 🎨 **Clean Design**: Modern, responsive UI with custom styling
- 💾 **Conversation History**: Maintains context across messages

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

Create a `.env` file with your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key_here
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

### Example Questions to Try:

**Multiplication (Uses Tool):**
- "What is 15 multiplied by 8?"
- "Calculate 25 times 4"
- "Multiply 100 by 50"

**General Questions (Direct Response):**
- "What is the capital of France?"
- "Tell me about Python programming"
- "Explain machine learning"

## 🎨 Interface Components

### Main Chat Area
- **User Messages**: Blue background, displays your questions
- **Assistant Messages**: Gray background, shows AI responses
- **Tool Calls**: Orange background, indicates when tools are used

### Sidebar Features
- **About Section**: Information about the agent and capabilities
- **Statistics**: Real-time message and tool call counts
- **Clear Chat**: Reset conversation and start fresh
- **Message Details**: Toggle to see internal message structure

## 🏗️ Architecture

```
User Input
    ↓
[Input Node] → Creates HumanMessage
    ↓
[Agent Node] → LLM analyzes and decides:
    ├─→ [ToolNode] → Executes multiply tool
    │       ↓
    │   [Agent Node] → Formats result
    └─→ [Output Node] → Direct response
         ↓
    Final Answer
```

## 🔧 Technical Details

### State Management
- **Session State**: Maintains conversation history and workflow instance
- **Message History**: Full conversation context for multi-turn interactions
- **Conversation Memory**: Agent has access to previous messages

### Workflow Integration
- Uses the same `create_workflow()` from `main.py`
- Preserves message history across turns
- Automatic state management for seamless conversations

### Error Handling
- Graceful error messages displayed in chat
- Try-catch blocks for robust operation
- User-friendly error descriptions

## 📁 Project Structure

```
2.Router/
├── app.py                    # Streamlit chat application
├── main.py                   # LangGraph workflow definition
├── requirements.txt          # Dependencies including streamlit
├── .env                      # API keys (not in git)
└── src/
    ├── models/
    │   └── graph_state.py   # State definition
    ├── nodes/
    │   ├── input_node.py    # Input processor
    │   └── output_node.py   # Output generator
    └── tools/
        └── multiply.py       # Multiply tool
```

## 🎯 Features Explained

### Smart Tool Routing
The agent automatically determines when to use the multiply tool:
- Detects multiplication questions in natural language
- Extracts numbers from the question
- Calls tool and formats the result naturally

### Conversation Context
The app maintains full conversation history:
- Multi-turn conversations
- Agent remembers previous questions
- Context-aware responses

### Visual Feedback
- **Spinner**: Shows when agent is processing
- **Tool Call Badges**: Highlights when tools are used
- **Message Styling**: Different colors for different message types
- **Real-time Updates**: Instant response display

## 🔍 Monitoring & Debugging

### Sidebar Stats
- Track total messages sent
- Count tool invocations
- Monitor conversation length

### Message Details Toggle
Enable "Show Message Details" to see:
- Internal message types (HumanMessage, AIMessage, ToolMessage)
- Message content snippets
- Tool call indicators

## 🛠️ Customization

### Styling
Edit the CSS in `st.markdown()` section to customize:
- Colors and backgrounds
- Border styles
- Font sizes
- Layout spacing

### Agent Behavior
Modify `main.py` to:
- Add more tools
- Change LLM model
- Adjust temperature/parameters
- Add custom routing logic

### UI Components
Extend `app.py` to add:
- File upload for documents
- Image generation
- Voice input/output
- Export conversation

## 🚨 Troubleshooting

### "Module not found: streamlit"
```bash
pip install streamlit
```

### "OpenAI API key not found"
Make sure `.env` file exists with:
```
OPENAI_API_KEY=sk-...
```

### "Workflow not working"
Verify `main.py` is in the same directory as `app.py`

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

## 📝 Tips

1. **Clear Chat**: Use the sidebar button to reset and start fresh
2. **Tool Testing**: Try various multiplication questions to see tool calling
3. **Context**: Ask follow-up questions that reference previous messages
4. **Experimentation**: Mix calculation and general questions

## 🔄 Development Mode

Run with auto-reload for development:

```bash
streamlit run app.py --server.runOnSave true
```

## 📊 Performance

- **Fast Response**: Optimized for quick interactions
- **Lightweight**: Minimal memory footprint
- **Scalable**: Can handle long conversations
- **Stateful**: Maintains context efficiently

## 🎓 Learn More

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangGraph Guide](https://langchain-ai.github.io/langgraph/)
- [LangChain Tools](https://python.langchain.com/docs/modules/tools/)

---

**Built with ❤️ using LangGraph, LangChain, and Streamlit**

**Ready to chat? Run `streamlit run app.py` and start asking questions!** 🚀
