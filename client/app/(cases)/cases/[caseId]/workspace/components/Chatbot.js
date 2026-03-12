"use client";

import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { useSession } from "next-auth/react";
import { Ellipsis, Divide } from "lucide-react";
import { useId } from "react";
export default function Chatbot({ caseId }) {
  const queryClient = useQueryClient();
  const session = useSession();
  const uid = useId();
  const [input, setInput] = useState("");
  const [chatError, setChatError] = useState("");

  const { data: messages = [], isPending } = useQuery({
    queryKey: [caseId, "chats"],
    queryFn: async () => {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/cases/${caseId}/conversation`,
        {
          headers: {
            Authorization: `Bearer ${session?.data?.accessToken}`,
          },
        },
      );
      return response.data.data;
    },
  });

  console.log(messages);

  const chatMutation = useMutation({
    mutationFn: async (message) => {
      const { data } = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/cases/${caseId}/chat`,
        { message },
        { headers: { Authorization: `Bearer ${session?.data?.accessToken}` } },
      );
      return data;
    },
    onSuccess: (data) => {
      setChatError("");
      queryClient.setQueryData([caseId, "chats"], (old) => [
        ...old,
        { id: `${uid}-${Date.now()}`, role: "assistant", content: data?.reply },
      ]);
    },
    onError: (error) => {
      setChatError(
        error?.response?.data?.message ||
          error?.response?.data?.detail ||
          error?.message ||
          "Failed to send message.",
      );
    },
  });

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!input.trim() || chatMutation.isPending) return;
    const text = input.trim();

    // Add user message directly to query cache
    queryClient.setQueryData([caseId, "chats"], (old) => [
      ...(old ?? []),
      { id: `${uid}-${Date.now()}`, role: "user", content: text },
    ]);

    setInput("");
    setChatError("");
    chatMutation.mutate(text);
  };
  return (
    <div className="flex h-screen overflow-y-hidden w-full flex-col bg-white">
      <header className="flex items-center justify-between border-b border-gray-200 bg-white px-8 py-5 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Case Chat</h1>
          <p className="mt-1 text-sm text-gray-600">
            Ask questions and get AI-powered answers based on this case&apos;s
            documents.
          </p>
        </div>
      </header>

      <section className="flex-1 overflow-y-auto bg-gray-50 px-8 py-6">
        <div className="flex flex-col gap-4 w-full">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="text-4xl mb-4">💬</div>
              <p className="text-sm text-gray-600 max-w-xs">
                Start by asking a question about this case or uploading files in
                the sidebar.
              </p>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={message.id ?? index}
              className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[70%] h-max rounded-xl flex flex-col gap-2 px-4 py-3 text-sm shadow-sm ${
                  message.role === "user"
                    ? "bg-blue-600 text-white rounded-br-none"
                    : "bg-white text-gray-900 border border-gray-200 rounded-bl-none"
                }`}
              >
                <p
                  className={`${
                    message.role === "assistant"
                      ? "border-b border-zinc-600 pb-2"
                      : ""
                  }`}
                >
                  {message.content?.response ?? message.content}
                </p>

                <div>
                  {(message?.content?.citations ?? message?.citations)?.length >
                    0 && (
                    <ol>
                      {(message?.content?.citations ?? message?.citations).map(
                        (citation, index) => (
                          <li className="text-zinc-600" key={index}>
                            {`source: ${citation.source}`}
                            {citation.page !== 0
                              ? `, page: ${citation.page}`
                              : ""}
                          </li>
                        ),
                      )}
                    </ol>
                  )}
                </div>
              </div>
            </div>
          ))}

          {chatMutation.isPending && (
            <div className="flex justify-start rounded-lg w-max animate-pulse p-2 bg-white shadow-sm">
              <Ellipsis color="blue" size={40} />
            </div>
          )}

          {chatError && (
            <div className="mx-auto w-full max-w-3xl">
              <p className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700 border border-red-200">
                ⚠️ {chatError}
              </p>
            </div>
          )}
        </div>
      </section>
      <form
        onSubmit={handleSubmit}
        className="border-t border-gray-200 bg-white px-8 py-5 shadow-lg"
      >
        <div className="flex w-full items-end gap-3">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask something about this case..."
            className="max-h-32 flex-1 resize-none rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 shadow-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
          />
          <button
            type="submit"
            disabled={!input.trim() || chatMutation.isPending}
            className="inline-flex items-center justify-center rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {chatMutation.isPending ? "Sending..." : "Send"}
          </button>
        </div>
      </form>
    </div>
  );
}
