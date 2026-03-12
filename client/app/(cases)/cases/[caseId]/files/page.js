import Filespage from "./components/Filespage";

export default async function Page({ params }) {
  const { caseId } = await params;
  return <Filespage caseId={caseId} />;
}
