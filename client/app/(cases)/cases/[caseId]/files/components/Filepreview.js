import { FileText, Loader2, CheckCircle, XCircle, Trash2 } from "lucide-react";
import { filesize } from "filesize";

export default function FilePreview({ file, status, onDelete }) {
  const statusConfig = {
    uploading: {
      icon: <Loader2 className="h-4 w-4 animate-spin text-zinc-400" />,
      label: "Uploading",
      labelClass: "text-zinc-400",
    },
    processing: {
      icon: <Loader2 className="h-4 w-4 animate-spin text-blue-500" />,
      label: "Processing",
      labelClass: "text-blue-500",
    },
    success: {
      icon: <CheckCircle className="h-4 w-4 text-green-500" />,
      label: "Ready",
      labelClass: "text-green-500",
    },
    fail: {
      icon: <XCircle className="h-4 w-4 text-red-500" />,
      label: "Failed",
      labelClass: "text-red-500",
    },
  };

  const { icon, label, labelClass } = statusConfig[status] ?? statusConfig.fail;

  return (
    <div className="mt-3 flex items-center gap-3 rounded-lg border border-zinc-200 bg-white px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900">
      <FileText className="h-5 w-5 shrink-0 text-zinc-400" />

      <div className="min-w-0 flex-1">
        <p className="truncate text-xs font-medium text-zinc-800 dark:text-zinc-100">
          {file.name}
        </p>
        <p className="text-xs text-zinc-400">{file.type || "Unknown format"}</p>
        <p className="text-xs text-zinc-400">{filesize(file.size)}</p>
      </div>

      <div className="flex shrink-0 flex-col items-center gap-1">
        {icon}
        <span className={`text-[10px] font-medium ${labelClass}`}>{label}</span>
        {status === "fail" && (
          <button
            type="button"
            onClick={onDelete}
            className="mt-0.5 text-red-400 transition hover:text-red-600"
          >
            <Trash2 className="h-3.5 w-3.5" />
          </button>
        )}
      </div>
    </div>
  );
}
