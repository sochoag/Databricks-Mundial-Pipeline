const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface TeamStats {
  team_id: number;
  team_name: string;
  team_short_name: string;
  team_tla: string;
  crest_url: string;
  country: string;
  country_code: string;
  total_games: number;
  total_wins: number;
  total_draws: number;
  total_losses: number;
  goals_scored: number;
  goals_conceded: number;
  goal_difference: number;
  avg_goals_per_game: number;
}

export interface GroupStanding {
  group_name: string;
  position: number;
  team_id: number;
  team_name: string;
  crest_url: string;
  country_code: string;
  played_games: number;
  won: number;
  draw: number;
  lost: number;
  points: number;
  goals_for: number;
  goals_against: number;
  goal_difference: number;
}

export interface PipelineStack {
  ingestion: Record<string, unknown>;
  storage: Record<string, unknown>;
  transformation: Record<string, unknown>;
  modeling: Record<string, unknown>;
  serving: Record<string, unknown>;
  frontend: Record<string, unknown>;
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API}${path}`);
  if (!res.ok) throw new Error(`API error ${res.status}: ${path}`);
  return res.json();
}

export const api = {
  teams: () => get<TeamStats[]>("/teams/"),
  teamByCountry: (code: string) =>
    get<TeamStats[]>(`/teams/`).then((ts) =>
      ts.find((t) => t.country_code === code) ?? null
    ),
  standings: () => get<GroupStanding[]>("/standings/"),
  pipeline: () => get<PipelineStack>("/pipeline/"),
};
