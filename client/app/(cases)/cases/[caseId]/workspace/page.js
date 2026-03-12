import Chatbot from "./components/Chatbot";

export default async function Page({ params }) {
  const { caseId } = await params;
  return <Chatbot caseId={caseId} />;
}
