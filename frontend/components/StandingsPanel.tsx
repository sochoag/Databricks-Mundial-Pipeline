"use client";

import { useEffect, useState } from "react";
import { api, GroupStanding } from "@/lib/api";

export default function StandingsPanel({ onClose }: { onClose: () => void }) {
  const [standings, setStandings] = useState<GroupStanding[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeGroup, setActiveGroup] = useState<string>("GROUP_A");

  useEffect(() => {
    api.standings().then((s) => {
      setStandings(s);
      setLoading(false);
    });
  }, []);

  const groups = [...new Set(standings.map((s) => s.group_name))].sort();
  const filtered = standings.filter((s) => s.group_name === activeGroup);

  return (
    <aside className="absolute left-0 top-0 h-full w-96 bg-slate-900/95 backdrop-blur text-white p-6 z-20 flex flex-col overflow-y-auto border-r border-slate-700">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold">Fase de Grupos</h2>
        <button onClick={onClose} className="text-slate-400 hover:text-white text-xl">✕</button>
      </div>

      {loading ? (
        <p className="text-slate-400 animate-pulse">Cargando...</p>
      ) : (
        <>
          <div className="flex flex-wrap gap-2 mb-4">
            {groups.map((g) => (
              <button
                key={g}
                onClick={() => setActiveGroup(g)}
                className={`px-3 py-1 rounded text-xs font-bold transition ${
                  activeGroup === g
                    ? "bg-emerald-600 text-white"
                    : "bg-slate-700 text-slate-300 hover:bg-slate-600"
                }`}
              >
                {g.replace("GROUP_", "")}
              </button>
            ))}
          </div>

          <table className="w-full text-sm">
            <thead>
              <tr className="text-slate-400 text-xs border-b border-slate-700">
                <th className="text-left py-2">#</th>
                <th className="text-left py-2">Equipo</th>
                <th className="py-2">PJ</th>
                <th className="py-2">G</th>
                <th className="py-2">E</th>
                <th className="py-2">P</th>
                <th className="py-2 text-emerald-400">Pts</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((row) => (
                <tr key={row.team_id} className="border-b border-slate-800 hover:bg-slate-800 transition">
                  <td className="py-2 text-slate-400">{row.position}</td>
                  <td className="py-2 font-medium">{row.team_name}</td>
                  <td className="py-2 text-center text-slate-300">{row.played_games}</td>
                  <td className="py-2 text-center text-emerald-400">{row.won}</td>
                  <td className="py-2 text-center text-yellow-400">{row.draw}</td>
                  <td className="py-2 text-center text-red-400">{row.lost}</td>
                  <td className="py-2 text-center font-bold text-emerald-400">{row.points}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </aside>
  );
}
