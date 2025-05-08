import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import "@fontsource/orbitron"; // Defaults to weight 400
import "@fontsource/orbitron/400.css"; // Specify weight
import "react-toastify/dist/ReactToastify.css";
import Logo from "./components/Logo";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "CAPSTONE VTA",
  description: "Virtual Teaching Assistant For Capstone Project",
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Logo />
        {children}
      </body>
    </html>
  );
}
