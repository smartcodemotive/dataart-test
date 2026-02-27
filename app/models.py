from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str

    projects: list["Project"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str = ""

    owner_id: int = Field(foreign_key="users.id", index=True)
    owner: User | None = Relationship(back_populates="projects")
