import { Fragment } from "react";
import { Disclosure, Menu, Transition } from "@headlessui/react";
import { Bars3Icon, BellIcon, XMarkIcon } from "@heroicons/react/24/outline";
import Link from "next/link";
import { useChatContext } from "../Context/ChatContext";
const navigation = [
];
function classNames(
  ...classes: Array<string | number | boolean | null | undefined>
) {
  return classes.filter(Boolean).join(" ");
}

export default function HeaderSection() {
  const useChat = useChatContext();
  return (
    <Disclosure as="nav">
        <>
          <div className="px-6">
            <div className="relative flex h-12 items-center">
              <div className="absolute inset-y-0 left-0 flex items-center sm:hidden">
                <Disclosure.Button className="relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white ml-1">
                  <span className="absolute -inset-0.5" />
                  <span className="sr-only">Open main menu</span>
              
                    <Bars3Icon className="block h-4 w-4" aria-hidden="true" />
                </Disclosure.Button>
              </div>
              <div className="pl-8 sm:pl-2">
                <a
                  href="/"
                  className="bot-font font-semibold tracking-widest text-xs md:text-sm mb-1 flex flex-col"
                >
                  <span className="text-lg md:text-xl text-[#1240AB]">Capstone VTA</span>
                </a>
              </div>
              <div className="flex flex-1 items-center sm:items-stretch sm:justify-start">
                <div className="hidden sm:ml-6 sm:block">
                </div>
              </div>
            </div>
          </div>

          <Disclosure.Panel className="sm:hidden">
            <div className="space-y-1 px-2 pb-3 pt-2 flex flex-col">
               <Link href="/chat" className="bot-font text-xs"> CHAT</Link>
               <Link href="#" className="bot-font text-xs" onClick={()=>useChat.handleModal()}> RATING</Link>
            </div>
          </Disclosure.Panel>
        </>
    </Disclosure>
  );
}
