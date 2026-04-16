import os
from flask import Flask

def create_app(test_config=None):
    # 初始化 Flask 實體
    app = Flask(__name__, instance_relative_config=True)
    
    # 載入配置
    app.config.from_object('config.Config')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊所有的 Blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.history import history_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(history_bp)

    return app
