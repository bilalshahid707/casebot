"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { useSession } from "next-auth/react";
import axios from "axios";
import FileUploader from "./FileUploader";
import { Ellipsis } from "lucide-react";
import Link from "next/link";
import ChatInterface from "./ChatInterface";

export default function CasePage({ caseId, caseData }) {
  const session = useSession();

  return (
    <div className="flex h-screen bg-white font-sans text-gray-900">
      {/* Sidebar */}
      <aside className="flex w-72 flex-col border-r border-gray-200 bg-gray-50 px-6 py-6 overflow-y-auto max-h-full">
        <div className="mb-6 rounded-lg bg-white p-4 shadow-sm border border-gray-200">
          <p className="text-xs font-semibold uppercase tracking-widest text-blue-600 mb-2">
            Case Information
          </p>

          <p className="text-sm font-semibold text-gray-900 break-all">
            ID: <span className="font-mono text-blue-700">#{caseData.id}</span>
          </p>

          <p className="text-sm font-semibold text-gray-900">
            Case No:{" "}
            <span className="font-mono text-blue-700">
              #{caseData.case_number}
            </span>
          </p>

          <p className="text-sm text-gray-900">
            Name:{" "}
            <span className="font-medium text-gray-700">
              {caseData.case_name}
            </span>
          </p>

          {caseData.opposing_party && (
            <p className="text-sm text-gray-900">
              Opposing Party:{" "}
              <span className="font-medium text-gray-700">
                {caseData.opposing_party}
              </span>
            </p>
          )}

          {caseData.client && (
            <p className="text-sm text-gray-900">
              Client:{" "}
              <span className="font-medium text-gray-700">
                {caseData.client}
              </span>
            </p>
          )}

          <p className="text-sm text-gray-900">
            Status:{" "}
            <span
              className={`inline-block rounded-full px-2 py-0.5 text-xs font-semibold ${
                caseData.status === "active"
                  ? "bg-green-100 text-green-700"
                  : caseData.status === "closed"
                    ? "bg-red-100 text-red-700"
                    : "bg-zinc-100 text-zinc-600"
              }`}
            >
              {caseData.status}
            </span>
          </p>
        </div>

        <div className="flex flex-col gap-2">
          <FileUploader caseId={caseId} />

          <div className="flex flex-col gap-2">
            <h2>All files</h2>
            {caseData?.assets.map((asset) => (
              <Link
                key={asset.id}
                href={asset.url}
                target="_blank"
                rel="noopener noreferrer"
                className="font-normal text-xs text-blue-600"
              >
                {asset.name}
              </Link>
            ))}
          </div>
        </div>
      </aside>

      <div className="flex-1">
        <ChatInterface caseId={caseId} />
      </div>
    </div>
  );
}
