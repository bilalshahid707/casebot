"use client";

import { useRef, useState } from "react";
import { useSession } from "next-auth/react";
import axios from "axios";
import Filepreview from "./Filepreview";
import { Upload } from "lucide-react";

export default function Fileuploader({ caseId }) {
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

    await Promise.all(
      newFiles.map(async (fileData) => {
        const formData = new FormData();
        formData.append("file", fileData.file);
        try {
          const { data } = await axios.post(
            `${process.env.NEXT_PUBLIC_API_URL}/cases/${caseId}/assets/upload`,
            formData,
            {
              headers: {
                Authorization: `Bearer ${session?.data?.accessToken}`,
              },
            },
          );

          setFiles((prev) =>
            prev.map((f) =>
              f.id === fileData.id ? { ...f, status: "processing" } : f,
            ),
          );

          await axios.post(
            `${process.env.NEXT_PUBLIC_API_URL}/cases/${caseId}/assets/${data.id}/process`,
            null,
            {
              headers: {
                Authorization: `Bearer ${session?.data?.accessToken}`,
              },
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
      }),
    );
  };

  return (
    <>
      {/* Drop zone */}
      <div
        onClick={handleUploadClick}
        className="cursor-pointer rounded-xl border-2 border-dashed border-gray-300 bg-gray-50 px-6 py-10 text-center hover:border-blue-400 hover:bg-blue-50 transition"
      >
        <Upload className="mx-auto mb-3 text-gray-400" size={28} />
        <p className="text-sm font-medium text-gray-700">
          Drag and drop files here
        </p>
        <p className="mt-1 text-xs text-gray-500">PDF, DOCX, TXT up to 50MB</p>
        <button
          type="button"
          className="mt-4 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 transition"
        >
          Browse Files
        </button>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        multiple
        className="hidden"
        onChange={handleFilesSelected}
      />

      {uploadError && (
        <p className="mt-3 text-xs text-red-600">⚠️ {uploadError}</p>
      )}

      <div className="mt-6 text-xs text-zinc-500">
        <p className="font-medium text-zinc-700">Files & processing</p>
        <p className="mt-1">
          After uploading, CaseBot will process your documents and use them to
          answer questions in the chat.
        </p>
      </div>

      <div>
        {files.length > 0 &&
          files.map((file) => (
            <Filepreview
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
