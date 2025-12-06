import React, { useState, useEffect } from 'react';
import Card from '../components/Card';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, ReferenceLine } from 'recharts';
import { Activity, TrendingUp, AlertTriangle, Loader2 } from 'lucide-react';


const Technicals = () => {
  const [activeTicker, setActiveTicker] = useState('TSLA');
  const [dbData, setDbData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Update active ticker if data loads and TSLA is not available
  useEffect(() => {
    if (dbData.length > 0) {
      const availableTickers = [...new Set(dbData.map(item => item.ticker))];
      if (!availableTickers.includes(activeTicker) && availableTickers.length > 0) {
        setActiveTicker(availableTickers[0]);
      }
    }
  }, [dbData, activeTicker]);

  // Fetch real market data from TiDB
  useEffect(() => {
    const fetchMarketData = async () => {
      try {
        const response = await fetch('http://localhost:4000/api/market-data');
        if (!response.ok) {
          throw new Error(`Failed to fetch market data: ${response.status}`);
        }
        const marketData = await response.json();

        // Process data to ensure dates are in correct format for charts
        const processedData = marketData.map(item => ({
          ...item,
          date: item.date ? new Date(item.date).toISOString().split('T')[0] : item.date,
          price: parseFloat(item.price) || 0,
          rsi: parseFloat(item.rsi) || 0
        }));

        setDbData(processedData);
      } catch (error) {
        console.error('Error fetching market data:', error);
        // Set empty array on error to prevent crashes
        setDbData([]);
      } finally {
        setLoading(false);
      }
    };

    fetchMarketData();
  }, []);

  // Filter based on active selection and sort by date
  const chartData = dbData
    .filter(d => d.ticker === activeTicker)
    .sort((a, b) => new Date(a.date) - new Date(b.date));
  const latestData = chartData[chartData.length - 1];

  if (loading) {
    return <div className="flex justify-center items-center h-64 text-fintech-primary"><Loader2 className="animate-spin" size={48} /></div>;
  }

  return (
    <div className="space-y-6">
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row justify-between items-end gap-4">
        <div>
            <h1 className="text-2xl font-bold text-white">Market Data Agent</h1>
            <p className="text-fintech-textSec">Live technical data from TiDB.</p>
        </div>
        
        <div className="flex bg-fintech-panel p-1 rounded-xl border border-fintech-border">
            {([...new Set(dbData.map(item => item.ticker))].slice(0, 4).length > 0
              ? [...new Set(dbData.map(item => item.ticker))].slice(0, 4).map(ticker => (
                <button
                    key={ticker}
                    onClick={() => setActiveTicker(ticker)}
                    className={`px-6 py-2 rounded-lg text-sm font-medium transition-all ${
                        activeTicker === ticker
                        ? 'bg-fintech-primary text-white shadow-glow-purple'
                        : 'text-fintech-textSec hover:text-white'
                    }`}
                >
                    {ticker}
                </button>
            ))
              : (
                <button className="px-6 py-2 rounded-lg text-sm font-medium text-fintech-textSec">
                    No data available
                </button>
            ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Charts Section */}
        <div className="lg:col-span-2 space-y-6">
            <Card>
                <div className="flex justify-between items-center mb-4">
                    <h3 className="text-white font-semibold flex items-center gap-2">
                        <TrendingUp size={18} className="text-fintech-primary"/> Price Action ({activeTicker})
                    </h3>
                    <span className="text-2xl font-bold text-white">
                        ${latestData?.price ? parseFloat(latestData.price).toFixed(2) : '---'}
                    </span>
                </div>
                <div className="h-[250px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={chartData}>
                            <defs>
                                <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#8A2BE2" stopOpacity={0.3}/>
                                    <stop offset="95%" stopColor="#8A2BE2" stopOpacity={0}/>
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="#2A2A2E" vertical={false} />
                            <XAxis dataKey="date" stroke="#666673" tick={{fontSize: 12}} />
                            <YAxis domain={['auto', 'auto']} stroke="#666673" tick={{fontSize: 12}} orientation="right" />
                            <Tooltip 
                                contentStyle={{ backgroundColor: '#1A1A1E', borderColor: '#2A2A2E' }}
                                itemStyle={{ color: '#fff' }}
                            />
                            <Area type="monotone" dataKey="price" stroke="#8A2BE2" strokeWidth={2} fill="url(#colorPrice)" />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </Card>

            <Card>
                <div className="flex justify-between items-center mb-4">
                    <h3 className="text-white font-semibold flex items-center gap-2">
                        <Activity size={18} className="text-fintech-primary"/> RSI Indicator
                    </h3>
                    <div className={`px-2 py-1 rounded text-xs font-bold ${
                        (latestData?.rsi || 50) > 70 ? 'bg-fintech-bear/20 text-fintech-bear' : 
                        (latestData?.rsi || 50) < 30 ? 'bg-fintech-bull/20 text-fintech-bull' : 
                        'bg-fintech-panel text-fintech-textSec'
                    }`}>
                        RSI: {latestData?.rsi ? parseFloat(latestData.rsi).toFixed(2) : '---'}
                    </div>
                </div>
                <div className="h-[150px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#2A2A2E" vertical={false} />
                            <XAxis dataKey="date" stroke="#666673" tick={{fontSize: 12}} />
                            <YAxis domain={[0, 100]} stroke="#666673" tick={{fontSize: 12}} orientation="right" ticks={[30, 50, 70]} />
                            <ReferenceLine y={70} stroke="#FF4F6F" strokeDasharray="3 3" />
                            <ReferenceLine y={30} stroke="#3BE28F" strokeDasharray="3 3" />
                            <Tooltip 
                                contentStyle={{ backgroundColor: '#1A1A1E', borderColor: '#2A2A2E' }}
                                itemStyle={{ color: '#fff' }}
                            />
                            <Area type="monotone" dataKey="rsi" stroke="#F5C542" strokeWidth={2} fill="transparent" />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </Card>
        </div>

        {/* Right: DB Logs */}
        <div className="lg:col-span-1 space-y-4">
             <div className="flex items-center gap-2 mb-2">
                <AlertTriangle size={16} className="text-fintech-primary" />
                <span className="text-sm font-semibold text-fintech-textSec uppercase">Analysis Log ({activeTicker})</span>
             </div>
             
             <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
                {[...chartData].reverse().map((day, idx) => (
                    <Card key={idx} className="!p-4 border-l-4 border-l-fintech-primary">
                        <div className="flex justify-between items-start mb-2">
                            <span className="text-xs text-fintech-textSec font-mono">{day.date}</span>
                            <span className="text-xs font-bold text-white">RSI: {day.rsi ? day.rsi.toFixed(1) : 'N/A'}</span>
                        </div>
                        <p className="text-sm text-white/90 leading-relaxed">
                            "Technical analysis data from TiDB - {day.ticker || 'Unknown ticker'}"
                        </p>
                    </Card>
                ))}
                {chartData.length === 0 && <p className="text-fintech-textSec text-sm">No data found for this ticker.</p>}
             </div>
        </div>

      </div>
    </div>
  );
};

export default Technicals;