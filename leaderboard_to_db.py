import datetime
import locale

import requests
import lxml.html

from sqlalchemy import Column, create_engine, func, types, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///subterfuge.db')
Session = sessionmaker()
Session.configure(bind=engine)


def str_to_int(s):
    if s == "-":
        return 0
    elif s.endswith('%'):
        return int(s[:-1])/100
    else:
        return int(s)


def main():
    Base.metadata.create_all(engine)
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

    page = requests.get('http://subterfuge-game.com/leaderboards.html')
    rows = lxml.html.fromstring(page.content).xpath('//table/tr')

    first_row = 'Rank Player Rating Ratedgames Totalgames Finished Eliminated Resigned Joined'
    if ' '.join(rows[0].text_content().split()) != first_row:
        raise IOError('Warning: Site has changed')

    s = Session()
    last_stats = dict(
        s.query(PlayerStats.player_id, func.max(PlayerStats.totalgames)).group_by(PlayerStats.player_id).all())
    for row in rows[1:]:
        r = [c.text_content() for c in row.xpath('./td')]

        playername = r[1]
        totalgames = str_to_int(r[7])
        joined_date = datetime.datetime.strptime(r[11], "%d %b %Y").date()

        player = s.query(Player).filter_by(playername=playername, joined=joined_date).first()
        if player is None:
            player = Player(playername=playername, joined=joined_date)

        if player.player_id not in last_stats or last_stats[player.player_id] != totalgames:
            ps = PlayerStats()
            ps.player = player
            ps.elo = str_to_int(r[2])
            ps.gold = str_to_int(r[3])
            ps.silver = str_to_int(r[4])
            ps.bronze = str_to_int(r[5])
            ps.ratedgames = str_to_int(r[6])
            ps.totalgames = totalgames
            ps.finished = str_to_int(r[8])
            ps.eliminated = str_to_int(r[9])
            ps.resigned = str_to_int(r[10])
            s.add(ps)

    s.commit()


class Player(Base):
    __tablename__ = 'player'

    player_id = Column(types.Integer, primary_key=True, autoincrement=True)
    playername = Column(types.String)
    joined = Column(types.Date)

    UniqueConstraint(playername, joined)

    def __str__(self):
        return '{ id: %d, playername: "%s", joined_date: %s }' % (self.player_id, self.playername, self.joined)


class PlayerStats(Base):
    __tablename__ = 'playerstats'

    playerstats_id = Column(types.Integer, primary_key=True, autoincrement=True)
    player_id = Column(types.Integer, ForeignKey(Player.player_id))
    timestamp = Column(types.TIMESTAMP, server_default=func.now())

    elo = Column(types.Integer)
    gold = Column(types.Integer)
    silver = Column(types.Integer)
    bronze = Column(types.Integer)
    ratedgames = Column(types.Integer)
    totalgames = Column(types.Integer)
    finished = Column(types.DECIMAL)
    eliminated = Column(types.DECIMAL)
    resigned = Column(types.DECIMAL)

    player = relationship(Player)

    UniqueConstraint(player_id, elo, gold, silver, bronze, ratedgames, totalgames, finished, resigned)


if __name__ == '__main__':
    main()
