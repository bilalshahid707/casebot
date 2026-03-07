"use client";

import Link from "next/link";
import { signOut } from "next-auth/react";
import { usePathname } from "next/navigation";

export default function Sidebar({ user }) {
  const pathname = usePathname();
  const displayName = user?.username || user?.name || "User";
  return (
    <aside className="flex w-64 flex-col bg-blue-800 p-4 ">
      {/* User row */}
      <div className="mb-4 flex items-center gap-3 rounded-md bg-blue-700 p-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-white text-md font-bold text-blue-800 ">
          {user ? (displayName[0] || "U").toUpperCase() : "?"}
        </div>
        <div className="flex">
          <span className="text-md font-semibold text-white">
            {displayName}
          </span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="mt-6 flex flex-col flex-1 space-y-2">
        <Link
          href="/dashboard/cases"
          className={`${
            pathname.includes("/dashboard/cases")
              ? "bg-blue-600 text-white"
              : "text-blue-100 hover:bg-blue-700 hover:text-white"
          } flex items-center gap-2 rounded-lg px-3 py-2.5 text-sm font-medium transition`}
        >
          <span>Cases</span>
        </Link>
      </nav>

      {/* Sign out at bottom */}
      {user && (
        <>
          <Link
            type="button"
            href={"/dashboard/cases"}
            className="mt-4 inline-flex items-center justify-center rounded-lg px-3 py-2 text-sm font-medium transition bg-blue-500 hover:text-white"
          >
            Go back
          </Link>
          <button
            type="button"
            onClick={async () => await signOut({ callbackUrl: "/" })}
            className="mt-4 inline-flex items-center justify-center rounded-lg px-3 py-2 text-sm font-medium text-red-600 transition bg-white hover:bg-blue-700 hover:text-white"
          >
            Sign out
          </button>
        </>
      )}
    </aside>
  );
}
