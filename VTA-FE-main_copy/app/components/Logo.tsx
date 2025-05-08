import Image from 'next/image';
import React from 'react';

export default function Logo() {
  return (
    <div className="fixed top-4 right-6 z-50">
      <Image
        src="/constructor-logo.png"
        alt="Constructor Institute of Technology Logo"
        width={120}
        height={60}
        className="object-contain rounded-lg"
      />
    </div>
  );
} 