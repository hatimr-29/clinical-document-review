import React from 'react';
import { ShieldAlert, Info } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-slate-200 mt-auto py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <div className="flex items-center space-x-2 text-xs text-slate-500">
            <Info className="w-4 h-4 text-blue-600 flex-shrink-0" />
            <span>
              <strong>ClinReview AI v1.0.0</strong> – Educational Demonstration & Clinical Document Review Tool.
            </span>
          </div>
          <div className="flex items-center space-x-2 bg-amber-50 text-amber-800 border border-amber-200 px-3 py-1.5 rounded-md text-xs">
            <ShieldAlert className="w-4 h-4 text-amber-600 flex-shrink-0" />
            <span>
              All data presented is synthetic. Not intended for direct medical diagnosis or treatment decisions.
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};
