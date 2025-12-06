import React, { useState, useEffect } from 'react';
import { ArrowUpRight, ArrowDownLeft, Search, Filter, Cpu, Activity, AlertCircle } from 'lucide-react';


const History = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('ALL'); // ALL, BUY, SELL
  const [search, setSearch] = useState('');

  // Fetch real transaction data from TiDB
  useEffect(() => {
    const fetchTransactionData = async () => {
      try {
        const response = await fetch('http://localhost:4000/api/transactions');
        if (!response.ok) {
          throw new Error('Failed to fetch transaction data');
        }
        const transactionData = await response.json();
        setTransactions(transactionData);
      } catch (error) {
        console.error('Error fetching transaction data:', error);
        // Set empty array on error to prevent crashes
        setTransactions([]);
      } finally {
        setLoading(false);
      }
    };

    fetchTransactionData();
  }, []);

  // Filter Logic
  const filteredData = transactions.filter(tx => {
    // Normalize action to uppercase for comparison
    const actionUpper = tx.action ? tx.action.toUpperCase() : 'UNKNOWN';
    const matchesFilter = filter === 'ALL' || actionUpper === filter;
    const matchesSearch = tx.ticker && tx.ticker.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  return (
    <div className="space-y-6">
      
      {/* Page Header */}
      <div className="flex flex-col gap-4 lg:gap-6">
        <div>
            <h1 className="text-2xl lg:text-3xl font-bold text-white mb-1">AI Trade History</h1>
            <p className="text-fintech-textSec text-sm lg:text-lg">Live feed from Asset Movement Agent</p>
        </div>

        {/* Search & Filter - Mobile stacked, Desktop horizontal */}
        <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-end lg:gap-4">
            <div className="relative w-full lg:w-auto lg:flex-1 lg:max-w-sm">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-fintech-textSec" size={16} />
                <input
                    type="text"
                    placeholder="Search by ticker..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="w-full bg-fintech-panel border border-fintech-border rounded-lg py-2.5 lg:py-3 pl-9 lg:pl-10 pr-4 text-white placeholder-fintech-textSec focus:outline-none focus:border-fintech-primary transition-colors text-sm lg:text-base"
                />
            </div>
            <div className="flex bg-fintech-panel p-1 rounded-lg border border-fintech-border w-full lg:w-auto">
                {['ALL', 'BUY', 'SELL'].map(f => (
                    <button
                        key={f}
                        onClick={() => setFilter(f)}
                        className={`flex-1 lg:flex-none px-4 lg:px-6 py-2 lg:py-2.5 rounded-md text-xs lg:text-sm font-medium transition-all ${
                            filter === f
                            ? 'bg-fintech-primary text-white shadow-glow-purple'
                            : 'text-fintech-textSec hover:text-white hover:bg-fintech-card/50'
                        }`}
                    >
                        {f}
                    </button>
                ))}
            </div>
        </div>
      </div>

      {/* Transaction List */}
      <div className="space-y-3">
        {filteredData.map((tx, index) => {
            // Data Processing with null checks
            const action = tx.action ? tx.action.toUpperCase() : 'UNKNOWN'; // 'buy' -> 'BUY'
            const quantity = parseFloat(tx.quantity) || 0;
            const price = parseFloat(tx.price) || 0;
            const totalValue = (quantity * price).toFixed(2);
            const score = parseFloat(tx.movement_score) || 0;

            return (
                <div
                    key={tx.id || tx.crosscheck_id || index}
                    className="bg-fintech-card border border-fintech-border rounded-xl p-4 lg:p-6 hover:border-fintech-primary/50 transition-all group"
                >
                    {/* Mobile-First Layout */}
                    <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4 lg:gap-6">
                        {/* Header Section - Always visible */}
                        <div className="flex items-center gap-3 lg:gap-4 flex-shrink-0">
                            <div className={`w-10 h-10 lg:w-12 lg:h-12 rounded-full flex items-center justify-center ${
                                action === 'BUY' ? 'bg-fintech-bull/10 text-fintech-bull' :
                                'bg-fintech-bear/10 text-fintech-bear'
                            }`}>
                                {action === 'BUY' ? <ArrowDownLeft size={20} className="lg:w-6 lg:h-6" /> : <ArrowUpRight size={20} className="lg:w-6 lg:h-6" />}
                            </div>
                            <div className="min-w-0 flex-1">
                                <div className="flex items-center gap-2 lg:gap-3 mb-1">
                                    <h3 className="text-white font-bold text-lg lg:text-xl truncate">{tx.ticker}</h3>
                                    <span className={`px-2 py-1 rounded-md text-xs font-bold border flex-shrink-0 ${
                                        action === 'BUY' ? 'border-fintech-bull text-fintech-bull bg-fintech-bull/10' :
                                        'border-fintech-bear text-fintech-bear bg-fintech-bear/10'
                                    }`}>
                                        {action}
                                    </span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <Activity size={12} className="text-fintech-primary flex-shrink-0" />
                                    <span className="text-xs lg:text-sm text-fintech-textSec truncate">
                                        Score: <span className="text-white font-mono font-medium">{score.toFixed(2)}</span>
                                    </span>
                                </div>
                            </div>
                        </div>

                        {/* Details Section - Responsive */}
                        <div className="flex-1 min-w-0 lg:ml-6">
                            {/* Financial Details - Responsive grid */}
                            <div className="grid grid-cols-3 gap-3 lg:gap-6 mb-3 lg:mb-4">
                                <div className="text-center">
                                    <p className="text-xs text-fintech-textSec uppercase tracking-wide">Price</p>
                                    <p className="text-white font-mono text-sm lg:text-lg font-semibold truncate">${price.toFixed(2)}</p>
                                </div>
                                <div className="text-center">
                                    <p className="text-xs text-fintech-textSec uppercase tracking-wide">Qty</p>
                                    <p className="text-white font-mono text-sm lg:text-lg font-semibold truncate">{quantity}</p>
                                </div>
                                <div className="text-center">
                                    <p className="text-xs text-fintech-textSec uppercase tracking-wide">Total</p>
                                    <p className="text-white font-bold text-sm lg:text-lg truncate">${totalValue}</p>
                                </div>
                            </div>

                            {/* AI Summary - Responsive */}
                            <div className="bg-fintech-panel/30 p-3 lg:p-4 rounded-lg border border-fintech-border/30">
                                <div className="flex items-start gap-2 lg:gap-3">
                                    <Cpu size={14} className="text-fintech-primary mt-0.5 flex-shrink-0 lg:w-4 lg:h-4" />
                                    <div className="flex-1 min-w-0">
                                        <p className="text-xs lg:text-sm font-medium text-fintech-primary mb-1">AI Analysis</p>
                                        <p className="text-xs lg:text-sm text-fintech-textSec leading-relaxed line-clamp-2 lg:line-clamp-none">{tx.summary || 'No summary available'}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );
        })}

        {filteredData.length === 0 && !loading && (
            <div className="text-center py-12 text-fintech-textSec flex flex-col items-center">
                <AlertCircle size={32} className="mb-2 opacity-50"/>
                No movement records found.
            </div>
        )}
      </div>
    </div>
  );
};

export default History;