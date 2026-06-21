"use client";
import { useState } from "react";
import api from "@/lib/api";
import { AISessionResponse } from "@/types";
import { AlertTriangle, Brain, CheckCircle } from "lucide-react";
import toast from "react-hot-toast";

export default function AIAssistantPage() {
  const [symptom, setSymptom] = useState("");
  const [session, setSession] = useState<AISessionResponse | null>(null);
  const [answers, setAnswers] = useState<string[][]>([]);
  const [result, setResult] = useState<AISessionResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const startSession = async () => {
    if (!symptom.trim()) return;
    setLoading(true);
    try {
      const { data } = await api.post<AISessionResponse>("/ai/symptom/", { symptom });
      setSession(data);
      setAnswers(data.questions?.map(() => []) ?? []);
    } catch {
      toast.error("Could not start session.");
    } finally {
      setLoading(false);
    }
  };

  const submitAnswers = async () => {
    if (!session?.session_id) return;
    setLoading(true);
    try {
      const { data } = await api.post<AISessionResponse>(
        `/ai/session/${session.session_id}/answer/`,
        { answers: answers.flat() }
      );
      setResult(data);
    } catch {
      toast.error("Could not process answers.");
    } finally {
      setLoading(false);
    }
  };

  if (result?.is_emergency) {
    return (
      <div className="max-w-lg mx-auto mt-16 p-8 bg-red-50 border-2 border-red-500 rounded-xl text-center">
        <AlertTriangle className="w-16 h-16 text-red-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-red-700 mb-2">Medical Emergency</h2>
        <p className="text-red-600 whitespace-pre-line">{result.message}</p>
        <p className="mt-4 font-semibold text-red-700">No medicine recommendations.</p>
      </div>
    );
  }

  return (
    <main className="max-w-2xl mx-auto py-12 px-4">
      <div className="flex items-center gap-3 mb-8">
        <Brain className="w-8 h-8 text-green-600" />
        <h1 className="text-2xl font-bold">AI Health Assistant</h1>
      </div>

      {/* Step 1: symptom input */}
      {!session && (
        <div className="card">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Describe your symptom
          </label>
          <input
            className="input mb-4"
            placeholder="e.g. headache, fever, cough..."
            value={symptom}
            onChange={(e) => setSymptom(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && startSession()}
          />
          <button className="btn-primary w-full" onClick={startSession} disabled={loading}>
            {loading ? "Checking..." : "Start Health Check"}
          </button>
        </div>
      )}

      {/* Step 2: questions */}
      {session && !result && session.questions && (
        <div className="space-y-6">
          <p className="text-gray-500 text-sm">
            Please answer these questions to get recommendations:
          </p>
          {session.questions.map((q, qi) => (
            <div key={qi} className="card">
              <p className="font-medium text-gray-800 mb-3">{q.question}</p>
              <div className="space-y-2">
                {q.options.map((opt) => {
                  const selected = answers[qi]?.includes(opt);
                  return (
                    <button
                      key={opt}
                      onClick={() => {
                        const updated = [...answers];
                        if (q.multi) {
                          updated[qi] = selected
                            ? updated[qi].filter((a) => a !== opt)
                            : [...(updated[qi] || []), opt];
                        } else {
                          updated[qi] = [opt];
                        }
                        setAnswers(updated);
                      }}
                      className={`w-full text-left px-4 py-2 rounded-lg border text-sm transition-colors ${
                        selected
                          ? "bg-green-50 border-green-500 text-green-700"
                          : "border-gray-200 hover:border-green-300"
                      }`}
                    >
                      {selected ? "✓ " : ""}{opt}
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
          <button
            className="btn-primary w-full"
            onClick={submitAnswers}
            disabled={loading || answers.some((a) => a.length === 0)}
          >
            {loading ? "Processing..." : "Get Recommendations"}
          </button>
        </div>
      )}

      {/* Step 3: results */}
      {result && !result.is_emergency && (
        <div className="space-y-4">
          <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 text-sm text-amber-800">
            <AlertTriangle className="w-4 h-4 inline mr-2" />
            {result.disclaimer}
          </div>
          <div className="card">
            <p className="text-gray-600 mb-4">{result.advice}</p>
            <h3 className="font-semibold text-gray-800 mb-3">Suggested Products:</h3>
            <div className="space-y-2">
              {result.recommended_products?.map((p) => (
                <div key={p.id} className="flex items-center justify-between py-2 border-b last:border-0">
                  <div>
                    <p className="font-medium text-sm">{p.name}</p>
                    <p className="text-gray-400 text-xs">{p.generic_name}</p>
                  </div>
                  <span className="text-green-700 font-semibold text-sm">SAR {p.price}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
