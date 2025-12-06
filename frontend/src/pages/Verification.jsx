import React from 'react';
import Card from '../components/Card';
import { mockData } from '../data/mockData';
import { CheckCircle2, AlertTriangle, ArrowRight } from 'lucide-react';

const Verification = () => {
  const { finalSignal, confidence, reasoning } = mockData.crossVerification;
  
  // Dynamic styles based on signal
  const signalColor = finalSignal === 'Bullish' ? 'text-fintech-bull' : finalSignal === 'Bearish' ? 'text-fintech-bear' : 'text-fintech-neutral';
  const glowType = finalSignal === 'Bullish' ? 'green' : finalSignal === 'Bearish' ? 'red' : 'none';

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold text-white">Market Intelligence Center</h2>
        <p className="text-fintech-textSec">Cross-Verification Agent Output</p>
      </div>

      {/* Main Signal Card */}
      <Card glow={glowType} className="border-t-4 border-t-fintech-primary text-center py-12">
        <p className="text-fintech-textSec uppercase tracking-widest text-sm font-semibold mb-4">Final System Verdict</p>
        <h1 className={`text-6xl font-black ${signalColor} mb-6 tracking-tight`}>
          {finalSignal.toUpperCase()}
        </h1>
        
        <div className="flex justify-center items-center gap-2 mb-8">
            <div className="h-2 w-48 bg-fintech-panel rounded-full overflow-hidden">
                <div 
                    className={`h-full ${finalSignal === 'Bullish' ? 'bg-fintech-bull' : 'bg-fintech-bear'}`} 
                    style={{ width: `${confidence * 100}%` }}
                ></div>
            </div>
            <span className="text-white font-mono">{(confidence * 100).toFixed(0)}% Confidence</span>
        </div>

        <p className="text-white text-lg max-w-xl mx-auto italic">
          "{mockData.crossVerification.reasoning[0]} and {mockData.crossVerification.reasoning[1]}"
        </p>
      </Card>

      {/* Comparison Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4 opacity-10">
                <h1 className="text-8xl font-bold text-white">S</h1>
            </div>
            <h3 className="text-fintech-primary font-bold mb-4">Sentiment Agent</h3>
            <div className="space-y-4">
                <div className="flex justify-between text-sm">
                    <span className="text-fintech-textSec">Score</span>
                    <span className="text-white">{(mockData.sentimentAgent.score * 100).toFixed(0)}/100</span>
                </div>
                <div className="flex justify-between text-sm">
                    <span className="text-fintech-textSec">Key Theme</span>
                    <span className="text-white text-right">Rate Cuts</span>
                </div>
                <div className="mt-4 p-3 bg-fintech-panel rounded-lg text-xs text-fintech-textSec">
                    "News analysis suggests strong optimism in tech."
                </div>
            </div>
        </Card>

        <Card className="relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4 opacity-10">
                 <h1 className="text-8xl font-bold text-white">T</h1>
            </div>
            <h3 className="text-fintech-primary font-bold mb-4">Technical Agent</h3>
            <div className="space-y-4">
                <div className="flex justify-between text-sm">
                    <span className="text-fintech-textSec">Trend</span>
                    <span className="text-white">{mockData.technicalAgent.trend}</span>
                </div>
                <div className="flex justify-between text-sm">
                    <span className="text-fintech-textSec">RSI</span>
                    <span className="text-white">{mockData.technicalAgent.indicators.rsi}</span>
                </div>
                <div className="mt-4 p-3 bg-fintech-panel rounded-lg text-xs text-fintech-textSec">
                    "Price is above MA50 confirms uptrend structure."
                </div>
            </div>
        </Card>
      </div>

      {/* Logic Breakdown */}
      <Card>
        <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
            <CheckCircle2 className="text-fintech-bull" /> 
            Why this verdict?
        </h3>
        <ul className="space-y-3">
            {reasoning.map((reason, idx) => (
                <li key={idx} className="flex items-start gap-3 text-fintech-textSec text-sm">
                    <ArrowRight size={16} className="mt-1 text-fintech-primary shrink-0" />
                    {reason}
                </li>
            ))}
        </ul>
      </Card>
    </div>
  );
};

export default Verification;