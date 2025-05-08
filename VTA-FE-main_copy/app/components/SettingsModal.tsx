import React, { useState, useEffect } from 'react';
import { useChatContext } from '../Context/ChatContext';
import { CiCircleRemove } from "react-icons/ci";

export default function SettingsModal({ isOpen }: { isOpen: boolean }) {
  const useChat = useChatContext();
  const [instructions, setInstructions] = useState(useChat.customInstructions);

  useEffect(() => {
    setInstructions(useChat.customInstructions);
  }, [useChat.customInstructions]);

  const handleSave = () => {
    useChat.updateCustomInstructions(instructions);
  };

  const handleClearHistory = () => {
    localStorage.removeItem("VTAChatHistory");
    window.location.reload();
  };

  return (
    <div
      className={`sm:w-full md:w-2/3 h-[75vh] main-sec-v2-bg-color absolute top-6 bottom-4 left-[15%] mx-4 m-auto rounded z-10 overflow-y-auto ${
        !isOpen && "hidden"
      }`}
    >
      <div className="flex justify-between px-4 py-3 flex-nowrap items-center border-b border-[#1240AB]/20">
        <h5 className="bot-font tracking-widest text-base font-bold">
          Chat settings
        </h5>
        <div 
          className="p-2 hover:bg-[#1240AB]/10 hover:scale-110 hover:cursor-pointer rounded-full"
          onClick={() => useChat.handleSettingsModal()}
        >
          <CiCircleRemove size={30} className="text-[#1240AB]" />
        </div>
      </div>
      <div className="px-4 pt-3 text-[#1240AB]">
        <div className="space-y-5">
          <div>
            <label className="block text-sm font-medium mb-2">Custom instructions</label>
            <textarea
              className="w-full h-36 p-3 rounded bg-white/90 text-sm"
              placeholder="Add your custom instructions here..."
              value={instructions}
              onChange={(e) => setInstructions(e.target.value)}
            />
            <button
              onClick={handleSave}
              className="mt-3 px-6 py-2 bg-[#1240AB] text-white rounded hover:bg-[#1240AB]/90 text-sm"
            >
              Save Instructions
            </button>
          </div>

          <div className="border-t border-[#1240AB]/20 pt-3">
            <button
              onClick={handleClearHistory}
              className="mt-3 px-6 py-2 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
            >
              Clear Chat History
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 