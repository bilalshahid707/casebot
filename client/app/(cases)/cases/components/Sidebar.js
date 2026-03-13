"use client";

import Link from "next/link";
import { signOut } from "next-auth/react";

export default function Sidebar({ user }) {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 p-6 flex flex-col h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-xl font-bold text-blue-600">LexiBot AI</h1>
      </div>

      {/* Navigation Sections */}
      <nav className="flex-1 space-y-6">
        {/* Case Context Section */}
        <div>
          <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-4">
            Case Context
          </h2>
          <ul className="space-y-3">
            <li>
              <Link
                href="/dashboard/cases/"
                className="text-gray-700 hover:text-blue-600 text-sm transition"
              >
                Workspace
              </Link>
            </li>
            <li>
              <Link
                href="/dashboard/cases"
                className="text-gray-700 hover:text-blue-600 text-sm transition"
              >
                Case Files
              </Link>
            </li>
            <li>
              <Link
                href="/dashboard/cases"
                className="text-gray-700 hover:text-blue-600 text-sm transition"
              >
                AI Summaries
              </Link>
            </li>
            <li>
              <Link
                href="/dashboard/cases"
                className="text-gray-700 hover:text-blue-600 text-sm transition"
              >
                Timeline
              </Link>
            </li>
          </ul>
        </div>

        {/* Management Section */}
        <div>
          <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-4">
            Management
          </h2>
          <ul className="space-y-3">
            <li>
              <Link
                href="/dashboard/cases"
                className="text-gray-700 hover:text-blue-600 text-sm transition"
              >
                Case Graph
              </Link>
            </li>
            <li>
              <Link
                href="/dashboard/cases"
                className="text-gray-700 hover:text-blue-600 text-sm transition"
              >
                Settings
              </Link>
            </li>
          </ul>
        </div>
      </nav>

      {/* Sign Out Button */}
      {user && (
        <button
          onClick={async () => await signOut({ callbackUrl: "/" })}
          className="w-full bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-3 rounded-lg text-sm transition"
        >
          Sign Out
        </button>
      )}
    </aside>
  );
}
