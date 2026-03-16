import Link from "next/link";

export default function FileList({ files }) {
  if (files.length === 0)
    return (
      <p className="text-center text-sm text-gray-500">
        No files uploaded yet.
      </p>
    );

  return (
    <div className="flex flex-col divide-y divide-gray-100 rounded-xl border border-gray-200 bg-white">
      {files.map((file) => {
        return (
          <div
            key={file.id}
            className="flex items-center gap-4 px-5 py-3.5 hover:bg-gray-50 transition"
          >
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
