-- CreateTable
CREATE TABLE "Player" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "joined" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "Leaderboard" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "timestamp" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "LeaderboardEntry" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "leaderboardId" INTEGER NOT NULL,
    "playerId" INTEGER NOT NULL,
    "rank" INTEGER NOT NULL,
    "elo" INTEGER NOT NULL,
    "gold" INTEGER NOT NULL,
    "silver" INTEGER NOT NULL,
    "bronze" INTEGER NOT NULL,
    "rated_games" INTEGER NOT NULL,
    "total_games" INTEGER NOT NULL,
    "finished" INTEGER NOT NULL,
    "eliminated" INTEGER NOT NULL,
    "resigned" INTEGER NOT NULL,
    CONSTRAINT "LeaderboardEntry_leaderboardId_fkey" FOREIGN KEY ("leaderboardId") REFERENCES "Leaderboard" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "LeaderboardEntry_playerId_fkey" FOREIGN KEY ("playerId") REFERENCES "Player" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateIndex
CREATE INDEX "Player_name_idx" ON "Player"("name");

-- CreateIndex
CREATE UNIQUE INDEX "Player_name_joined_key" ON "Player"("name", "joined");

-- CreateIndex
CREATE UNIQUE INDEX "Leaderboard_timestamp_key" ON "Leaderboard"("timestamp" DESC);

-- CreateIndex
CREATE INDEX "LeaderboardEntry_leaderboardId_rank_idx" ON "LeaderboardEntry"("leaderboardId", "rank");

-- CreateIndex
CREATE UNIQUE INDEX "LeaderboardEntry_playerId_leaderboardId_key" ON "LeaderboardEntry"("playerId", "leaderboardId");

