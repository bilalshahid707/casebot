"use client";

import { useRef, useState } from "react";
import { useSession } from "next-auth/react";
import axios from "axios";
import FilePreview from "./FilePreview";

export default function FileUploader({ caseId }) {
  const session = useSession();
  const fileInputRef = useRef(null);
  const [files, setFiles] = useState([]);
  const [uploadError, setUploadError] = useState("");

  const handleUploadClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFilesSelected = async (event) => {
    const fileList = event.target.files;
    if (!fileList) return;
    setUploadError("");

    const newFiles = Array.from(fileList).map((file) => ({
      id: crypto.randomUUID(),
      name: file.name,
      status: "uploading",
      file,
    }));

    setFiles((prev) => [...prev, ...newFiles]);

    newFiles.forEach(async (fileData) => {
      const formData = new FormData();
      formData.append("file", fileData.file);
      try {
        const { data } = await axios.post(
          `${process.env.NEXT_PUBLIC_API_URL}/cases/${caseId}/assets/upload`,
          formData,
          {
            headers: { Authorization: `Bearer ${session?.data?.accessToken}` },
          },
        );

        setFiles((prev) =>
          prev.map((f) =>
            f.id === fileData.id ? { ...f, status: "processing" } : f,
          ),
        );

        await axios.post(
          `${process.env.NEXT_PUBLIC_API_URL}/cases/${caseId}/assets/${data.data.id}/process`,
          formData,
          {
            headers: { Authorization: `Bearer ${session?.data?.accessToken}` },
          },
        );

        setFiles((prev) =>
          prev.map((f) =>
            f.id === fileData.id ? { ...f, status: "success" } : f,
          ),
        );
        if (fileInputRef.current) fileInputRef.current.value = "";
      } catch (error) {
        setFiles((prev) =>
          prev.map((f) =>
            f.id === fileData.id ? { ...f, status: "fail" } : f,
          ),
        );
        setUploadError(
          error?.response?.data?.message || "Failed to upload file.",
        );
      }
    });
  };

  return (
    <>
      <button
        type="button"
        onClick={handleUploadClick}
        className="flex items-center justify-center rounded-lg bg-zinc-900 px-3 py-2 text-sm font-medium text-zinc-50 shadow-sm transition hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-70 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200"
      >
        Upload case files
      </button>

      <input
        ref={fileInputRef}
        type="file"
        multiple
        className="hidden"
        onChange={handleFilesSelected}
      />

      {uploadError && (
        <p className="mt-3 text-xs text-red-600 dark:text-red-400">
          {uploadError}
        </p>
      )}

      <div className="mt-6 text-xs text-zinc-500 dark:text-zinc-400">
        <p className="font-medium text-zinc-700 dark:text-zinc-200">
          Files & processing
        </p>
        <p className="mt-1">
          After uploading, CaseBot will process your documents and use them to
          answer questions in the chat.
        </p>
      </div>

      <div>
        {files.length > 0 &&
          files.map((file) => (
            <FilePreview
              key={file.id}
              file={file.file}
              status={file.status}
              onDelete={() =>
                setFiles((prev) => prev.filter((f) => f.id !== file.id))
              }
            />
          ))}
      </div>
    </>
  );
}
