import React from 'react';
import Card from '../components/Card';
import { mockData } from '../data/mockData';
import { Plus, Send, Download, ArrowUpRight, ArrowDownLeft, CreditCard } from 'lucide-react';

const BankingDashboard = () => {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:justify-between lg:items-end gap-6">
        <div>
            <h2 className="text-xl text-fintech-textSec">Total Liquidity</h2>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-white mt-1">
                {mockData.user.currency}{mockData.banking.checkingBalance.toLocaleString()}
            </h1>
        </div>
        <div className="flex gap-3">
            <button className="flex items-center gap-2 bg-fintech-primary hover:bg-fintech-primaryHover text-white px-4 lg:px-5 py-2.5 rounded-xl transition-all text-sm font-medium">
                <Plus size={18} /> Add Money
            </button>
            <button className="flex items-center gap-2 bg-fintech-card border border-fintech-primary text-fintech-primary hover:bg-fintech-panel px-4 lg:px-5 py-2.5 rounded-xl transition-all text-sm font-medium">
                <Send size={18} /> Transfer
            </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
        {/* Left Column: Cards & Accounts */}
        <div className="lg:col-span-2 space-y-4 lg:space-y-6">
            
            {/* Visual Credit Cards */}
            <h3 className="text-white font-semibold">My Cards</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* Card 1: Purple Gradient */}
                <div className="h-44 sm:h-52 rounded-2xl p-4 sm:p-6 relative bg-gradient-to-br from-[#8A2BE2] to-[#4B0082] shadow-glow-purple transition-transform hover:-translate-y-1 cursor-pointer">
                    <div className="absolute top-0 right-0 w-24 h-24 sm:w-32 sm:h-32 bg-white opacity-10 rounded-full -mr-6 sm:-mr-10 -mt-6 sm:-mt-10 blur-xl"></div>
                    <div className="flex justify-between items-start">
                        <span className="text-white/80 font-medium tracking-wider">NeoBank</span>
                        <CreditCard className="text-white/80" />
                    </div>
                    <div className="mt-6 sm:mt-8">
                        <span className="text-white text-lg sm:text-2xl tracking-widest font-mono">**** **** **** 4829</span>
                    </div>
                    <div className="mt-6 sm:mt-8">
                        {/* Mobile Layout - Stacked */}
                        <div className="block sm:hidden">
                            <div className="flex justify-between items-start">
                                <div className="flex-1 min-w-0 mr-2">
                                    <p className="text-xs text-white/60 uppercase">Card Holder</p>
                                    <p className="text-xs text-white font-medium tracking-wide truncate" style={{maxWidth: '120px'}}>ALEX STERLING</p>
                                </div>
                                <div className="flex-shrink-0">
                                    <p className="text-xs text-white/60 uppercase">Expires</p>
                                    <p className="text-xs text-white font-medium">12/28</p>
                                </div>
                            </div>
                        </div>
                        {/* Desktop Layout - Side by Side */}
                        <div className="hidden sm:flex sm:justify-between sm:items-end">
                            <div className="min-w-0 flex-1">
                                <p className="text-xs text-white/60 uppercase">Card Holder</p>
                                <p className="text-sm text-white font-medium tracking-wide">ALEX STERLING</p>
                            </div>
                            <div className="flex flex-col items-end">
                                <p className="text-xs text-white/60 uppercase">Expires</p>
                                <p className="text-sm text-white font-medium">12/28</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Card 2: Black Minimal */}
                <div className="h-44 sm:h-52 rounded-2xl p-4 sm:p-6 relative bg-fintech-card border border-fintech-border transition-transform hover:-translate-y-1 cursor-pointer group">
                    <div className="flex justify-between items-start">
                        <span className="text-fintech-textSec font-medium tracking-wider">Metal</span>
                        <CreditCard className="text-fintech-textSec group-hover:text-white transition-colors" />
                    </div>
                     <div className="mt-6 sm:mt-8">
                        <span className="text-fintech-textSec group-hover:text-white transition-colors text-lg sm:text-2xl tracking-widest font-mono">**** **** **** 9921</span>
                    </div>
                     <div className="mt-6 sm:mt-8">
                        {/* Mobile Layout - Stacked */}
                        <div className="block sm:hidden">
                            <div className="flex justify-between items-start">
                                <div className="flex-1 min-w-0 mr-2">
                                    <p className="text-xs text-fintech-textSec uppercase">Card Holder</p>
                                    <p className="text-xs text-fintech-textSec group-hover:text-white font-medium tracking-wide truncate" style={{maxWidth: '120px'}}>ALEX STERLING</p>
                                </div>
                                <div className="flex-shrink-0">
                                    <p className="text-xs text-fintech-textSec uppercase">Expires</p>
                                    <p className="text-xs text-fintech-textSec group-hover:text-white font-medium">12/28</p>
                                </div>
                            </div>
                        </div>
                        {/* Desktop Layout - Side by Side */}
                        <div className="hidden sm:flex sm:justify-between sm:items-end">
                            <div className="min-w-0 flex-1">
                                <p className="text-xs text-fintech-textSec uppercase">Card Holder</p>
                                <p className="text-sm text-fintech-textSec group-hover:text-white font-medium tracking-wide">ALEX STERLING</p>
                            </div>
                            <div className="flex flex-col items-end">
                                <p className="text-xs text-fintech-textSec uppercase">Expires</p>
                                <p className="text-sm text-fintech-textSec group-hover:text-white font-medium">12/28</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-2 gap-3 sm:gap-4">
                <Card className="flex items-center gap-2 sm:gap-4 p-4">
                    <div className="p-2 sm:p-3 rounded-full bg-fintech-bull/10 text-fintech-bull flex-shrink-0">
                        <ArrowDownLeft size={20} className="sm:w-6 sm:h-6" />
                    </div>
                    <div className="min-w-0 flex-1">
                        <p className="text-fintech-textSec text-xs truncate">Income (Oct)</p>
                        <p className="text-white font-bold text-sm sm:text-lg truncate">$8,450.00</p>
                    </div>
                </Card>
                <Card className="flex items-center gap-2 sm:gap-4 p-4">
                    <div className="p-2 sm:p-3 rounded-full bg-fintech-bear/10 text-fintech-bear flex-shrink-0">
                        <ArrowUpRight size={20} className="sm:w-6 sm:h-6" />
                    </div>
                    <div className="min-w-0 flex-1">
                        <p className="text-fintech-textSec text-xs truncate">Spend (Oct)</p>
                        <p className="text-white font-bold text-sm sm:text-lg truncate">$3,240.50</p>
                    </div>
                </Card>
            </div>
        </div>

        {/* Right Column: Recent Transactions */}
        <Card className="h-full lg:h-fit">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-white font-semibold">Transactions</h3>
                <button className="text-xs text-fintech-primary hover:text-white">View All</button>
            </div>
            
            <div className="space-y-6">
                {mockData.banking.recentTransactions.map((tx) => (
                    <div key={tx.id} className="flex items-center justify-between group cursor-pointer gap-3">
                        <div className="flex items-center gap-3 min-w-0 flex-1">
                            <div className="w-10 h-10 rounded-full bg-fintech-panel border border-fintech-border flex items-center justify-center text-xl group-hover:border-fintech-primary transition-colors flex-shrink-0">
                                {tx.icon}
                            </div>
                            <div className="min-w-0 flex-1">
                                <h4 className="text-white text-sm font-medium truncate">{tx.to}</h4>
                                <p className="text-xs text-fintech-textSec">{tx.date}</p>
                            </div>
                        </div>
                        <span className={`text-sm font-medium flex-shrink-0 ${tx.amount > 0 ? 'text-fintech-bull' : 'text-white'}`}>
                            {tx.amount > 0 ? '+' : ''}{mockData.user.currency}{Math.abs(tx.amount).toFixed(2)}
                        </span>
                    </div>
                ))}
            </div>
            
            <div className="mt-8 p-4 bg-fintech-panel rounded-xl border border-fintech-border text-center">
                 <p className="text-sm text-fintech-textSec mb-2">Want to grow your wealth?</p>
                 <button className="w-full py-2 bg-fintech-card border border-fintech-primary text-fintech-primary rounded-lg text-sm hover:bg-fintech-primary hover:text-white transition-all">
                    Go to AI Investment Hub
                 </button>
            </div>
        </Card>
      </div>
    </div>
  );
};

export default BankingDashboard;