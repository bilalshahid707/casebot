import Graphpage from "./components/Graphpage";

export default async function Page({ params }) {
  const { caseId } = await params;
  return <Graphpage caseId={caseId} />;
}
