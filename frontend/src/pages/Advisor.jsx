import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, Trash2, StopCircle } from 'lucide-react';

const Advisor = () => {
  const [messages, setMessages] = useState([
    { 
      role: 'ai', 
      content: "Hello! I'm your AI Financial Copilot. I have access to real-time market sentiment and technical indicators. How can I help you today?" 
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async (text = input) => {
    if (!text.trim()) return;

    // 1. Add User Message
    const userMsg = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      // 2. Call Backend
      const response = await fetch('http://localhost:4000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      const data = await response.json();

      // 3. Add AI Message
      setMessages(prev => [...prev, { role: 'ai', content: data.reply }]);
    } catch {
      setMessages(prev => [...prev, { role: 'ai', content: "Error: I couldn't connect to the intelligence server." }]);
    } finally {
      setIsTyping(false);
    }
  };

  // Quick Prompt Chips
  const suggestions = [
    "What is the current market sentiment?",
    "Analyze TSLA technicals",
    "Show me recent AI trades",
    "Explain the risk level"
  ];

  return (
    <div className="h-[calc(100vh-120px)] flex flex-col max-w-4xl mx-auto">
        
        {/* Header */}
        <div className="flex items-center justify-between mb-4 px-4">
            <div>
                <h1 className="text-2xl font-bold text-white flex items-center gap-2">
                    <Sparkles className="text-fintech-primary" /> AI Advisor
                </h1>
                <p className="text-xs text-fintech-textSec">Powered by Multi-Agent System</p>
            </div>
            <button 
                onClick={() => setMessages([messages[0]])}
                className="p-2 hover:bg-fintech-panel rounded-full text-fintech-textSec hover:text-fintech-bear transition-colors"
                title="Clear Chat"
            >
                <Trash2 size={18} />
            </button>
        </div>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto space-y-6 pr-4 custom-scrollbar bg-fintech-card/30 rounded-2xl p-6 border border-fintech-border relative">
            
            {messages.map((msg, idx) => (
                <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''} animate-in fade-in slide-in-from-bottom-2 duration-300`}>
                    
                    {/* Avatar */}
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 shadow-lg ${
                        msg.role === 'ai' 
                        ? 'bg-gradient-to-br from-fintech-primary to-indigo-900 text-white border border-fintech-primary/50' 
                        : 'bg-fintech-panel text-fintech-textSec border border-fintech-border'
                    }`}>
                        {msg.role === 'ai' ? <Bot size={20} /> : <User size={20} />}
                    </div>

                    {/* Bubble */}
                    <div className={`p-4 rounded-2xl max-w-[85%] text-sm leading-relaxed shadow-md ${
                        msg.role === 'ai' 
                            ? 'bg-fintech-panel border border-fintech-border text-gray-200 rounded-tl-none' 
                            : 'bg-fintech-primary text-white rounded-tr-none'
                    }`}>
                        {/* Render simple formatting (bolding) */}
                        {msg.content.split('**').map((part, i) => 
                            i % 2 === 1 ? <strong key={i} className="text-white font-bold">{part}</strong> : part
                        )}
                    </div>
                </div>
            ))}

            {/* Typing Indicator */}
            {isTyping && (
                <div className="flex gap-4 animate-pulse">
                    <div className="w-10 h-10 rounded-full bg-fintech-panel border border-fintech-border flex items-center justify-center">
                        <Bot size={20} className="text-fintech-primary" />
                    </div>
                    <div className="bg-fintech-panel border border-fintech-border px-4 py-3 rounded-2xl rounded-tl-none flex items-center gap-1">
                        <div className="w-2 h-2 bg-fintech-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                        <div className="w-2 h-2 bg-fintech-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                        <div className="w-2 h-2 bg-fintech-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                </div>
            )}
            
            <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="mt-4 space-y-4">
            
            {/* Quick Suggestions (Only show if not typing) */}
            {!isTyping && (
                <div className="flex gap-2 overflow-x-auto pb-2 custom-scrollbar">
                    {suggestions.map((s, i) => (
                        <button 
                            key={i}
                            onClick={() => handleSend(s)}
                            className="whitespace-nowrap px-4 py-2 bg-fintech-panel border border-fintech-border rounded-full text-xs text-fintech-textSec hover:border-fintech-primary hover:text-white transition-all hover:shadow-glow-purple"
                        >
                            {s}
                        </button>
                    ))}
                </div>
            )}

            {/* Input Box */}
            <form 
                onSubmit={(e) => { e.preventDefault(); handleSend(); }} 
                className="relative group"
            >
                <input 
                    type="text" 
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask about market trends, specific assets, or trade history..."
                    disabled={isTyping}
                    className="w-full bg-fintech-panel border border-fintech-border rounded-2xl py-4 pl-6 pr-16 text-white placeholder:text-fintech-textSec/50 focus:outline-none focus:border-fintech-primary focus:shadow-glow-purple transition-all disabled:opacity-50"
                />
                <button 
                    type="submit"
                    disabled={!input.trim() || isTyping}
                    className="absolute right-3 top-3 p-2 bg-fintech-primary rounded-xl text-white hover:bg-fintech-primaryHover transition-all disabled:bg-fintech-border disabled:cursor-not-allowed hover:shadow-lg hover:shadow-purple-500/20"
                >
                    {isTyping ? <StopCircle size={20} className="animate-pulse"/> : <Send size={20} />}
                </button>
            </form>
        </div>
    </div>
  );
};

export default Advisor;