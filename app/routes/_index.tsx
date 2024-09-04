import { json, LoaderFunctionArgs, MetaFunction } from "@remix-run/cloudflare";
import { useLoaderData } from "@remix-run/react";
import { PrismaD1 } from "@prisma/adapter-d1";
import { PrismaClient } from "@prisma/client";

export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    {
      name: "description",
      content: "Welcome to Remix on Cloudflare!",
    },
  ];
};

export async function loader({ context }: LoaderFunctionArgs) {
  const env = context.cloudflare.env as Env;
  const adapter = new PrismaD1(env.DB);
  const prisma = new PrismaClient({ adapter });

  const page = 1;
  const page_size = 100;

  const lb = await prisma.leaderboard.findFirst({
    orderBy: { timestamp: "desc" },
    include: {
      entries: {
        where: { rank: { gt: page_size * (page - 1), lte: page_size * page } },
      },
    },
  });
  return json(lb);
}

export default function Index() {
  const results = useLoaderData<typeof loader>();
  return (
    <div style={{ fontFamily: "system-ui, sans-serif", lineHeight: "1.8" }}>
      <h1>Welcome to Remix</h1>
      <div>
        A value from D1:
        <pre>{JSON.stringify(results)}</pre>
      </div>
    </div>
  );
}
