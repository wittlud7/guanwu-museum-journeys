import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "观物 · 城市博物馆指南",
  description: "11城博物馆、文物观察与随行伴游。",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className="antialiased">{children}</body>
    </html>
  );
}
