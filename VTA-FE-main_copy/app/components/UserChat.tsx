import React from 'react'
import { CiUser } from "react-icons/ci";

export default function UserChat({message}:{message:string}) {
  return (
    <>
      <div className="mb-0.5">
        <div className="bg-[#F5F5F5] p-1 rounded-full h-[1.5rem] w-[1.5rem] flex justify-center items-center">
          <CiUser size={14} className="text-[#1240AB] stroke-[1]" />
        </div>
        <div className="ms-6 -mt-1">
          <p className="w-[95%] text-[#1240AB] text-xs sm:text-[0.85rem] leading-snug">
            {message}
          </p>
        </div>
      </div>
    </>
  );
}
