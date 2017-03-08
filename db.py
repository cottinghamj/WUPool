from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Enum, Boolean, MetaData, ForeignKey, Sequence
metadata = MetaData()

from sqlalchemy.orm import sessionmaker, relationship
Session = sessionmaker(bind=engine)
#Session = sessionmaker()

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), nullable=False)
    firstname = Column(String(30))
    lastname = Column(String(30))
    password = Column(String(64), nullable=False)
    email = Column(String(100), nullable=False)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.username, self.firstname + self.lastname, self.password)

class PoolGame(Base):
    __tablename__ = 'PoolGames'

    id = Column(Integer, Sequence('game_id_seq'), primary_key=True)
    type = Column(Enum('1v1', '2v2'), nullable=False)
    ### Bug: Need to build a constraint for when a certain level is checked, our player 2's are filled
    ### Might consider generalizing players into a table of their own
    side_1_p1_id = Column(Integer,  ForeignKey('Users.id'), nullable=False)
    side_1_p2_id = Column(Integer, ForeignKey('Users.id'), nullable=False, default=-1)
    side_2_p1_id = Column(Integer,  ForeignKey('Users.id'), nullable=False)
    side_2_p2_id = Column(Integer, ForeignKey('Users.id'), nullable=False, default=-1)
    time = Column(Integer)
    winner_side_1 = Column(Boolean, nullable=False) # Did side 1 win? If not side 2 won! Might need to make exception for tie

    side_1_p1 = relationship("User", foreign_keys=[side_1_p1_id])
    side_1_p2 = relationship("User", foreign_keys=[side_1_p2_id])
    side_2_p1 = relationship("User", foreign_keys=[side_2_p1_id])
    side_2_p2 = relationship("User", foreign_keys=[side_2_p2_id])
    
    
Base.metadata.create_all(engine)

session = Session()
ed_user = User(username='ed', firstname='ed', lastname='last', password='pass', email='email')
ed2_user = User(username='ed2', firstname='ed2', lastname='last', password='pass', email='email')
session.add(ed_user)
our_user = session.query(User).filter_by(username='ed').first()