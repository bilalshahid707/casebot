"use client";

import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { useSession } from "next-auth/react";
import Filelist from "./Filelist";
import Fileuploader from "./Fileuploader";

export default function FilesPage({ caseId }) {
  const { data: session } = useSession();

  const { data: files = [], isPending } = useQuery({
    queryKey: [caseId, "files"],
    queryFn: async () => {
      const res = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/cases/${caseId}/assets`,
        { headers: { Authorization: `Bearer ${session?.accessToken}` } },
      );
      return res.data.data;
    },
  });

  return (
    <div className="flex h-screen overflow-y-auto w-full flex-col bg-white">
      <header className="flex items-center justify-between border-b border-gray-200 bg-white px-8 py-5 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Case Files</h1>
          <p className="mt-1 text-sm text-gray-600">
            {files.length} document{files.length !== 1 ? "s" : ""} uploaded
          </p>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto px-8 py-6 flex flex-col gap-6">
        <Fileuploader caseId={caseId} />

        {isPending ? (
          <div className="flex flex-col gap-2">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="h-14 rounded-lg bg-gray-100 animate-pulse"
              />
            ))}
          </div>
        ) : (
          <Filelist files={files} />
        )}
      </div>
    </div>
  );
}
