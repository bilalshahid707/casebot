import { FileText, FileImage, File, Trash2 } from "lucide-react";
import { filesize } from "filesize";
import Link from "next/link";

function getFileIcon(filename) {
  const ext = filename?.split(".").pop()?.toLowerCase();
  if (["jpg", "jpeg", "png", "gif", "webp"].includes(ext)) return FileImage;
  if (["pdf", "doc", "docx", "txt"].includes(ext)) return FileText;
  return File;
}

export default function FileList({ files }) {
  console.log(files);
  if (files.length === 0)
    return (
      <p className="text-center text-sm text-gray-500">
        No files uploaded yet.
      </p>
    );

  return (
    <div className="flex flex-col divide-y divide-gray-100 rounded-xl border border-gray-200 bg-white">
      {files.map((file) => {
        const Icon = getFileIcon(file.asset_name);
        return (
          <div
            key={file.id}
            className="flex items-center gap-4 px-5 py-3.5 hover:bg-gray-50 transition"
          >
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-blue-50">
              <Icon size={18} className="text-blue-600" />
            </div>
            <div className="flex-1 min-w-0">
              <Link
                href={`${file.asset_URL}`}
                className="truncate text-sm font-medium text-blue"
              >
                {file.asset_name}
              </Link>
            </div>
          </div>
        );
      })}
    </div>
  );
}
