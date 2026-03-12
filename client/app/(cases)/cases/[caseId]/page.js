import { redirect } from "next/navigation";

export default async function Page({ params }) {
  const { caseId } = await params;
  redirect(`/cases/${caseId}/workspace`);
}
