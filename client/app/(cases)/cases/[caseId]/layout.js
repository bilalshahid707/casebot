import { Poppins } from "next/font/google";
import Sidebar from "./components/Sidebar";
import Providers from "@/app/providers";
import { auth } from "@/auth";
import "@/app/globals.css";
import { notFound, redirect } from "next/navigation";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["300", "400", "700"],
  variable: "--font-poppins",
});

export const metadata = {
  title: "Case Details",
  description: "Case details page",
};

export default async function CaseLayout({ children, params }) {
  const { caseId } = await params;
  const session = await auth();

  if (!session) redirect("/auth/signin");

  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/cases/${caseId}`,
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${session?.accessToken}`,
      },
    },
  );

  if (!res.ok) notFound();

  const caseData = await res.json();

  return (
    <html>
      <body className={`${poppins.variable} antialiased bg-white w-full`}>
        <div className="flex min-h-screen font-sans text-zinc-950">
          <Providers session={session}>
            <Sidebar caseId={caseData?.id} />
            {children}
          </Providers>
        </div>
      </body>
    </html>
  );
}
