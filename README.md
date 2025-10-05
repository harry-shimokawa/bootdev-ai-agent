# 🤖 AI Agent - File Operations & Code Assistant

A sophisticated AI-powered agent built with Google's Gemini AI that can autonomously perform file operations, execute Python code, debug issues, and enhance codebases through iterative function calling.

## 🌟 Features

### Core Capabilities
- **📁 File System Operations**: List directories, read files, write content securely within working directory boundaries
- **🐍 Python Code Execution**: Run Python scripts with timeout protection and argument passing
- **🔄 Iterative Conversations**: Continuous multi-step reasoning with up to 20 iterations
- **🛡️ Security Boundaries**: All operations constrained to `./calculator` working directory for safety
- **🎯 Function Calling**: Advanced Google GenAI function calling with proper schema declarations

### Advanced AI Capabilities
- **🔍 Bug Detection & Fixing**: Automatically identify and resolve code issues
- **📊 Code Analysis**: Deep inspection of project structure and logic
- **⚡ Feature Enhancement**: Add new functionality like mathematical operations
- **🔧 Code Refactoring**: Improve code quality, add type hints, and enhance maintainability
- **📝 Documentation Generation**: Create comprehensive project documentation

## 🏗️ Architecture

### Function System
The agent has access to four core functions:

1. **`get_files_info`** - List directory contents with file sizes
2. **`get_file_content`** - Read file contents with security validation  
3. **`write_file`** - Create/update files within working directory
4. **`run_python_file`** - Execute Python scripts with timeout protection

### Conversation Loop
```
User Prompt → AI Analysis → Function Calls → Tool Results → AI Analysis → ... → Final Response
```

The agent maintains conversation history and can make multiple function calls to solve complex problems iteratively.

## 📋 Requirements

- Python 3.12+
- UV package manager
- Google Gemini API key
- Required packages: `google-genai`, `python-dotenv`

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/harry-shimokawa/bootdev-ai-agent.git
   cd bootdev-ai-agent
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Set up environment**:
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

4. **Verify installation**:
   ```bash
   uv run main.py "list files in the current directory"
   ```

## 💡 Usage Examples

### Basic File Operations
```bash
# List directory contents
uv run main.py "what files are in the root directory?"

# Read file contents  
uv run main.py "show me the contents of main.py"

# Create new files
uv run main.py "create a new file called hello.py with a simple print statement"
```

### Code Analysis & Debugging
```bash
# Investigate code structure
uv run main.py "how does the calculator render results to the console?"

# Debug issues
uv run main.py "fix the bug: 3 + 7 * 2 shouldn't be 20"

# Run tests
uv run main.py "run the test suite and report results"
```

### Advanced Operations  
```bash
# Add new features
uv run main.py "Add support for exponentiation and modulo operations to the calculator"

# Code refactoring
uv run main.py "refactor the calculator code to add type hints and better error handling"

# Verbose output for detailed conversation flow
uv run main.py "analyze the project structure" --verbose
```

## 🎯 Example: Autonomous Bug Fixing

1. **Introduce a bug** (operator precedence):
   ```python
   # Change in calculator/pkg/calculator.py
   self.precedence = {"+": 3, "-": 1, "*": 2, "/": 2}  # Wrong!
   ```

2. **Agent detects and fixes**:
   ```bash
   uv run main.py "The calculator returns 20 for '3 + 7 * 2' instead of 17. Please investigate and fix."
   ```

3. **Agent workflow**:
   - Lists files to understand structure
   - Reads calculator code to find the issue
   - Identifies incorrect operator precedence
   - Fixes the precedence values
   - Tests the solution
   - Reports successful fix

## 🛡️ Security Features

### Working Directory Isolation
- All file operations restricted to `./calculator` directory
- Path traversal protection prevents access outside boundaries
- No system-level operations or network access

### Execution Safety
- Python execution limited to 30-second timeout
- No access to dangerous modules or system functions
- Error handling prevents crashes and data corruption

### API Rate Limiting
- Respects Google Gemini API rate limits
- Graceful handling of quota exceeded errors
- Automatic retry logic with proper delays

## ⚠️ Safety Warnings

**🚨 IMPORTANT SECURITY NOTICE 🚨**

This is a **demonstration/educational tool**. DO NOT use in production environments without additional security measures:

- **File System Access**: The agent can read, write, and execute files within the working directory
- **Code Execution**: Can run arbitrary Python code with potential for system interaction
- **Data Exposure**: May access sensitive files within the working directory
- **API Costs**: Function calls consume API quota and may incur charges

### Recommended Precautions
- ✅ Run in isolated environments only
- ✅ Never use with sensitive data
- ✅ Monitor API usage and costs
- ✅ Review generated code before execution
- ✅ Use proper access controls and permissions
- ❌ Do not share this tool with untrusted users
- ❌ Do not run in production environments

## 🧪 Testing

The project includes comprehensive tests:

```bash
# Run individual function tests
uv run python test_functions.py

# Test calculator functionality
uv run calculator/main.py "3 + 7 * 2"

# Run agent conversation tests
bootdev run ad0f349e-4426-4658-b3f5-7e7bbce2ae48
```

## 🗂️ Project Structure

```
bootdev-ai-agent/
├── main.py                 # Main AI agent application
├── config.py              # Configuration constants  
├── functions/              # Function implementations
│   ├── get_files_info.py   # Directory listing
│   ├── get_file_content.py # File reading
│   ├── write_file.py       # File writing
│   ├── run_python_file.py  # Python execution
│   └── system_prompt.py    # AI system instructions
├── calculator/             # Working directory & test app
│   ├── main.py            # Calculator application
│   ├── pkg/
│   │   ├── calculator.py  # Calculator logic
│   │   └── render.py      # Output formatting
│   └── tests.py           # Calculator tests
└── tests/                 # Agent tests
```

## 🔄 Development Workflow

This project demonstrates the complete lifecycle of building an AI agent:

1. **Basic Function Calling** - Individual tool usage
2. **Schema Declaration** - Proper API integration
3. **Conversation System** - Iterative multi-turn interactions  
4. **Agent Behavior** - Autonomous problem-solving
5. **Advanced Features** - Complex reasoning and code manipulation

## 📈 Performance & Limitations

### Capabilities
- ✅ Multi-step reasoning (up to 20 iterations)
- ✅ Complex code analysis and modification
- ✅ Autonomous bug detection and fixing
- ✅ New feature implementation
- ✅ Comprehensive error handling

### Current Limitations
- ⚠️ Single working directory constraint
- ⚠️ Limited to text-based file operations
- ⚠️ Python execution only (no other languages)
- ⚠️ API rate limiting (15 requests/minute on free tier)
- ⚠️ No persistent memory between sessions

## 🤝 Contributing

This is an educational project demonstrating AI agent capabilities. Contributions welcome for:

- Enhanced security features
- Additional function implementations
- Better error handling
- Performance improvements
- Documentation updates

## 📄 License

This project is provided for educational purposes. Please ensure responsible use and comply with Google's AI usage policies.

## 🙏 Acknowledgments

- Built with [Google Gemini AI](https://ai.google.dev/gemini-api)
- Inspired by modern AI agent architectures like Cursor, Claude Code, and Zed's Agentic Mode
- Developed as part of the BootDev AI Agent course

---

**Remember**: This tool provides AI agents with file system access and code execution capabilities. Always use in controlled environments and never with sensitive data! 🛡️
