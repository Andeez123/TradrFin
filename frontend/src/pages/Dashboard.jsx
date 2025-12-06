import React from 'react';
import Card from '../components/Card';
import { mockData } from '../data/mockData';
import { ArrowUpRight, ArrowDownRight, Wallet, TrendingUp } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const chartData = [
  { name: 'Mon', value: 82000 },
  { name: 'Tue', value: 83500 },
  { name: 'Wed', value: 83000 },
  { name: 'Thu', value: 85000 },
  { name: 'Fri', value: 86400 },
];

const Dashboard = () => {
  return (
    <div className="space-y-6">
      <header>
        <h2 className="text-2xl font-semibold text-white">Welcome back, {mockData.user.name}</h2>
        <p className="text-fintech-textSec">Here is your financial overview via Multi-Agent analysis.</p>
      </header>

      {/* Top Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6">
        <Card>
            <div className="flex items-start justify-between">
                <div>
                    <p className="text-fintech-textSec text-sm">Total Balance</p>
                    <h3 className="text-2xl sm:text-3xl font-bold text-white mt-1">
                        {mockData.user.currency}{mockData.user.balance.toLocaleString()}
                    </h3>
                </div>
                <div className="p-3 bg-fintech-panel rounded-lg text-fintech-primary">
                    <Wallet size={24} />
                </div>
            </div>
        </Card>

        <Card glow="green">
            <div className="flex items-start justify-between">
                <div>
                    <p className="text-fintech-textSec text-sm">Investment Value</p>
                    <h3 className="text-2xl sm:text-3xl font-bold text-white mt-1">
                        {mockData.user.currency}{mockData.portfolio.totalValue.toLocaleString()}
                    </h3>
                    <span className="text-fintech-bull text-sm flex items-center gap-1 mt-2">
                        <ArrowUpRight size={16} /> {mockData.portfolio.change}
                    </span>
                </div>
                <div className="p-3 bg-fintech-panel rounded-lg text-fintech-bull">
                    <TrendingUp size={24} />
                </div>
            </div>
        </Card>

        <Card glow="purple">
            <div className="flex items-start justify-between">
                <div>
                    <p className="text-fintech-textSec text-sm">Market Mood</p>
                    <h3 className="text-3xl font-bold text-fintech-primary mt-1">
                        {mockData.sentimentAgent.label}
                    </h3>
                    <p className="text-xs text-fintech-textSec mt-2 max-w-[200px] truncate">
                        {mockData.sentimentAgent.summary}
                    </p>
                </div>
                <div className="h-12 w-12 rounded-full border-4 border-fintech-primary flex items-center justify-center text-white font-bold">
                    {(mockData.sentimentAgent.score * 100).toFixed(0)}
                </div>
            </div>
        </Card>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chart Section */}
        <Card className="lg:col-span-2 min-h-[400px]">
            <h3 className="text-lg font-semibold text-white mb-6">Portfolio Performance</h3>
            <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData}>
                        <defs>
                            <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8A2BE2" stopOpacity={0.3}/>
                                <stop offset="95%" stopColor="#8A2BE2" stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <XAxis dataKey="name" stroke="#666673" axisLine={false} tickLine={false} />
                        <YAxis stroke="#666673" axisLine={false} tickLine={false} />
                        <Tooltip 
                            contentStyle={{ backgroundColor: '#1A1A1E', borderColor: '#2A2A2E' }}
                            itemStyle={{ color: '#8A2BE2' }}
                        />
                        <Area type="monotone" dataKey="value" stroke="#8A2BE2" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </Card>

        {/* Asset List */}
        <Card>
            <h3 className="text-lg font-semibold text-white mb-4">Your Assets</h3>
            <div className="space-y-4">
                {mockData.portfolio.assets.map((asset) => (
                    <div key={asset.symbol} className="flex items-center justify-between p-3 hover:bg-fintech-panel rounded-xl transition-colors cursor-pointer group">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-full bg-fintech-panel flex items-center justify-center text-fintech-primary font-bold group-hover:bg-fintech-primary group-hover:text-white transition-colors">
                                {asset.symbol[0]}
                            </div>
                            <div>
                                <h4 className="text-white font-medium">{asset.symbol}</h4>
                                <p className="text-xs text-fintech-textSec">{asset.name}</p>
                            </div>
                        </div>
                        <div className="text-right">
                            <p className="text-white font-medium">${asset.price}</p>
                            <span className={`text-xs ${asset.change.startsWith('+') ? 'text-fintech-bull' : 'text-fintech-bear'}`}>
                                {asset.change}
                            </span>
                        </div>
                    </div>
                ))}
            </div>
            <button className="w-full mt-6 py-3 border border-fintech-primary text-fintech-primary rounded-xl hover:bg-fintech-primary hover:text-white transition-all text-sm font-medium">
                View All Assets
            </button>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;