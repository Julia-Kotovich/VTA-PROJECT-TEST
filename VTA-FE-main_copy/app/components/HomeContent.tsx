import Image from 'next/image';
import React from 'react'

export default function HomeContent() {
  return (
    <section className="flex flex-col gap-3 justify-center items-center h-[75vh] border-2 rounded-md mb-2">
      <div>
        <Image src="/bot.svg" alt="star-icon" width={100} height={100} />
      </div>
      
      <div className="max-w-4xl text-center px-6 space-y-4 text-[#1240AB]">
        <p className="text-lg">
          👋 Welcome to the <span className="font-semibold">Virtual Teaching Assistant (VTA)</span> <br />
          for the Capstone Project Course by Prof. Manuel Oriol!
        </p>
        
        <p className="text-xs">
          👩‍💻 This VTA was developed by Julia Kotovich, PhD student at the Chair of Quantum Software Engineering, <br />
          Constructor Institute of Technology. <br />
        </p>
        
        <p className="text-xs">
          🎯 This VTA is trained on the official course materials to help you find quick, accurate answers to your questions <br />
          — fully offline. 📵
        </p>
        
        <p className="text-xs">
          💾 Your chat history is saved locally in your browser and will persist until you clear it manually in settings. <br />
          The history is device-specific and not synchronized across different browsers or devices. <br />
          You can download your chat history as a PDF file in the chat section.
        </p>
        
        <p className="text-xs">
          📝 P.S. Feel free to try it out and leave your thoughts in the "feedback" tab — your input is highly appreciated!
        </p>
      </div>

      {/* <div className="text-center main-prm-color">
        <h5 className="flex flex-col gap-2">
          <span>
            Hi, I am your <span className="bot-font text-lg">Virtual Teaching Assistant</span>
          </span>
          <span>
            for Capstone Project Course.
          </span>
          <span className="bot-font">
            How can I help you?
          </span>
        </h5>
      </div> */}
    </section>
  );
}
