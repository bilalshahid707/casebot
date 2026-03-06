"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { signOut } from "next-auth/react";
import { LayoutDashboard, LogOut } from "lucide-react";

export default function UserDropdown({ session, openDropDdown }) {
  const [open, setOpen] = useState(openDropDdown);
  const dropdownRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="absolute top-12 right-0 z-50 " ref={dropdownRef}>
      {/* Dropdown */}
      {open && (
        <div className="w-44 bg-white rounded-xl shadow-lg border border-slate-100 py-1">
          <Link
            href="/dashboard/cases"
            onClick={() => setOpen(false)}
            className="flex items-center gap-2.5 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50"
          >
            <LayoutDashboard size={15} className="text-slate-400" />
            Dashboard
          </Link>
          <hr className="my-1 border-slate-100" />
          <button
            onClick={async () => await signOut()}
            className="w-full flex items-center gap-2.5 px-4 py-2.5 text-sm text-red-500 hover:bg-red-50 cursor-pointer"
          >
            <LogOut size={15} className="text-red-400" />
            Sign out
          </button>
        </div>
      )}
    </div>
  );
}
