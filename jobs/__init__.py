from flask import Flask

def create_app():
    app=Flask("jobs")
    app.config.from_mapping(
        DATABASE="naukri"
    )

    from . import jobs
    app.register_blueprint(jobs.bp)

    return app