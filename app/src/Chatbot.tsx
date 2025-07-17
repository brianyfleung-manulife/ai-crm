import React, { useState, useRef, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Send, Bot, User } from "lucide-react";


interface Message {
  text: string;
  from: 'user' | 'bot';
  timestamp: Date;
}

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      text: "Hello! I'm your AI CRM assistant. How can I help you today?",
      from: 'bot',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      text: input,
      from: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const response = await fetch(`${apiUrl}/chatbot/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: input })
      });

      const data = await response.json();
      
      const botMessage: Message = {
        text: data.response,
        from: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        text: "Sorry, I'm having trouble connecting. Please try again later.",
        from: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const TypingIndicator = () => (
    <div className="flex space-x-1">
      <div className="w-2 h-2 bg-green-500 rounded-full animate-bounce"></div>
      <div className="w-2 h-2 bg-green-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
      <div className="w-2 h-2 bg-green-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
    </div>
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <span className="inline-flex items-center gap-2">
            <Bot className="h-6 w-6" />
            AI CRM Assistant
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* Messages Container */}
        <div className="h-[400px] overflow-y-auto space-y-2">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.from === 'user' ? 'justify-end' : 'justify-start'} items-end`}
            >
              {msg.from === 'bot' && (
                <span className="mr-2"><Bot className="h-4 w-4" /></span>
              )}
              <div className="flex flex-col max-w-xs">
                <div
                  className={`rounded-xl px-4 py-2 mb-1 text-sm break-words ${
                    msg.from === 'user'
                      ? 'bg-green-600 text-white rounded-br-md'
                      : 'bg-gray-100 text-gray-900 border rounded-bl-md'
                  }`}
                >
                  {msg.text}
                </div>
                <span
                  className={`text-xs text-gray-500 ${msg.from === 'user' ? 'text-right pr-1' : 'text-left pl-1'}`}
                >
                  {msg.timestamp.toLocaleTimeString()}
                </span>
              </div>
              {msg.from === 'user' && (
                <span className="ml-2"><User className="h-4 w-4" /></span>
              )}
            </div>
          ))}
          {isLoading && (
            <div className="flex items-center mb-2">
              <span className="mr-2"><Bot className="h-4 w-4" /></span>
              <TypingIndicator />
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        {/* Input Container */}
        <div>
          <form style={{ display: 'flex', gap: 8, alignItems: 'flex-end', marginTop: 16 }} onSubmit={e => { e.preventDefault(); sendMessage(); }}>
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here..."
              disabled={isLoading}
            />
            <Button 
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
              size="icon"
              type="submit"
            >
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
      </CardContent>
    </Card>
  );
};

export default Chatbot;
