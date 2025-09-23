from pydantic import BaseModel, Field


class Reference(BaseModel):
    """
    Represents a reference with page number and content.
    """

    page: int = Field(description="The page number where the reference is found.")
    content: str = Field(description="original content from source, do not alter")


class Topic(BaseModel):
    """
    Represents a topic with a title, explanation of a topic, and associated references.
    """

    title: str = Field(description="The title of the topic.")
    explanation: str = Field(
        description="A refined explanation of the topic, primarily based on the provided references."
    )
    references: list[Reference] = Field(
        description="A list of references that support or relate to the topic."
    )
