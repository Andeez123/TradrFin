import React from 'react';
import Card from '../components/Card';
import { mockData } from '../data/mockData';
import { TrendingUp, Activity, Newspaper, Zap } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

// Reusing chart data
const chartData = [
  { name: 'Mon', value: 72000 },
  { name: 'Tue', value: 73500 },
  { name: 'Wed', value: 73000 },
  { name: 'Thu', value: 75000 },
  { name: 'Fri', value: 75250 },
];

const AIInvest = () => {
  return (
    <div className="space-y-6">
      {/* Introduction Banner */}
      <div className="relative p-6 lg:p-8 rounded-2xl bg-gradient-to-r from-fintech-card to-fintech-panel border border-fintech-border overflow-hidden">
        <div className="absolute top-0 right-0 w-32 h-32 lg:w-64 lg:h-64 bg-fintech-primary opacity-10 blur-3xl rounded-full translate-x-1/2 -translate-y-1/2"></div>

        <div className="relative z-10 flex flex-col lg:flex-row lg:justify-between lg:items-center gap-6">
            <div>
                <h1 className="text-xl sm:text-2xl lg:text-3xl font-bold text-white mb-2">AI Investment Hub</h1>
                <p className="text-fintech-textSec max-w-lg text-sm lg:text-base">
                    Multi-Agent Intelligence is analyzing your portfolio 24/7.
                    Current Signal: <span className="text-fintech-bull font-bold">BULLISH</span>
                </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-3 lg:gap-3">
                 <div className="text-center sm:text-right">
                    <p className="text-xs text-fintech-textSec">Portfolio Value</p>
                    <p className="text-xl lg:text-2xl font-bold text-white">${mockData.portfolio.investedValue.toLocaleString()}</p>
                 </div>
                 <div className="bg-fintech-bull/10 px-3 py-1 rounded-lg flex items-center text-fintech-bull h-fit self-center">
                    <TrendingUp size={16} className="mr-1"/> +1.65%
                 </div>
            </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-6">
        
        {/* Main Chart */}
        <Card className="lg:col-span-2">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-semibold text-white">Performance</h3>
                <div className="flex gap-2">
                    {['1D', '1W', '1M', '1Y'].map(t => (
                        <button key={t} className={`px-3 py-1 text-xs rounded-md ${t === '1W' ? 'bg-fintech-primary text-white' : 'bg-fintech-panel text-fintech-textSec'}`}>
                            {t}
                        </button>
                    ))}
                </div>
            </div>
            <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData}>
                        <defs>
                            <linearGradient id="colorInvest" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8A2BE2" stopOpacity={0.3}/>
                                <stop offset="95%" stopColor="#8A2BE2" stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <XAxis dataKey="name" stroke="#666673" hide />
                        <YAxis stroke="#666673" orientation="right" tick={{fontSize: 12}} axisLine={false} tickLine={false} />
                        <Tooltip 
                            contentStyle={{ backgroundColor: '#1A1A1E', borderColor: '#2A2A2E', borderRadius: '10px' }}
                            itemStyle={{ color: '#fff' }}
                        />
                        <Area type="monotone" dataKey="value" stroke="#8A2BE2" strokeWidth={2} fillOpacity={1} fill="url(#colorInvest)" />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </Card>

        {/* AI Insight Cards */}
        <div className="space-y-6">
            <Card glow="purple">
                <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-fintech-primary/20 rounded-lg text-fintech-primary">
                        <Zap size={20} />
                    </div>
                    <h3 className="text-white font-medium">Daily AI Signal</h3>
                </div>
                <div className="text-center py-4">
                    <span className="text-4xl font-bold text-fintech-bull">BUY</span>
                    <p className="text-xs text-fintech-textSec mt-2">Confidence Score: 88%</p>
                </div>
                <div className="mt-4 pt-4 border-t border-fintech-border">
                    <p className="text-sm text-fintech-textSec italic">
                        "Cross-verification complete. Sentiment and Technicals align on Tech Sector."
                    </p>
                    <button className="w-full mt-4 py-2 bg-fintech-panel hover:bg-fintech-primary hover:text-white text-fintech-textSec text-xs rounded-lg transition-colors">
                        View Full Analysis
                    </button>
                </div>
            </Card>

            <Card>
                <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-fintech-panel rounded-lg text-white">
                        <Activity size={20} />
                    </div>
                    <h3 className="text-white font-medium">Top Movers</h3>
                </div>
                <div className="space-y-3">
                    {mockData.portfolio.assets.map((asset) => (
                        <div key={asset.symbol} className="flex justify-between items-center text-sm">
                            <span className="text-white font-medium">{asset.symbol}</span>
                            <span className={asset.change.startsWith('+') ? 'text-fintech-bull' : 'text-fintech-bear'}>
                                {asset.change}
                            </span>
                        </div>
                    ))}
                </div>
            </Card>
        </div>
      </div>
    </div>
  );
};

export default AIInvest;