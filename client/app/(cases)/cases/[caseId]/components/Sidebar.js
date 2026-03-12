"use client";

import Link from "next/link";
import { redirect } from "next/navigation";

export default function Sidebar({ caseId }) {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 p-6 flex flex-col h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-xl font-bold text-blue-600">Casebot</h1>
      </div>

      {/* Navigation Sections */}
      <nav className="flex-1 space-y-6">
        {/* Case Context Section */}
        <div>
          <h2 className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-4">
            Case Context
          </h2>
          <ul className="space-y-3">
            <li>
              <Link
                href={`/cases/${caseId}/workspace`}
                className="text-gray-700 hover:text-blue-600 text-sm transition"
              >
                Workspace
              </Link>
            </li>
            <li>
              <Link
                href={`/cases/${caseId}/files`}
                className="text-gray-700 hover:text-blue-600 text-sm transition"
              >
                Case Files
              </Link>
            </li>

            <li>
              <Link
                href={`/cases/${caseId}/graph`}
                className="text-gray-700 hover:text-blue-600 text-sm transition"
              >
                Case Graph
              </Link>
            </li>
          </ul>
        </div>
      </nav>

      <button
        onClick={() => redirect("/dashboard/cases")}
        className="w-full cursor-pointer bg-blue-800  text-white font-medium py-2 px-3 rounded-lg text-sm transition"
      >
        back to dashboard
      </button>
    </aside>
  );
}
