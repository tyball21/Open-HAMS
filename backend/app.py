# backend/app.py

from .factory import create_app

app = create_app(DevelopmentConfig)  # Or TestingConfig, ProductionConfig based on the environment

if __name__ == '__main__':
    app.run()
