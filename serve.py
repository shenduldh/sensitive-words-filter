import uvicorn
import os
import click
from dotenv import load_dotenv


@click.command()
@click.option("--env", default="./.env")
def main(env):
    load_dotenv(env, override=True)

    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        reload_excludes=["tests/*", "logs/*"],
        reload_includes=["app/*", "assets/*", "src/*"],
        reload=True,
    )


if __name__ == "__main__":
    main()
