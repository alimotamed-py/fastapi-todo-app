# ==================== Add Library And Package ====================
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from app.database import Base, create_engine, sessionmaker, get_db
from app.config import app

# ==================== Add Library And Package ====================
SQLALCHEMY_DATABASE_URL = "sqllite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       'check_same_thread': False}, poolclass=StaticPool)


TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Module
@pytest.fixture(scope='module')
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Module
@pytest.fixture(scope='module', autouse=True)
def override_dependencies(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.pop(get_db, None)


# Session
@pytest.fixture(scope='session', autouse=True)
def tearup_and_down_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# function
@pytest.fixture(scope='function')
def anon_client():
    client = TestClient(app)
    yield client
