import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import { Outlet } from 'react-router-dom';
import { Bell, Search, UserCircle, Menu, X } from 'lucide-react';

const MainLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-fintech-bg font-sans selection:bg-fintech-primary selection:text-white">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <main className="lg:pl-64">
        {/* Header */}
        <header className="h-20 border-b border-fintech-border bg-fintech-bg/80 backdrop-blur-md sticky top-0 z-30 flex items-center justify-between px-4 lg:px-8">
            {/* Mobile Menu Button */}
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden p-2 text-fintech-textSec hover:text-white transition-colors"
            >
              <Menu size={24} />
            </button>

            {/* Search (Mock) */}
            <div className="relative flex-1 max-w-sm sm:max-w-md mx-2 sm:mx-4">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-fintech-textSec" size={18} />
                <input
                    type="text"
                    placeholder="Search..."
                    className="w-full bg-fintech-panel border border-fintech-border rounded-lg py-2 pl-10 pr-4 text-sm text-white focus:outline-none focus:border-fintech-primary transition-colors"
                />
            </div>

            {/* Right Actions */}
            <div className="flex items-center gap-4 lg:gap-6">
                <button className="relative text-fintech-textSec hover:text-white transition-colors">
                    <Bell size={20} />
                    <span className="absolute -top-1 -right-1 w-2 h-2 bg-fintech-primary rounded-full animate-pulse"></span>
                </button>
                <div className="h-8 w-[1px] bg-fintech-border hidden sm:block"></div>
                <div className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity">
                    <div className="text-right hidden lg:block">
                        <p className="text-sm font-medium text-white">Alex Sterling</p>
                        <p className="text-xs text-fintech-textSec">Pro Member</p>
                    </div>
                    <UserCircle size={36} className="text-fintech-textSec" />
                </div>
            </div>
        </header>

        {/* Page Content */}
        <div className="p-3 sm:p-4 lg:p-8 pb-8 lg:pb-12">
            <Outlet />
        </div>
      </main>
    </div>
  );
};

export default MainLayout;