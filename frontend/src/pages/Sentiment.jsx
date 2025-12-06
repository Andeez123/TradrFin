import React, { useState, useEffect } from 'react';
import Card from '../components/Card';
import { Newspaper, Globe, TrendingUp, TrendingDown, Minus, Loader2 } from 'lucide-react';


const Sentiment = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch real sentiment data from TiDB
  useEffect(() => {
    const fetchSentimentData = async () => {
      try {
        const response = await fetch('http://localhost:4000/api/sentiment');
        if (!response.ok) {
          throw new Error('Failed to fetch sentiment data');
        }
        const sentimentData = await response.json();
        setData(sentimentData);
      } catch (error) {
        console.error('Error fetching sentiment data:', error);
        // Set empty array on error to prevent crashes
        setData([]);
      } finally {
        setLoading(false);
      }
    };

    fetchSentimentData();
  }, []);

  const getSentimentStyle = (type) => {
    // Safety check if type is null
    const sentiment = type ? type.toLowerCase() : 'neutral';
    switch (sentiment) {
      case 'positive':
        return { color: 'text-fintech-bull', bg: 'bg-fintech-bull/10', border: 'border-fintech-bull', icon: <TrendingUp size={20} /> };
      case 'negative':
        return { color: 'text-fintech-bear', bg: 'bg-fintech-bear/10', border: 'border-fintech-bear', icon: <TrendingDown size={20} /> };
      default:
        return { color: 'text-fintech-neutral', bg: 'bg-fintech-neutral/10', border: 'border-fintech-neutral', icon: <Minus size={20} /> };
    }
  };


  if (loading) {
    return <div className="flex justify-center items-center h-64 text-fintech-primary"><Loader2 className="animate-spin" size={48} /></div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
            <h1 className="text-2xl font-bold text-white">Sentiment Intelligence</h1>
            <p className="text-fintech-textSec">Real-time analysis from TiDB Database.</p>
        </div>
        <div className="px-4 py-2 bg-fintech-card border border-fintech-border rounded-xl">
            <span className="text-xs text-fintech-textSec uppercase tracking-wider">Live Feeds</span>
            <p className="text-xl font-bold text-white text-center">{data.length}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {data.map((item, index) => {
          const style = getSentimentStyle(item.sentiment);

          return (
            <Card key={item.id || index} className="group hover:border-fintech-primary/50 transition-all">
              <div className="flex flex-col md:flex-row gap-6">
                <div className="md:w-48 shrink-0 flex flex-col justify-center items-center p-4 rounded-xl bg-fintech-panel border border-fintech-border">
                    <div className={`mb-2 p-3 rounded-full ${style.bg} ${style.color}`}>
                        {style.icon}
                    </div>
                    <span className={`uppercase font-bold text-sm ${style.color}`}>
                        {item.sentiment || 'UNKNOWN'}
                    </span>
                    <div className="mt-2 text-xs text-fintech-textSec">
                        Confidence: {item.confidence ? (item.confidence * 100).toFixed(0) + '%' : 'N/A'}
                    </div>
                    <div className="w-full h-1.5 bg-fintech-bg rounded-full mt-2 overflow-hidden">
                        <div
                            className={`h-full ${style.bg.replace('/10', '')}`}
                            style={{ width: item.confidence ? `${item.confidence * 100}%` : '0%' }}
                        ></div>
                    </div>
                </div>

                <div className="flex-1 space-y-3">
                    <div className="flex items-center gap-2 mb-1">
                        <span className="flex items-center gap-1 px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider bg-fintech-bg border border-fintech-border text-fintech-textSec">
                            <Globe size={14} /> {item.source || 'Database'}
                        </span>
                    </div>
                    <h3 className="text-lg font-semibold text-white group-hover:text-fintech-primary transition-colors">
                        "{item.content || 'Market Sentiment Analysis'}"
                    </h3>
                    <div className="p-3 bg-fintech-panel/50 rounded-lg border-l-2 border-fintech-primary">
                        <p className="text-sm text-fintech-textSec italic">
                            AI Summary: {item.summary || 'No summary available'}
                        </p>
                    </div>
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default Sentiment;