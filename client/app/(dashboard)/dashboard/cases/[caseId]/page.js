import { notFound, redirect } from "next/navigation";
import { auth } from "@/auth";
import CasePage from "./components/CasePage";

export default async function Page({ params }) {
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

  return <CasePage caseId={caseId} caseData={caseData.data} />;
}
