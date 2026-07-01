"use client";

import dynamic from "next/dynamic";
import { useState } from "react";
import TeamPanel from "@/components/TeamPanel";
import PipelinePanel from "@/components/PipelinePanel";
import StandingsPanel from "@/components/StandingsPanel";

const GlobeScene = dynamic(() => import("@/components/GlobeScene"), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center h-screen bg-slate-950 text-white">
      <p className="text-lg tracking-widest animate-pulse">CARGANDO GLOBO...</p>
    </div>
  ),
});

export type Panel = "team" | "pipeline" | "standings" | null;

export default function Home() {
  const [selectedCountry, setSelectedCountry] = useState<string | null>(null);
  const [activePanel, setActivePanel] = useState<Panel>(null);

  const handleCountryClick = (countryCode: string) => {
    setSelectedCountry(countryCode);
    setActivePanel("team");
  };

  return (
    <main className="relative w-screen h-screen bg-slate-950 overflow-hidden">
      <GlobeScene onCountryClick={handleCountryClick} />

      <header className="absolute top-0 left-0 right-0 p-6 flex items-start justify-between pointer-events-none z-10">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">
            Mundial de Datos
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            FIFA World Cup 2022 · Data Engineering Portfolio
          </p>
        </div>
        <nav className="flex gap-3 pointer-events-auto">
          <button
            onClick={() => setActivePanel(activePanel === "standings" ? null : "standings")}
            className="px-4 py-2 rounded-lg bg-slate-800/80 text-white text-sm hover:bg-slate-700 transition backdrop-blur"
          >
            Grupos
          </button>
          <button
            onClick={() => setActivePanel(activePanel === "pipeline" ? null : "pipeline")}
            className="px-4 py-2 rounded-lg bg-emerald-700/80 text-white text-sm hover:bg-emerald-600 transition backdrop-blur"
          >
            Stack Tecnico
          </button>
        </nav>
      </header>

      {!activePanel && (
        <p className="absolute bottom-8 left-1/2 -translate-x-1/2 text-slate-500 text-sm pointer-events-none z-10">
          Haz click en un pais participante para ver sus estadisticas
        </p>
      )}

      {activePanel === "team" && selectedCountry && (
        <TeamPanel countryCode={selectedCountry} onClose={() => setActivePanel(null)} />
      )}
      {activePanel === "pipeline" && (
        <PipelinePanel onClose={() => setActivePanel(null)} />
      )}
      {activePanel === "standings" && (
        <StandingsPanel onClose={() => setActivePanel(null)} />
      )}
    </main>
  );
}
