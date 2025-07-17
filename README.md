# AI CRM Chatbot

An AI-powered CRM chatbot built with FastAPI backend and React frontend, integrating Azure OpenAI through LangChain.

## Project Structure

```
ai-crm/
├── api/                    # FastAPI Backend
│   ├── main.py            # Main FastAPI application
│   └── requirements.txt   # Python dependencies
├── app/                   # React Frontend (Vite)
│   ├── src/
│   │   ├── App.tsx       # Main App component
│   │   ├── Chatbot.tsx   # Chatbot component
│   │   ├── Chatbot.css   # Chatbot styles
│   │   └── ...
│   └── package.json      # Node.js dependencies
└── README.md             # This file
```

## Features

- 🤖 AI-powered chatbot using Azure OpenAI GPT-4
- 🔗 LangChain integration for advanced language processing
- ⚡ FastAPI backend for high-performance API
- ⚛️ Modern React frontend with TypeScript
- 🎨 Beautiful, responsive UI design
- 🔄 Real-time chat interface
- 🔐 Azure AD authentication

## Prerequisites

- Python 3.8+
- Node.js 16+
- Azure OpenAI API access
- Azure AD tenant and app registration


## Quick Start Guide (For Beginners)

This guide is for users who are new to Python and React. Follow these simple steps to set up and run the project on your computer.

### 1. Install Prerequisites

You need to install:
- **Python 3.8 or newer**: [Download Python](https://www.python.org/downloads/)
- **Node.js 16 or newer**: [Download Node.js](https://nodejs.org/)

### 2. Set Up the Backend (Python)

1. Open your terminal (Command Prompt, PowerShell, or Terminal app).
2. Go to the backend folder:
   ```bash
   cd api
   ```
3. Create a Python virtual environment (this keeps dependencies separate):
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
5. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
6. Add your Azure credentials:
   - Open the `api` folder and create a file named `.env` (see the example in this README below).
   - Fill in your Azure details.
7. Start the backend server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   - If you see a message like `Uvicorn running on http://0.0.0.0:8000`, your backend is running!

### 3. Set Up the Frontend (React)

1. Open a **new terminal window** (keep the backend running in the old one).
2. Go to the frontend folder:
   ```bash
   cd app
   ```
3. Install the required Node.js packages:
   ```bash
   npm install
   ```
4. Start the frontend server:
   ```bash
   npm run dev
   ```
5. Open your web browser and go to [http://localhost:5173](http://localhost:5173)
   - You should see the AI CRM Chatbot app!

---

If you get stuck, search for the error message online or ask for help!

---

## API Endpoints

- `GET /` - Health check endpoint
- `POST /chatbot/` - Send message to chatbot and receive response

### Request Format
```json
{
  "message": "Your question here"
}
```

### Response Format
```json
{
  "response": "AI generated response"
}
```

## Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain** - Framework for developing applications with LLMs
- **Azure OpenAI** - AI language model
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server
- **CSS3** - Modern styling with animations

## Development

### Running in Development Mode

1. Start the backend:
   ```bash
   cd api && python main.py
   ```

2. Start the frontend:
   ```bash
   cd app && npm run dev
   ```

### Building for Production

1. Build the frontend:
   ```bash
   cd app && npm run build
   ```

2. The backend can be deployed using Docker or cloud services like Azure App Service.

## Environment Variables

Create a `.env` file in the `api` directory with:

```env
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_SUBSCRIPTION_KEY=your_subscription_key
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support or questions, please open an issue on the repository.
