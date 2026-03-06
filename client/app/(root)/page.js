"use client";

import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import {
  UserPlus,
  FolderPlus,
  Upload,
  MessageSquare,
  ArrowRight,
  Sparkles,
} from "lucide-react";
export default function Home() {
  const router = useRouter();
  const session = useSession();

  const handleCreateCase = () => {
    if (session) {
      router.push("/dashboard/cases");
    } else {
      router.push("/auth/signin");
    }
  };

  const steps = [
    {
      id: 1,
      label: "Signup",
      description: "Create your free account in seconds",
      icon: UserPlus,
    },
    {
      id: 2,
      label: "Create your case",
      description: "Set up your legal case details",
      icon: FolderPlus,
    },
    {
      id: 3,
      label: "Upload case files",
      description: "Add documents, evidence & notes",
      icon: Upload,
    },
    {
      id: 4,
      label: "Start chatting",
      description: "AI-powered insights, instantly",
      icon: MessageSquare,
    },
  ];
  return (
    <main className="bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Messages / Welcome */}
      <section className="h-full w-full p-12">
        <div className="mx-auto flex flex-col gap-4 items-center h-full max-w-7xl p-12">
          <div className="w-full flex flex-col items-center justify-center gap-2">
            <h2 className="text-5xl font-bold text-black">
              Simplify Your{" "}
              <span className="text-blue-800">Case Management</span>
            </h2>
            <p className="text-black text-center font-normal">
              Upload your documents and let our AI analyze, organize, and
              extract key insights instantly so you can focus on winning your
              case. Secure, efficient and built for modern law pofessionals
            </p>
          </div>

          <div className="min-h-screen  flex items-center justify-center px-6 py-16">
            <div className="w-full max-w-4xl">
              {/* Header */}
              <div className="text-center mb-14">
                <div className="inline-flex items-center gap-1.5 bg-blue-50 border border-blue-100 rounded-full px-4 py-1.5 mb-5">
                  <Sparkles size={13} className="text-blue-500" />
                  <span className="text-xs font-semibold text-blue-500 uppercase tracking-widest">
                    How it works
                  </span>
                </div>
                <h2 className="text-4xl font-bold text-slate-800 mb-3">
                  Four steps to <span className="text-blue-600">clarity.</span>
                </h2>
                <p className="text-slate-500 text-base">
                  From signup to AI-powered legal insights — in minutes.
                </p>
              </div>

              <div className="flex items-center mb-14">
                {steps.map((step, idx) => {
                  const Icon = step.icon;
                  return (
                    <div
                      key={step.id}
                      className="flex items-center flex-1 min-w-0"
                    >
                      <div className="flex-1 bg-white rounded-2xl p-6 border border-slate-200 relative overflow-hidden">
                        <div className="absolute top-3.5 right-3.5 w-5 h-5 rounded-full bg-slate-100 flex items-center justify-center text-[10px] font-bold text-slate-400">
                          {step.id}
                        </div>

                        <div className="w-12 h-12 rounded-2xl bg-blue-600 flex items-center justify-center mb-4 shadow-md shadow-blue-200">
                          <Icon size={20} color="#ffffff" strokeWidth={2} />
                        </div>

                        <p className="text-sm font-bold text-slate-800 mb-1 leading-snug">
                          {step.label}
                        </p>

                        <p className="text-xs text-slate-400 leading-relaxed">
                          {step.description}
                        </p>
                      </div>

                      {idx < steps.length - 1 && (
                        <div className="flex items-center px-2 shrink-0">
                          <ArrowRight
                            size={16}
                            className="text-blue-200"
                            strokeWidth={2.5}
                          />
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              <div className="text-center">
                <button
                  onClick={handleCreateCase}
                  className="inline-flex items-center gap-2.5 bg-blue-600 text-white text-sm font-semibold px-8 py-4 rounded-xl shadow-lg shadow-blue-200 cursor-pointer border-0"
                >
                  <FolderPlus size={17} strokeWidth={2.2} />
                  Create your case
                  <ArrowRight size={15} strokeWidth={2.5} />
                </button>
                <p className="mt-3.5 text-xs text-slate-400">
                  No credit card required · Free to start
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
