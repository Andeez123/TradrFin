import React, { useState } from 'react';
import Card from '../components/Card';
import { mockData } from '../data/mockData';
import { Send, Bot, ArrowRight, CheckCircle, AlertCircle } from 'lucide-react';

const Transfer = () => {
  const [transferData, setTransferData] = useState({
    recipient: '',
    amount: '',
    description: '',
    account: 'checking'
  });

  const [aiTransfer, setAiTransfer] = useState({
    command: '',
    isProcessing: false,
    result: null
  });

  const handleTransfer = (e) => {
    e.preventDefault();
    // Mock transfer success
    alert('Transfer completed successfully!');
    setTransferData({
      recipient: '',
      amount: '',
      description: '',
      account: 'checking'
    });
  };

  const handleAITransfer = async () => {
    if (!aiTransfer.command.trim()) return;

    setAiTransfer(prev => ({ ...prev, isProcessing: true }));

    // Mock AI processing
    setTimeout(() => {
      setAiTransfer({
        command: '',
        isProcessing: false,
        result: {
          success: true,
          message: 'AI processed: "Transfer $50 to John for coffee" - Transfer completed successfully!',
          details: {
            amount: '$50.00',
            recipient: 'John',
            purpose: 'coffee'
          }
        }
      });
    }, 2000);
  };

  const recentRecipients = [
    { name: 'Sarah Johnson', account: '**** 4582', avatar: 'SJ' },
    { name: 'Mike Chen', account: '**** 8921', avatar: 'MC' },
    { name: 'Emily Davis', account: '**** 3345', avatar: 'ED' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-semibold text-white">Transfer Money</h2>
          <p className="text-fintech-textSec">Send money securely to anyone</p>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-fintech-textSec">Available Balance:</span>
          <span className="text-white font-medium">
            {mockData.user.currency}{mockData.banking.checkingBalance.toLocaleString()}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Transfer Form */}
        <div className="lg:col-span-2 space-y-6">
          {/* Quick Transfer */}
          <Card>
            <h3 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
              <Send size={20} />
              Quick Transfer
            </h3>

            <form onSubmit={handleTransfer} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-fintech-textSec mb-2">
                    From Account
                  </label>
                  <select
                    value={transferData.account}
                    onChange={(e) => setTransferData(prev => ({ ...prev, account: e.target.value }))}
                    className="w-full bg-fintech-panel border border-fintech-border rounded-lg px-3 py-2 text-white focus:outline-none focus:border-fintech-primary"
                  >
                    <option value="checking">Checking Account •••• 4829</option>
                    <option value="savings">Savings Account •••• 9921</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-fintech-textSec mb-2">
                    Recipient
                  </label>
                  <input
                    type="text"
                    placeholder="Account number or email"
                    value={transferData.recipient}
                    onChange={(e) => setTransferData(prev => ({ ...prev, recipient: e.target.value }))}
                    className="w-full bg-fintech-panel border border-fintech-border rounded-lg px-3 py-2 text-white placeholder-fintech-textSec focus:outline-none focus:border-fintech-primary"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-fintech-textSec mb-2">
                    Amount
                  </label>
                  <div className="relative">
                    <span className="absolute left-3 top-1/2 -translate-y-1/2 text-fintech-textSec">
                      {mockData.user.currency}
                    </span>
                    <input
                      type="number"
                      placeholder="0.00"
                      value={transferData.amount}
                      onChange={(e) => setTransferData(prev => ({ ...prev, amount: e.target.value }))}
                      className="w-full bg-fintech-panel border border-fintech-border rounded-lg pl-8 pr-3 py-2 text-white placeholder-fintech-textSec focus:outline-none focus:border-fintech-primary"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-fintech-textSec mb-2">
                    Description (Optional)
                  </label>
                  <input
                    type="text"
                    placeholder="What's this for?"
                    value={transferData.description}
                    onChange={(e) => setTransferData(prev => ({ ...prev, description: e.target.value }))}
                    className="w-full bg-fintech-panel border border-fintech-border rounded-lg px-3 py-2 text-white placeholder-fintech-textSec focus:outline-none focus:border-fintech-primary"
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full bg-fintech-primary hover:bg-fintech-primaryHover text-white py-3 rounded-lg font-medium transition-all flex items-center justify-center gap-2"
              >
                <Send size={18} />
                Send Transfer
              </button>
            </form>
          </Card>

          {/* Recent Recipients */}
          <Card>
            <h3 className="text-lg font-semibold text-white mb-4">Recent Recipients</h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {recentRecipients.map((recipient, index) => (
                <button
                  key={index}
                  onClick={() => setTransferData(prev => ({ ...prev, recipient: recipient.account }))}
                  className="flex items-center gap-3 p-3 rounded-lg border border-fintech-border hover:border-fintech-primary hover:bg-fintech-panel transition-all text-left"
                >
                  <div className="w-10 h-10 rounded-full bg-fintech-primary flex items-center justify-center text-white font-medium">
                    {recipient.avatar}
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="text-white text-sm font-medium truncate">{recipient.name}</p>
                    <p className="text-fintech-textSec text-xs">{recipient.account}</p>
                  </div>
                  <ArrowRight size={16} className="text-fintech-textSec" />
                </button>
              ))}
            </div>
          </Card>
        </div>

        {/* AI Transfer Assistant */}
        <div className="space-y-6">
          <Card>
            <h3 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
              <Bot size={20} className="text-fintech-primary" />
              AI Transfer Assistant
            </h3>

            <div className="space-y-4">
              <div className="p-4 bg-fintech-panel rounded-lg border border-fintech-border">
                <p className="text-sm text-fintech-textSec mb-3">
                  Describe your transfer in natural language
                </p>
                <textarea
                  placeholder="e.g., 'Send $50 to John for coffee' or 'Transfer $200 to savings account'"
                  value={aiTransfer.command}
                  onChange={(e) => setAiTransfer(prev => ({ ...prev, command: e.target.value }))}
                  className="w-full bg-fintech-bg border border-fintech-border rounded-lg px-3 py-2 text-white placeholder-fintech-textSec focus:outline-none focus:border-fintech-primary resize-none"
                  rows={3}
                />
                <button
                  onClick={handleAITransfer}
                  disabled={!aiTransfer.command.trim() || aiTransfer.isProcessing}
                  className="w-full mt-3 bg-fintech-primary hover:bg-fintech-primaryHover disabled:opacity-50 disabled:cursor-not-allowed text-white py-2 rounded-lg font-medium transition-all flex items-center justify-center gap-2"
                >
                  {aiTransfer.isProcessing ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      Processing...
                    </>
                  ) : (
                    <>
                      <Bot size={16} />
                      Process with AI
                    </>
                  )}
                </button>
              </div>

              {/* AI Result */}
              {aiTransfer.result && (
                <div className={`p-4 rounded-lg border ${
                  aiTransfer.result.success
                    ? 'bg-green-500/10 border-green-500/20'
                    : 'bg-red-500/10 border-red-500/20'
                }`}>
                  <div className="flex items-start gap-3">
                    {aiTransfer.result.success ? (
                      <CheckCircle size={20} className="text-green-500 mt-0.5 flex-shrink-0" />
                    ) : (
                      <AlertCircle size={20} className="text-red-500 mt-0.5 flex-shrink-0" />
                    )}
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-white mb-2">
                        {aiTransfer.result.success ? 'Transfer Completed' : 'Transfer Failed'}
                      </p>
                      <p className="text-sm text-fintech-textSec mb-3">
                        {aiTransfer.result.message}
                      </p>
                      {aiTransfer.result.details && (
                        <div className="space-y-1 text-xs">
                          <div className="flex justify-between">
                            <span className="text-fintech-textSec">Amount:</span>
                            <span className="text-white">{aiTransfer.result.details.amount}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-fintech-textSec">To:</span>
                            <span className="text-white">{aiTransfer.result.details.recipient}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-fintech-textSec">Purpose:</span>
                            <span className="text-white">{aiTransfer.result.details.purpose}</span>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* AI Examples */}
              <div className="space-y-2">
                <p className="text-sm font-medium text-white">Try these examples:</p>
                <div className="space-y-2">
                  {[
                    "Transfer $25 to Sarah for lunch",
                    "Send $100 to Mike Chen",
                    "Move $500 to savings account",
                    "Pay $75 to Emily for groceries"
                  ].map((example, index) => (
                    <button
                      key={index}
                      onClick={() => setAiTransfer(prev => ({ ...prev, command: example }))}
                      className="w-full text-left p-2 rounded border border-fintech-border hover:border-fintech-primary hover:bg-fintech-panel transition-all text-sm text-fintech-textSec hover:text-white"
                    >
                      "{example}"
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </Card>

          {/* Transfer Tips */}
          <Card>
            <h4 className="text-md font-semibold text-white mb-3">Transfer Tips</h4>
            <div className="space-y-2 text-sm text-fintech-textSec">
              <p>• Transfers are instant between your accounts</p>
              <p>• External transfers may take 1-3 business days</p>
              <p>• Use AI assistant for quick voice-to-transfer</p>
              <p>• All transfers are secured with bank-level encryption</p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Transfer;
