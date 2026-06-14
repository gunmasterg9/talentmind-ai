import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TalentMind AI - Intelligent Recruiter Dashboard",
  description: "AI-Powered Candidate Discovery and Ranking Engine",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased selection:bg-purple-900 selection:text-purple-200">
        {children}
      </body>
    </html>
  );
}
