"use client";

import Link from "next/link";
import { useSession } from "next-auth/react";
import { useState } from "react";
import UserDropdown from "./UserDropdown";

export const Header = () => {
  const session = useSession();
  console.log(session);
  const [openDropdown, setOpenDropdown] = useState(false);
  return (
    <header className="sticky top-0 z-40 w-full border-b-2 border-blue-800 bg-white">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
        <Link href="/" className="font-bold text-blue-800 text-xl">
          CaseBot
        </Link>

        <nav className="flex items-center gap-2 relative">
          {session && session.status === "authenticated" ? (
            <>
              <button
                onClick={() => setOpenDropdown((prev) => !prev)}
                className="w-9 h-9 rounded-full bg-blue-800 text-white font-semibold text-sm flex items-center justify-center uppercase cursor-pointer relative"
              >
                {session?.data?.user.username
                  ? session.data.user.username[0]
                  : "U"}
              </button>
            </>
          ) : (
            <>
              <Link
                href="/auth/signin"
                className="rounded-lg p-2 px-6 text-md bg-blue-800 text-white font-medium transition hover:bg-blue-950"
              >
                Sign in
              </Link>
              <Link
                href="/auth/signup"
                className="rounded-lg p-2 px-6 text-md bg-blue-800 text-white font-medium transition hover:bg-blue-950"
              >
                Sign up
              </Link>
            </>
          )}
          {openDropdown && (
            <UserDropdown openDropDdown={openDropdown} session={session} />
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;
