"use client";

import { useEffect, useState } from "react";
import { api, TeamStats } from "@/lib/api";

export default function TeamPanel({
  countryCode,
  onClose,
}: {
  countryCode: string;
  onClose: () => void;
}) {
  const [team, setTeam] = useState<TeamStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.teamByCountry(countryCode).then((t) => {
      setTeam(t);
      setLoading(false);
    });
  }, [countryCode]);

  return (
    <aside className="absolute right-0 top-0 h-full w-80 bg-slate-900/95 backdrop-blur text-white p-6 z-20 flex flex-col overflow-y-auto border-l border-slate-700">
      <button
        onClick={onClose}
        className="self-end text-slate-400 hover:text-white text-xl mb-4"
        aria-label="Cerrar"
      >
        ✕
      </button>

      {loading ? (
        <p className="text-slate-400 animate-pulse">Cargando...</p>
      ) : !team ? (
        <div>
          <p className="text-slate-400 text-sm">
            Pais no encontrado en el Mundial 2022.
          </p>
          <p className="text-slate-500 text-xs mt-2">Codigo: {countryCode}</p>
        </div>
      ) : (
        <>
          <div className="flex items-center gap-3 mb-6">
            {team.crest_url && (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={team.crest_url} alt={team.team_name} className="w-12 h-12 object-contain" />
            )}
            <div>
              <h2 className="text-xl font-bold">{team.team_name}</h2>
              <p className="text-slate-400 text-sm">{team.country}</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <Stat label="Partidos" value={team.total_games} />
            <Stat label="Victorias" value={team.total_wins} color="text-emerald-400" />
            <Stat label="Empates" value={team.total_draws} color="text-yellow-400" />
            <Stat label="Derrotas" value={team.total_losses} color="text-red-400" />
            <Stat label="Goles a favor" value={team.goals_scored} />
            <Stat label="Goles en contra" value={team.goals_conceded} />
            <Stat
              label="Diferencia"
              value={team.goal_difference > 0 ? `+${team.goal_difference}` : team.goal_difference}
              color={team.goal_difference > 0 ? "text-emerald-400" : "text-red-400"}
            />
            <Stat label="Goles/partido" value={team.avg_goals_per_game} />
          </div>
        </>
      )}
    </aside>
  );
}

function Stat({
  label,
  value,
  color = "text-white",
}: {
  label: string;
  value: string | number;
  color?: string;
}) {
  return (
    <div className="bg-slate-800 rounded-lg p-3">
      <p className="text-slate-400 text-xs">{label}</p>
      <p className={`text-xl font-bold mt-1 ${color}`}>{value}</p>
    </div>
  );
}
