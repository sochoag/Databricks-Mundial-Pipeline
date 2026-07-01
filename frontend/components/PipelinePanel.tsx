"use client";

import { useEffect, useState } from "react";
import { api, PipelineStack } from "@/lib/api";

const ICONS: Record<string, string> = {
  ingestion: "✈",
  storage: "🗄",
  transformation: "⚡",
  modeling: "🧱",
  serving: "🔌",
  frontend: "🌐",
};

const COLORS: Record<string, string> = {
  ingestion: "border-blue-500",
  storage: "border-yellow-500",
  transformation: "border-orange-500",
  modeling: "border-purple-500",
  serving: "border-green-500",
  frontend: "border-cyan-500",
};

export default function PipelinePanel({ onClose }: { onClose: () => void }) {
  const [stack, setStack] = useState<PipelineStack | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.pipeline().then((s) => {
      setStack(s);
      setLoading(false);
    });
  }, []);

  return (
    <aside className="absolute right-0 top-0 h-full w-96 bg-slate-900/95 backdrop-blur text-white p-6 z-20 flex flex-col overflow-y-auto border-l border-slate-700">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-lg font-bold">Stack Tecnico</h2>
          <p className="text-slate-400 text-xs mt-1">Arquitectura de datos end-to-end</p>
        </div>
        <button onClick={onClose} className="text-slate-400 hover:text-white text-xl">✕</button>
      </div>

      {/* Pipeline flow */}
      <div className="flex items-center gap-1 text-xs text-slate-400 mb-6 flex-wrap">
        {["ingestion","storage","transformation","modeling","serving","frontend"].map((step, i) => (
          <span key={step} className="flex items-center gap-1">
            <span className="text-slate-300 capitalize">{step}</span>
            {i < 5 && <span className="text-slate-600">→</span>}
          </span>
        ))}
      </div>

      {loading ? (
        <p className="text-slate-400 animate-pulse">Cargando stack...</p>
      ) : !stack ? (
        <p className="text-slate-400">Stack no disponible — API desconectada</p>
      ) : (
        <div className="flex flex-col gap-4">
          {Object.entries(stack).map(([key, val]) => {
            const v = val as Record<string, unknown>;
            return (
              <div
                key={key}
                className={`bg-slate-800 rounded-lg p-4 border-l-4 ${COLORS[key] ?? "border-slate-600"}`}
              >
                <div className="flex items-center gap-2 mb-2">
                  <span>{ICONS[key]}</span>
                  <span className="font-semibold capitalize">{key}</span>
                  <span className="ml-auto text-xs text-slate-400 bg-slate-700 px-2 py-0.5 rounded">
                    {String(v.tool ?? "")}
                  </span>
                </div>
                <p className="text-slate-300 text-sm">{String(v.description ?? "")}</p>
                {Array.isArray(v.models) && (
                  <div className="mt-2 flex flex-wrap gap-1">
                    {(v.models as string[]).map((m) => (
                      <span key={m} className="text-xs bg-slate-700 text-slate-300 px-2 py-0.5 rounded">
                        {m}
                      </span>
                    ))}
                  </div>
                )}
                {Array.isArray(v.buckets) && (
                  <div className="mt-2 flex flex-wrap gap-1">
                    {(v.buckets as string[]).map((b) => (
                      <span key={b} className="text-xs bg-slate-700 text-yellow-300 px-2 py-0.5 rounded font-mono">
                        {b}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </aside>
  );
}
