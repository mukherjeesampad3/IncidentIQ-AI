# 🧠 Enterprise ITSM AI Assistant

An intelligent IT Service Management assistant that integrates with ServiceNow and leverages AI to analyze incidents, provide recommendations, and automate ticket creation.

## 📋 Features

- **Incident Analysis**: Automatically analyze ServiceNow incidents using AI
- **Smart Recommendations**: Get root cause analysis and resolution steps based on historical data
- **Incident Creation**: Create new incidents through natural language processing
- **Similar Incident Detection**: Find and analyze similar historical incidents
- **Web Interface**: User-friendly Streamlit interface for easy interaction
- **REST API**: Flask-based API for programmatic access

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: Streamlit
- **AI Engine**: Ollama (Local LLM)
- **ITSM Integration**: ServiceNow REST API
- **Environment Management**: python-dotenv

## 📦 Installation

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** installed and running locally
3. **ServiceNow instance** with API access
4. Required Python packages (see requirements below)

### Setup Instructions

1. **Clone or download the project files**
   ```bash
   cd path/to/your/project
   ```

2. **Install required packages**
   ```bash
   pip install streamlit requests flask python-dotenv
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root with the following variables:
   ```env
   SERVICENOW_INSTANCE=https://your-instance.service-now.com
   SERVICENOW_USERNAME=your_username
   SERVICENOW_PASSWORD=your_password
   OLLAMA_MODEL=llama3
   ```

4. **Install and configure Ollama**
   
   Download Ollama from [https://ollama.ai](https://ollama.ai) and install the model:
   ```bash
   ollama pull llama3
   ```

5. **Start Ollama service**
   ```bash
   ollama serve
   ```

## 🚀 Usage

### Starting the Application

1. **Start the Flask API server**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

2. **Start the Streamlit interface** (in a new terminal)
   ```bash
   streamlit run ui.py
   ```
   The web interface will open at `http://localhost:8501`

### Using the Interface

#### Analyzing Incidents
- Enter a message containing a ServiceNow incident number (e.g., "Analyze incident INC0012345")
- The system will:
  - Fetch incident details from ServiceNow
  - Find similar historical incidents
  - Generate AI-powered analysis including root cause and resolution steps

#### Creating Incidents
- Use natural language to describe the incident with "create incident" keyword
- Example: "Create incident for email server outage affecting all users"
- The system will:
  - Extract structured data using AI
  - Create the incident in ServiceNow
  - Return the created incident details

## 📁 Project Structure

```
mcp/
├── app.py              # Flask API server with ServiceNow integration
├── ui.py               # Streamlit web interface
├── .env                # Environment variables (create this file)
├── venv/               # Virtual environment (optional)
└── README.md           # This file
```

## 🔧 API Endpoints

### POST /chat
Processes user messages for incident analysis or creation.

**Request Body:**
```json
{
  "message": "Analyze incident INC0012345"
}
```

**Response Format:**
```json
{
  "mode": "analyze|create|error",
  "data": {...},
  "error": "error message if applicable"
}
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SERVICENOW_INSTANCE` | Your ServiceNow instance URL | Yes |
| `SERVICENOW_USERNAME` | ServiceNow username | Yes |
| `SERVICENOW_PASSWORD` | ServiceNow password | Yes |
| `OLLAMA_MODEL` | Ollama model name (default: llama3) | No |

### ServiceNow Permissions

Ensure your ServiceNow user has the following permissions:
- Read access to the `incident` table
- Write access to the `incident` table (for creation)
- API access enabled

## 🔍 How It Works

1. **User Input**: User enters a request through the Streamlit interface
2. **Message Processing**: Flask API processes the message and determines the action
3. **ServiceNow Integration**: System fetches or creates incidents using ServiceNow REST API
4. **AI Analysis**: Ollama generates intelligent analysis based on incident data and historical patterns
5. **Response**: Results are displayed in the web interface with structured information

## 🛡️ Security Considerations

- Store sensitive credentials in environment variables only
- Use HTTPS for ServiceNow connections in production
- Implement proper authentication for the web interface in production
- Regularly update dependencies for security patches

## 🔧 Troubleshooting

### Common Issues

1. **Connection to ServiceNow fails**
   - Verify your credentials in the `.env` file
   - Check your ServiceNow instance URL
   - Ensure your account has API access

2. **Ollama errors**
   - Make sure Ollama is running (`ollama serve`)
   - Verify the model is installed (`ollama list`)
   - Check if the model name in `.env` matches the installed model

3. **Import errors**
   - Install required packages: `pip install streamlit requests flask python-dotenv`
   - Activate your virtual environment if using one

### Logs and Debugging

- Flask runs in debug mode by default - check console output for errors
- Streamlit displays errors in the web interface
- Check Ollama logs if AI responses seem incorrect

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is provided as-is for educational and internal use. Please ensure compliance with your organization's policies when integrating with production ServiceNow instances.

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review ServiceNow and Ollama documentation
- Verify your environment configuration

---

**Note**: This application is designed for internal enterprise use and requires proper ServiceNow credentials and Ollama installation to function correctly.