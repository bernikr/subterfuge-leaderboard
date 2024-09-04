import { ActionFunctionArgs, json } from "@remix-run/cloudflare";
import { PrismaD1 } from "@prisma/adapter-d1";
import { Prisma, PrismaClient } from "@prisma/client";
import LeaderboardEntryCreateWithoutLeaderboardInput = Prisma.LeaderboardEntryCreateWithoutLeaderboardInput;

type ApiImportLeaderboardEntry = {
  player_name: string;
  player_joined: string;

  rank: number;
  elo: number;
  gold: number;
  silver: number;
  bronze: number;
  rated_games: number;
  total_games: number;
  finished: number;
  eliminated: number;
  resigned: number;
};

type ApiImportLeaderboard = {
  timestamp: string;
  entries: ApiImportLeaderboardEntry[];
};

export async function loader() {
  return json({ error: "Method not supported" }, 405);
}

export async function action({ request, context }: ActionFunctionArgs) {
  if (request.method != "POST")
    return json({ error: "Method not supported" }, 405);

  const env = context.cloudflare.env as Env;
  const adapter = new PrismaD1(env.DB);
  const prisma = new PrismaClient({ adapter });

  const input = await request.json<ApiImportLeaderboard>();
  const timestamp = new Date(Date.parse(input.timestamp));

  await prisma.leaderboard.deleteMany({ where: { timestamp: timestamp } });
  const res = await prisma.leaderboard.create({
    data: {
      timestamp: new Date(Date.parse(input.timestamp)),
      entries: {
        create: input.entries.map(
          (e): LeaderboardEntryCreateWithoutLeaderboardInput => {
            const player_joined = new Date(Date.parse(e.player_joined));
            return {
              rank: e.rank,
              elo: e.elo,
              gold: e.gold,
              silver: e.silver,
              bronze: e.bronze,
              rated_games: e.rated_games,
              total_games: e.total_games,
              finished: e.finished,
              eliminated: e.eliminated,
              resigned: e.resigned,
              player: {
                connectOrCreate: {
                  where: {
                    name_joined: {
                      name: e.player_name,
                      joined: player_joined,
                    },
                  },
                  create: {
                    name: e.player_name,
                    joined: player_joined,
                  },
                },
              },
            };
          }
        ),
      },
    },
  });

  return json({ success: true, res: res });
}
