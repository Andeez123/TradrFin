import React from 'react';
import { Wallet, LineChart, PieChart, Activity, Bot, ArrowRightLeft, History, X } from 'lucide-react';
import { NavLink } from 'react-router-dom';

const Sidebar = ({ isOpen, onClose }) => {
  const navItems = [
    // Banking Group
    { icon: Wallet, label: "My Banking", path: "/" },
    { icon: ArrowRightLeft, label: "Transfers", path: "/transfers" },

    // AI Investment Group (The special feature)
    { icon: LineChart, label: "AI Invest", path: "/ai-invest" }, // New Main Entry for AI
    { icon: History, label: "History", path: "/history" },
    { icon: PieChart, label: "Sentimental", path: "/sentiment" },
    { icon: Activity, label: "Market Data Analysis", path: "/technicals" },
    { icon: Bot, label: "AI Advisor", path: "/advisor" },
  ];

  return (
    <div className={`w-64 h-screen bg-fintech-panel border-r border-fintech-border flex flex-col fixed left-0 top-0 z-50 transform transition-transform duration-300 ease-in-out ${
      isOpen ? 'translate-x-0' : '-translate-x-full'
    } lg:translate-x-0`}>
      {/* Mobile Close Button */}
      <button
        onClick={onClose}
        className="lg:hidden absolute top-4 right-4 p-2 text-fintech-textSec hover:text-white transition-colors"
      >
        <X size={24} />
      </button>

      <div className="p-8">
        <h1 className="text-2xl font-bold text-white tracking-tight">
          Tradr<span className="text-fintech-primary">Fin</span>
        </h1>
        <p className="text-xs text-fintech-textSec mt-1">Digital Banking + AI</p>
      </div>

      <nav className="flex-1 px-4 space-y-2">
        {navItems.map((item, index) => (
          <React.Fragment key={item.path}>
             {/* Add a separator label before the AI section */}
             {index === 2 && (
                <div className="pt-4 pb-2 px-4 text-xs font-semibold text-fintech-textSec/50 uppercase tracking-wider">
                    Investment Intelligence
                </div>
             )}
             <NavLink
                to={item.path}
                onClick={onClose}
                className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                    isActive
                    ? "bg-fintech-primary text-white shadow-glow-purple"
                    : "text-fintech-textSec hover:bg-fintech-card hover:text-white"
                }`
                }
            >
                <item.icon size={20} />
                <span className="font-medium text-sm">{item.label}</span>
            </NavLink>
          </React.Fragment>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;